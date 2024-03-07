import logging
from odoo import http, _
from odoo.http import request
from ... import whatsapp_helpdesk_create_ticket


_logger = logging.getLogger(__name__)

class WhatsappWebhookVerify(whatsapp_helpdesk_create_ticket.controller.main.Whatsapp):

    @http.route('/whatsapp_meta/response/message', type='http', auth='public', methods=['GET', 'POST'], website=True) #webhook receiving function
    def whatsapp_meta_webhook(self):
        _logger.info("In whatsapp integration controller verification")

        Param = request.env['res.config.settings'].sudo().get_values()
        whatsapp_verify_token = Param.get('whatsapp_meta_webhook_token')

        VERIFY_TOKEN = whatsapp_verify_token

        if 'hub.mode' in request.httprequest.args:
            mode = request.httprequest.args.get('hub.mode')
        if 'hub.verify_token' in request.httprequest.args:
            token = request.httprequest.args.get('hub.verify_token')

        if 'hub.challenge' in request.httprequest.args:
            challenge = request.httprequest.args.get('hub.challenge')

        if 'hub.mode' in request.httprequest.args and 'hub.verify_token' in request.httprequest.args:
            mode = request.httprequest.args.get('hub.mode')
            token = request.httprequest.args.get('hub.verify_token')
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                challenge = request.httprequest.args.get('hub.challenge')
                is_instance_verify = Param.get('module_whatsapp_meta_webhook_verify')
                if is_instance_verify:
                    request.env['ir.config_parameter'].sudo().set_param(
                        'module_whatsapp_meta_webhook_verify', False)
                    module_whatsapp_meta_webhook_verify = False
                return http.Response(challenge, status=200)

                # return challenge, 200
            else:
                return http.Response('ERROR', status=403)

        return 'SOMETHING', 200
