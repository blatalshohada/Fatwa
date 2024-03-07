# -*- coding: utf-8 -*-
from odoo import fields, models,api ,_
import html2text
import logging

_logger = logging.getLogger(__name__)

# This model inherites helpdesk_ticket model to make sure the body of the reached email is represented in the ticket's description.

class Helpdesk(models.Model):
    _inherit = "helpdesk.ticket"

    @api.depends('create_date')
    def get_create_date(self):
        for rec in self:
            rec.date = rec.create_date.date()
            message=self.env['mail.message'].sudo().browse(rec.message_ids.ids)
            message_body= html2text.html2text(message.mapped('body')[0] )
            message_compare=message_body.replace('\n', '<br/>')

            #_logger.info("rec.fatwa_question_channel_id.name: %s", rec.fatwa_question_channel_id.name)
            #_logger.info("message_compare: %s", message_compare)
            # ftawa.mnarat@gmail.com
            # message.get('to')
            #_logger.info("to: %s", message.get('to'))
            #_logger.info("partner_email: %s", rec.partner_email)

            if rec.partner_email != '':
                _logger.info("قناة وصول التذكرة - بريدية بديهيا")
                ticket_in = self.env['question.channel'].search(
                    [('name', '=', 'بريد'), ],
                    limit=1,
                )
                rec.write({'description': message_body,'fatwa_question_channel_id': ticket_in})                
            elif rec.fatwa_question_channel_id.name == 'المكتب':
                _logger.info("قناة وصول التذكرة - المكتب")
            elif rec.fatwa_question_channel_id.name == 'واتساب':
                _logger.info("قناة وصول التذكرة - واتساب")
            elif message_compare == 'تم إنشاء تذكرة مكتب المساعدة<br/><br/>':
                _logger.info("قناة وصول التذكرة - بدون قناة")
            else:
                _logger.info("قناة وصول التذكرة - بريدية بديهيا")
                ticket_in = self.env['question.channel'].search(
                    [('name', '=', 'بريد'), ],
                    limit=1,
                )
                rec.write({'description': message_body,'fatwa_question_channel_id': ticket_in})




