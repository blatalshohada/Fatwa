# -*- coding: utf-8 -*-
from odoo import fields, models,api ,_


class Helpdesk(models.Model):
    _inherit = "helpdesk.ticket"

    date=fields.Date(compute='get_create_date',store=1)
    # question_status_id = fields.Many2one('question.status', string='حالة السوال')
    # priority_value=fields.Char(compute='get_priority_value')
    # ticket_id=fields.Many2one('helpdesk.ticket',string='السؤال الاصلى قبل تنقيحات المراجع')
    # ticket_ids=fields.Many2many('helpdesk.ticket','relation_helpdesk','helpd_column1','helpd_column1_column2',string='Grade Category')
    # partner_phone=fields.Char('واتساب المستفتى')
    # fatwa_links=fields.Char('رابط الفتوى الصوتية' )



    # @api.onchange('partner_id')
    # def get_customer_phone(self):
    #     if self.partner_id:
    #         self.partner_phone=self.partner_id.mobile
    #
    # @api.depends('priority')
    # def get_priority_value(self):
    #     for rec in self:
    #          rec.priority_value=dict(rec._fields['priority'].selection).get(rec.priority)
    #
    @api.depends('create_date')
    def get_create_date(self ):
        for rec in self:
            rec.date=rec.create_date.date()
            # message=self.env['mail.message'].sudo().browse(rec.message_ids.ids)
            # rec.description=message.mapped('body')
    #
    #
    # def onchange_stage_id(self):
    #     for rec in self:
    #         rec.activity_schedule('helpdesk_ticket_reports.schdule_activity_helpdesk',
    #             user_id=rec.user_id.id,
    #             note='تم تحريك هذه الفتوه الى ' + ' ' + str(rec.stage_id.name) + str(
    #             ) + '.<br/>')
    #         print("aaaaaaa", rec.message_ids)
    #
    # def confirm_mail (self):
    #    ir_model_data = self.env['ir.model.data']
    #    template_res = self.env['mail.template']
    #    template_id = ir_model_data.get_object_reference('helpdesk_ticket_reports', 'medical_email_30_template')[1]
    #
    #    template = template_res.browse(template_id)
    #    for rec in self:
    #        email_values = {
    #            'email_to': rec.partner_id.email,
    #            'email_from': rec.company_id.email,
    #            'subject': 'الرد على السوال',
    #        }
    #
    #        template.body_html = '<p>عزيزى المستفتى  ${(object.partner_id.name)},''<br/><br/>  نود ابلاغ حضرتكم بانه تم الاجابه على  الفتوة رقم' + ' ' + str( rec.name)  + ' سوال بعنوان  . <br/><br/>' +  ' ' + str( rec.description) + ' والاجابة هى . <br/><br/>' \
    #                             + str( rec.fatwa_replay) + '  '  'شكرا جزيلا,<br/>' \
    #                        '${(object.company_id.name)}'
    #
    #        template.send_mail(rec.id, force_send=True, email_values=email_values)


