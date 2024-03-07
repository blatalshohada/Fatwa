# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    whatsapp_meta_phone_number_id = fields.Char(string='Whatsapp meta Phone Number Id')
    whatsapp_meta_api_token = fields.Char('Whatsapp meta Token')
    module_whatsapp_meta_webhook_verify = fields.Boolean(string="verify webhook")
    whatsapp_meta_webhook_token = fields.Char('Meta Webhook Verify Token')
    whatsapp_meta_webhook_callback_url = fields.Char(string="webhook's callback URL", readonly=True, help='Please update the Meta Api account webhook configuration with this information.')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        config_parameters = self.env['ir.config_parameter']
        config_parameters.set_param("whatsapp_meta_phone_number_id", self.whatsapp_meta_phone_number_id)
        config_parameters.set_param("whatsapp_meta_api_token", self.whatsapp_meta_api_token)
        config_parameters.set_param("module_whatsapp_meta_webhook_verify", self.module_whatsapp_meta_webhook_verify)
        config_parameters.set_param("whatsapp_meta_webhook_token", self.whatsapp_meta_webhook_token)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(whatsapp_meta_phone_number_id=self.env['ir.config_parameter'].get_param(
            'whatsapp_meta_phone_number_id'))
        res.update(whatsapp_meta_api_token=self.env['ir.config_parameter'].get_param(
            'whatsapp_meta_api_token'))
        res.update(module_whatsapp_meta_webhook_verify=self.env['ir.config_parameter'].get_param(
            'module_whatsapp_meta_webhook_verify'))
        res.update(whatsapp_meta_webhook_token=self.env['ir.config_parameter'].get_param(
            'whatsapp_meta_webhook_token'))
        res.update(whatsapp_meta_webhook_callback_url=self.env['ir.config_parameter'].get_param(
            'whatsapp_meta_webhook_callback_url'))
        return res

    def get_base_url(self):
        for record in self:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            base_url_route = base_url + '/whatsapp_meta/response/message'
            record.whatsapp_meta_webhook_callback_url = base_url_route
            self.env['ir.config_parameter'].set_param("whatsapp_meta_webhook_callback_url", base_url_route)
