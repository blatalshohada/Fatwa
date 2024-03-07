# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from requests.structures import CaseInsensitiveDict
import requests
import logging
import json

_logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    # send and receive whatsapp message history recorded
    whatsapp_message_ids = fields.One2many('whatsapp.messages', 'helpdesk_id', invisible=True,
                                           string='Whatsapp Messages')

    # @api.model_create_multi
    # def create(self, list_value):
    #     tickets = super(HelpdeskTicket, self).create(list_value)

    #     # send newly created ticket information to customer function call
    #     for ticket in tickets:
    #         ticket.send_message_on_whatsapp_meta(ticket)

    #     return tickets

    # def write(self, vals):
    #     res = super(HelpdeskTicket, self).write(vals)
    #     if 'stage_id' in vals:
    #         stage_id = vals['stage_id']
    #         if stage_id:
    #             self.stage_change_send_message_on_whatsapp_meta(stage_id)
    #     return res

    def meta_create_whatsapp_message(self, recipient_phone_number, message, message_id, provider):
        whatsapp_messages_dict = {
            'senderName': 'Me',
            'to': recipient_phone_number,
            'message_id': message_id,
            'message_body': message,
            'time': fields.Datetime.now(),
            'state': 'sent',
            'helpdesk_id': self.id ,
            'whatsapp_message_provider': provider,
        }
        whatsapp_messages_id = self.env['whatsapp.messages'].sudo().create(whatsapp_messages_dict)
        _logger.info("Whatsapp message created in odoo from meta.")

    def send_message_on_whatsapp_meta(self, helpdesk_ticket):
        Param = self.env['res.config.settings'].sudo().get_values()

        phone_id = Param.get('whatsapp_meta_phone_number_id')
        access_token = Param.get('whatsapp_meta_api_token')
        req_headers = CaseInsensitiveDict()
        req_headers["Authorization"] = "Bearer " + access_token
        req_headers["Content-Type"] = "application/json"
        url = "https://graph.facebook.com/v15.0/{}/messages".format(phone_id)

        for ticket in helpdesk_ticket:
            if ticket.partner_id:
                if ticket.partner_id.mobile:
                    whatsapp_msg_number_without_space = ticket.partner_id.mobile.replace(" ", "")
                    whatsapp_msg_number_without_code = whatsapp_msg_number_without_space.replace(
                        '+' + str(ticket.partner_id.country_id.phone_code), "")
                    recipient_phone_number = str(
                        ticket.partner_id.country_id.phone_code) + whatsapp_msg_number_without_code
                else:
                    raise UserError(_('Please enter Customer mobile number'))
            else:
                raise UserError(_('Please choose a customer first'))
            if ticket.stage_id.id == 1:
                whatsapp_template_obj = self.env['whatsapp.templates']
                whatsapp_template_id = whatsapp_template_obj.sudo().search(
                    [('name', '=', 'new_ticket')],
                    limit=1)
                if whatsapp_template_id:
                    message = whatsapp_template_id.message_content
                else:
                    raise UserError(
                        _("WhatsApp template not found.Please create the 'New Ticket' WhatsApp templates"))
                payload = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": recipient_phone_number,
                    "type": "text",
                    "text": {
                        "body": message,
                    }
                }
                response = requests.post(url, headers=req_headers, json=payload)
                _logger.info("\nJson Response: {}".format(response.json()))
                if response.status_code == 201 or response.status_code == 200:
                    _logger.info("\nSend Message successfully")

                    response_dict = json.loads(response.text)
                    self.meta_create_whatsapp_message(recipient_phone_number, message,response_dict.get('messages')[
                                                                                          0].get('id'), 'Meta',)

    def stage_change_send_message_on_whatsapp_meta(self, stage_id):
        Param = self.env['res.config.settings'].sudo().get_values()

        phone_id = Param.get('whatsapp_meta_phone_number_id')
        access_token = Param.get('whatsapp_meta_api_token')
        req_headers = CaseInsensitiveDict()
        req_headers["Authorization"] = "Bearer " + access_token
        req_headers["Content-Type"] = "application/json"
        url = "https://graph.facebook.com/v15.0/{}/messages".format(phone_id)

        if self.partner_id:
            if self.partner_id.mobile:
                whatsapp_msg_number_without_space = self.partner_id.mobile.replace(" ", "")
                whatsapp_msg_number_without_code = whatsapp_msg_number_without_space.replace(
                    '+' + str(self.partner_id.country_id.phone_code), "")
                recipient_phone_number = str(
                    self.partner_id.country_id.phone_code) + whatsapp_msg_number_without_code
            else:
                raise UserError(_('Please enter Customer mobile number'))
        else:
            raise UserError(_('Please choose a customer first'))
        if stage_id == 2:
            whatsapp_template_obj = self.env['whatsapp.templates']
            whatsapp_template_id = whatsapp_template_obj.sudo().search(
                [('name', '=', 'ticket_in_progress')],
                limit=1)
            if whatsapp_template_id:
                message = whatsapp_template_id.message_content
            else:
                raise UserError(_("WhatsApp template not found.Please create the 'Ticket In Progress' WhatsApp template"))

            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_phone_number,
                "type": "text",
                "text": {
                    "body": message,
                }
            }
            response = requests.post(url, headers=req_headers, json=payload)
            _logger.info(
                "Json Response of helpdesk.ticket move to in progress send message: {}".format(response.json()))

            if response.status_code == 201 or response.status_code == 200:
                _logger.info("\nSend Message successfully")

                response_dict = json.loads(response.text)
                self.meta_create_whatsapp_message(recipient_phone_number, message, response_dict.get('messages')[
                    0].get('id'), 'Meta', )

        elif stage_id == 3:
            whatsapp_template_obj = self.env['whatsapp.templates']
            whatsapp_template_id = whatsapp_template_obj.sudo().search(
                [('name', '=', 'ticket_in_solved')],
                limit=1)
            if whatsapp_template_id:
                message = whatsapp_template_id.message_content
            else:
                raise UserError(_("WhatsApp template not found.Please create the 'Ticket In Solved' WhatsApp template"))

            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_phone_number,
                "type": "text",
                "text": {
                    "body": message,
                }
            }
            response = requests.post(url, headers=req_headers, json=payload)
            _logger.info(
                "Json Response of helpdesk.ticket move to in progress send message: {}".format(response.json()))

            if response.status_code == 201 or response.status_code == 200:
                _logger.info("\nSend Message successfully")

                response_dict = json.loads(response.text)
                self.meta_create_whatsapp_message(recipient_phone_number, message, response_dict.get('messages')[
                    0].get('id'), 'Meta', )

        elif stage_id == 4:
            whatsapp_template_obj = self.env['whatsapp.templates']
            whatsapp_template_id = whatsapp_template_obj.sudo().search(
                [('name', '=', 'ticket_in_cancelled')],
                limit=1)
            if whatsapp_template_id:
                message = whatsapp_template_id.message_content
            else:
                raise UserError(_("WhatsApp template not found.Please create the 'Ticket Cancelled' WhatsApp template"))

            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_phone_number,
                "type": "text",
                "text": {
                    "body": message,
                }
            }
            response = requests.post(url, headers=req_headers, json=payload)
            _logger.info(
                "Json Response of helpdesk.ticket move to in progress send message: {}".format(response.json()))

            if response.status_code == 201 or response.status_code == 200:
                _logger.info("\nSend Message successfully")

                response_dict = json.loads(response.text)
                self.meta_create_whatsapp_message(recipient_phone_number, message, response_dict.get('messages')[
                    0].get('id'), 'Meta', )

    def send_message_on_whatsapp_fatwa(self):
        update_msg = self.fatwa_new_replay

        if self.partner_id.country_id.phone_code and self.partner_id.mobile:
            whatsapp_number = self.partner_id.mobile
            whatsapp_msg_number_without_space = whatsapp_number.replace(" ", "")
            whatsapp_msg_number_without_code = whatsapp_msg_number_without_space.replace(
                '+' + str(self.partner_id.country_id.phone_code), "")

            recipient_phone_number = str(self.partner_id.country_id.phone_code) + whatsapp_msg_number_without_code

            Param = self.env['res.config.settings'].sudo().get_values()
            phone_id = Param.get('whatsapp_meta_phone_number_id')
            access_token = Param.get('whatsapp_meta_api_token')
            url = "https://graph.facebook.com/v15.0/{}/messages".format(phone_id)
            req_headers = CaseInsensitiveDict()
            req_headers["Authorization"] = "Bearer " + access_token
            req_headers["Content-Type"] = "application/json"

            data_json = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_phone_number,
                "type": "text",
                "text": {
                    "body": update_msg,
                }
            }
            response = requests.post(url, headers=req_headers, data=json.dumps(data_json))
            _logger.info("Json Response of send msg button: {}".format(response.json()))
            if response.status_code == 201 or response.status_code == 200:
                _logger.info("\nSend Message successfully")
                json_response = response.json()
                self.meta_create_whatsapp_message(recipient_phone_number, update_msg,json_response.get('messages')[
                                                                                        0].get('id'), 'Meta',)
        else:
            raise UserError(_('Please enter %s mobile number and select country', self.partner_id))
