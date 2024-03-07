from datetime import datetime
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
from dateutil.relativedelta import relativedelta

class WizardBatchCollect(models.TransientModel):
   _name = "wizard.helpdesk.report1"

   @api.model
   def _default_type_id(self):
      warehouse = self.env['helpdesk.ticket.type'].sudo().search(
         [('name', '=', 'استفتاء')], limit=1)
      return warehouse


   date_from = fields.Date(string='تاريخ البداية ', required=True,default=fields.Date.today() + relativedelta(months=-1))
   date_to = fields.Date(string='تاريخ النهاية', required=True,default=fields.Date.context_today,)
   question_type_id = fields.Many2one('helpdesk.ticket.type',string='نوع السؤال',required=1,default=lambda self: self._default_type_id())
   sender_id = fields.Many2one('sender.type', string='الراسل')
   user_id=fields.Many2one('res.users',string='مسند الى ')
   question_status_id = fields.Many2one('question.status', string='حالة السؤال')
   priority = fields.Selection([
    ('0', 'All'),
    ('1', 'Low priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
], string='الاولوية')





   @api.constrains('date_from', 'date_to')
   def check_date_constrain(self):
      if self.date_from != False and self.date_to != False and self.date_from > self.date_to:
         raise ValidationError(_("Date start Must be less than date end"))



   def print_pdf(self):
      [data] = self.read()
      datas = {
         'ids': [],
         'model': 'website.support.ticket',
         'form': data
      }
      return self.env.ref('helpdesk_ticket_reports.print_report_pdf_helpdesk_report1').report_action([],data=datas)





