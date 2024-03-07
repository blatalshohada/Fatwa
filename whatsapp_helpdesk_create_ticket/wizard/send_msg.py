# -*- coding: utf-8 -*-
import logging
import json
import requests
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from requests.structures import CaseInsensitiveDict
import re


_logger = logging.getLogger(__name__)


class SendWAMessage(models.TransientModel):
    _name = 'whatsapp.msg'
    _description = 'Send WhatsApp Message'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def default_get(self, fields):
        res = super(SendWAMessage, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        res_id = self.env.context.get('active_id')
        rec = self.env[active_model].browse(res_id)
        if rec.partner_id:
            default_partner_id = rec.partner_id.id
        else:
            raise UserError(_('Please choose a customer first'))
        res.update({'partner_id': default_partner_id})
        return res

    partner_id = fields.Many2one('res.partner', string='Recipients', required=True)
    message = fields.Text('Message', required=True)

    def action_send_msg(self):
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')
        if active_model == 'helpdesk.ticket':
            rec = self.env[active_model].browse(active_id)

            update_msg = self.message

            if rec.partner_id.country_id.phone_code and rec.partner_id.mobile:
                whatsapp_number = rec.partner_id.mobile
                whatsapp_msg_number_without_space = whatsapp_number.replace(" ", "")
                whatsapp_msg_number_without_code = whatsapp_msg_number_without_space.replace(
                    '+' + str(rec.partner_id.country_id.phone_code), "")

                recipient_phone_number = str(rec.partner_id.country_id.phone_code) + whatsapp_msg_number_without_code

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
                    rec.meta_create_whatsapp_message(recipient_phone_number, update_msg,json_response.get('messages')[
                                                                                          0].get('id'), 'Meta',)
            else:
                raise UserError(_('Please enter %s mobile number and select country', rec.partner_id))