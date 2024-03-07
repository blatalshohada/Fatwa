from odoo import  models, fields, api
import logging

_logger = logging.getLogger(__name__)

class LandingPage(models.Model):
    _name = 'landing.page'
    name = fields.Char('Title')
    action_id = fields.Char('ID')
    #helpdesk.ticket xml_id = helpdesk.helpdesk_ticket_action_main  كافة الفتاوى
