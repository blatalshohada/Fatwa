from odoo import  _ ,models, fields, api

import logging
TICKET_PRIORITY = [
    ('0', 'All'),
    ('1', 'Low priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
]

_logger = logging.getLogger(__name__)


class sourcefatwa(models.Model):
    _name = 'fatwa.source'

    name=fields.Char('المصدر')
    
class fatwa(models.Model):
    _inherit = 'helpdesk.ticket'
    _order = 'write_date desc'


    def _get_ticket_type(self):
        ticket_in = self.env['helpdesk.ticket.type'].search(
            [('name', '=', 'استفتاء'),],
            limit=1,
        )
        return ticket_in

    def _get_fatwa_source(self):
        ticket_in = self.env['fatwa.source'].search(
            [('name', '=', 'عبر النظام'),],
            limit=1,
        )
        return ticket_in

    def _get_fatwa_department(self):
        ticket_in = self.env['fatwa.department'].search(
            [('name', '=', 'عبادات'),],
            limit=1,
        )
        return ticket_in

    def _get_quest_channel(self):
        ticket_in = self.env['question.channel'].search(
            [('name', '=', 'المكتب'),],
            limit=1,
        )
        return ticket_in


    seq = fields.Char(copy=False,string='مسلسل الفتوى',readonly=1, required=False, index=True ,default=lambda self: _('New'))
    fatwa_replay = fields.Text('fatwa replay',)
    fatwa_new_replay=fields.Text('مختصر جواب الفتوى')
    fatwa_question=fields.Text('نص الفتوى بعد التنقيح')
    fatwa_question_channel_id=fields.Many2one('question.channel',string='قناة وصول السؤال',default=_get_quest_channel)
    # fatwa_question_channel_id = fields.Many2one('question.channel', string='قناة وصول السؤال',)
    sender_id = fields.Many2one('sender.type', string='نوع الراسل')
    fatwa_date=fields.Date(default=fields.Date.today,string='تاريخ الفتوى')
    name = fields.Char(string='عنوان الفتوى', required=True, index=True)
    state = fields.Selection([

        ('studying', 'تحت الدراسة'),
        ('saved', 'محفوظة'),
        ('refused', 'مرفوضة'),
        ('choiced', 'مختارة'),
        ('resolution', 'قرار'),
        ('fatwa', 'افتاء'),
        ('edit', 'تعديل'),
        ('urgent', 'مستعجلة'),
        ('reserved', 'محجوزة'),
        ('repeated', 'مكررة'),
        ('to_treat', 'معالجة'),
        ('fake', 'وهمية'),
        ('receive', 'استقبال'),
    ],
        string='الحالة',
        default='receive')


    archive = fields.Selection([
        ('yes', 'يأرشف'),
        ('no', 'لايأرشف'),
        ('no_selected', 'غير محدد'),

    ],default='no_selected',
        string='يأرشف/لايأرشف')


    publish = fields.Selection([
        ('yes', 'ينشر'),
        ('no', 'لا ينشر'),
        ('no_selected', 'غير محدد'),

    ],default='no_selected',string='ينشر/لا ينشر')

    send_or_not = fields.Selection([
        ('yes', 'يرسل'),
        ('no', 'لا يرسل'),
        ('no_selected', 'غير محدد'),

    ], default='no_selected',
        string='يأرشف/لايأرشف')

    choices_fatwa=fields.Boolean('فتوى مختارة')
    send= fields.Boolean  (string='لا يرسل',)
    for_study = fields.Boolean('للدراسة')
    refuse = fields.Boolean(' مرفوض')
    save_order=fields.Boolean('حجز الطلب')
    fatwa_saves = fields.Boolean('الى المحفوظات')
    fatwa_new_source_id=fields.Many2one('fatwa.source',default=_get_fatwa_source,string='مصدر الفتوى')
    # fatwa_new_source_id=fields.Many2one('fatwa.source',string='مصدر الفتوى')
    ticket_type_id = fields.Many2one('helpdesk.ticket.type', string="نوع السؤال",default=_get_ticket_type,)
    department_ids=fields.Many2many('fatwa.department',default=_get_fatwa_department,string='التصنيف')




    def button_receive(self):
        self.write({'state':'receive'})

    def button_resolution(self):
        self.write({'state': 'resolution'})

    def button_to_treat(self):
        self.write({'state':'to_treat'})

    def button_fatwa(self):
        self.write({'state':'fatwa'})

    def button_studying(self):
        self.write({'state':'studying'})

    # def button_close(self):
    #     self.write({'state':'close'})

    # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

    def button_fake(self):
        self.write({'state':'fake'})

    def button_repeated(self):
        self.write({'state':'repeated'})

    def button_reserved(self):
        self.write({'state':'reserved'})

    def button_urgent(self):
        self.write({'state':'urgent'})

    def button_edit(self):
        self.write({'state':'edit'})

    def button_choiced(self):
        self.write({'state':'choiced'})

    def button_refused(self):
        self.write({'state':'refused'})

    def button_saved(self):
        self.write({'state':'saved'})







    @api.model
    def create(self, vals):
        if vals.get('seq', 'New') == 'New':
            vals['seq'] = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or 'New'


        return super(fatwa, self).create(vals)

    question_status_id = fields.Many2one('question.status', string='حالة السوال')
    priority_value = fields.Char(compute='get_priority_value')
    ticket_id = fields.Many2one('helpdesk.ticket', string='السؤال الاصلى قبل تنقيحات المراجع',domain="[('active','=',False)]")
    ticket_ids = fields.Many2many('helpdesk.ticket', 'relation_helpdesk', 'helpd_column1', 'helpd_column1_column2',
                                  string='Grade Category',domain="[('active','=',False)]")
    partner_phone = fields.Char('واتساب المستفتى')
    fatwa_links = fields.Char('رابط الفتوى الصوتية')
    shot_name_id=fields.Many2one('shortcut.page',string='نصوص مختصرة')
    priority = fields.Selection(TICKET_PRIORITY, string='Priority', default='2')

    def button_up(self):
        if self.fatwa_replay:
            self.fatwa_replay = '\n\n' + self.shot_name_id.name + '\n\n' +  '\n\n' +self.fatwa_replay
        else:

            self.fatwa_replay = self.shot_name_id.name + '\n\n'

    def button_down(self):
        if self.fatwa_replay:
            self.fatwa_replay = self.fatwa_replay + '\n\n' + self.shot_name_id.name
        else:

            self.fatwa_replay = self.shot_name_id + '\n\n'

    @api.onchange('partner_id')
    def get_customer_phone(self):
        if self.partner_id:
            self.partner_phone = self.partner_id.mobile

    @api.depends('priority')
    def get_priority_value(self):
        for rec in self:
            rec.priority_value = dict(rec._fields['priority'].selection).get(rec.priority)



    def onchange_stage_id(self):
        for rec in self:
            rec.activity_schedule('fatwa.schdule_activity_helpdesk',
                                  user_id=rec.user_id.id,
                                  note='تم تحريك هذه الفتوه الى ' + ' ' + str(rec.stage_id.name) + str(
                                  ) + '.<br/>')
            print("aaaaaaa", rec.message_ids)

    def confirm_mail(self):
        ir_model_data = self.env['ir.model.data']
        template_res = self.env['mail.template']
        template_id = ir_model_data.get_object_reference('fatwa', 'medical_email_30_template')[1]

        template = template_res.browse(template_id)
        for rec in self:
            email_values = {
                'email_to': rec.partner_id.email,
                'email_from': rec.company_id.email,
                'subject': 'الرد على السوال',
            }

            template.body_html = '<p>عزيزى المستفتى  ${(object.partner_id.name)},''<br/><br/>  نود ابلاغ حضرتكم بانه تم الاجابه على  الفتوة رقم' + ' ' + str(
                rec.name) + ' سوال بعنوان  . <br/><br/>' + ' ' + str(rec.description) + ' والاجابة هى . <br/><br/>' \
                                 + str(rec.fatwa_replay) + '  '  'شكرا جزيلا,<br/>' \
                                                           '${(object.company_id.name)}'

            template.send_mail(rec.id, force_send=True, email_values=email_values)

    


class question(models.Model):
    _name = 'question.status'
    _rec_name = 'name'

    name = fields.Char('خالة السؤال',required=1)

class question_channal(models.Model):
    _name = 'question.channel'
    _rec_name = 'name'

    name = fields.Char('قناة وصول السؤال',required=1)
class sender(models.Model):
    _name = 'sender.type'

    name = fields.Char(string='الراسل' , required=True )


    _sql_constraints = [
        ('name_uniq', 'unique (name)', "هذا الراسل موجود بالفعل !"),
    ]


class shortcust(models.Model):
    _name = 'shortcut.page'

    name=fields.Char('المختصر')
