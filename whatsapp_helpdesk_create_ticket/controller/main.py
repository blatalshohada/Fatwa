import logging
from odoo import http, _
from odoo.http import request
import json
import phonenumbers
from odoo.addons.phone_validation.tools import phone_validation
from odoo import fields


_logger = logging.getLogger(__name__)

class Whatsapp(http.Controller):

    # webhook receiving function
    @http.route('/whatsapp_meta/response/message', type='json', auth='public', methods=['GET', 'POST'],
                website=True,
                csrf=False)
    def whatsapp_meta_webhook(self):
        _logger.info(
            "\nIn Meta api whatsapp integration whatsapp_helpdesk_create_ticket webhook route controller")
        data = json.loads(request.httprequest.data)
        _logger.info("data %s: ", str(data))
        _request = data

        text_body = data.get('entry') and data.get('entry')[0].get('changes') and \
                    data.get('entry')[0].get('changes')[0].get('value') and data.get('entry')[0].get('changes')[
                        0].get('value').get('messages') and \
                    data.get('entry')[0].get('changes')[0].get('value').get('messages')[0].get('text') and data.get('entry')[0].get('changes')[0].get('value').get('messages')[0].get('text').get('body')
        profile_name = data.get('entry') and data.get('entry')[0].get('changes') and \
                    data.get('entry')[0].get('changes')[0].get('value') and data.get('entry')[0].get('changes')[0].get('value').get('contacts') and data.get('entry')[0].get('changes')[0].get('value').get('contacts')[0].get('profile') and data.get('entry')[0].get('changes')[0].get('value').get('contacts')[0].get('profile').get('name')
        chat_id = data.get('entry') and data.get('entry')[0].get('changes') and \
                    data.get('entry')[0].get('changes')[0].get('value') and data.get('entry')[0].get('changes')[0].get('value').get('contacts') and data.get('entry')[0].get('changes')[0].get('value').get('contacts')[0].get('wa_id')

        if chat_id:
            chatid_split = chat_id.split('@')
            mobile = '+' + chatid_split[0]
            mobile_coutry_code = phonenumbers.parse(mobile, None)
            mobile_number = mobile_coutry_code.national_number
            country_code = mobile_coutry_code.country_code
            res_country_id = request.env['res.country'].sudo().search([('phone_code', '=', country_code)],
                                                                      limit=1)
            reg_sanitized_number = phone_validation.phone_format(str(mobile_number), res_country_id.code,
                                                                 country_code)
        if text_body:
            res_partner_obj = request.env["res.partner"].sudo().search([('mobile', '=', reg_sanitized_number)])
            if res_partner_obj:
                helpdesk_ticket_obj = request.env['helpdesk.ticket']
                helpdesk_ticket_id = ''
                solved_stage_id = request.env.ref('helpdesk.stage_solved').id
                cancel_stage_id = request.env.ref('helpdesk.stage_cancelled').id

                helpdesk_ticket_id = helpdesk_ticket_obj.sudo().search([('partner_id', '=', res_partner_obj.id),
                                                                        ('stage_id', 'not in',
                                                                         [solved_stage_id, cancel_stage_id])],
                                                                       limit=1)
                if not helpdesk_ticket_id:
                    helpdesk_ticket_id = helpdesk_ticket_obj.sudo().create({
                        'name': profile_name,
                        'partner_id': res_partner_obj.id,
                        'stage_id': request.env.ref('helpdesk.stage_new').id
                    })
                    _logger.info("Helpdesk ticket id1 %s: ", str(helpdesk_ticket_id))
                    result_lines = text_body.split('\n')
                    if len(result_lines) == 1:
                        result_lines = text_body.split('<br>')
                        if len(result_lines) == 1:
                            result_lines = text_body.split('<br/>')
                            if len(result_lines) == 1:
                                result_lines = text_body.split('<br />')
                    helpdesk_ticket_id.name = str(result_lines[0])
                    helpdesk_ticket_id.description = str(text_body)

                    ticket_in = request.env['question.channel'].sudo().search(
                        [('name', '=', 'واتساب'), ],
                        limit=1,
                    )
                    helpdesk_ticket_id.fatwa_question_channel_id = ticket_in
                else:
                    whatsapp_msg = request.env['whatsapp.messages']
                    whatsapp_message_dict = {
                        'message_body': text_body,
                        'senderName': profile_name,
                        'to': 'Me',
                        'state': 'received',
                        # 'message_id': data_dict_reply,
                        'time': fields.Datetime.now(),
                        'helpdesk_id': helpdesk_ticket_id.id,
                    }
                    whatsapp_message_id = whatsapp_msg.sudo().create(whatsapp_message_dict)
            else:
                res_partner_obj = request.env["res.partner"].sudo().create(
                            {'name': profile_name,
                             'mobile': reg_sanitized_number,
                             'country_id': res_country_id.id if res_country_id else None})
                helpdesk_ticket_obj = request.env['helpdesk.ticket']
                helpdesk_ticket_id = ''
                solved_stage_id = request.env.ref('helpdesk.stage_solved').id
                cancel_stage_id = request.env.ref('helpdesk.stage_cancelled').id
                helpdesk_ticket_id = helpdesk_ticket_obj.sudo().search([('partner_id', '=', res_partner_obj.id),
                                                                        ('stage_id', 'not in',
                                                                         [solved_stage_id, cancel_stage_id])],
                                                                       limit=1)
                if not helpdesk_ticket_id:
                    helpdesk_ticket_id = helpdesk_ticket_obj.sudo().create({
                        'name': profile_name,
                        'partner_id': res_partner_obj.id,
                        'stage_id': request.env.ref('helpdesk.stage_new').id
                    })
                    _logger.info("Helpdesk ticket id1 %s: ", str(helpdesk_ticket_id))
                    result_lines = text_body.split('\n')
                    if len(result_lines) == 1:
                        result_lines = text_body.split('<br>')
                        if len(result_lines) == 1:
                            result_lines = text_body.split('<br/>')
                            if len(result_lines) == 1:
                                result_lines = text_body.split('<br />')
                    helpdesk_ticket_id.name = str(result_lines[0])
                    helpdesk_ticket_id.description = str(text_body)

                    ticket_in = request.env['question.channel'].sudo().search(
                        [('name', '=', 'واتساب'), ],
                        limit=1,
                    )
                    helpdesk_ticket_id.fatwa_question_channel_id = ticket_in

