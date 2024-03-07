from odoo import _, api, models,fields

class LessonType(models.Model):
    _name = 'lesson.type'
    _rec_name='name'
    name=fields.Char(required=1)

class PriorityLevel(models.Model):
    _name = 'priority.level'
    _rec_name='name'
    name=fields.Char(required=1)

class Witnestype(models.Model):
    _name = 'witness.type'
    _rec_name='name'
    name=fields.Char(required=1)

class Certification(models.Model):
    _name = 'certificates.specialty'
    _rec_name='name'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, track_visibility='onchange', index=True,
                       default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', readonly=True, track_visibility='onchange',
                                 track_sequence=3, default=lambda self: self.env.company)

    certificate_name=fields.Char()
    certificate_title=fields.Char('Certificate title')
    description=fields.Char('Certificate text')
    certificates_specialists=fields.Char('Certification specialty')
    witness_type_id=fields.Many2one('witness.type',string='Witness type')
    witness_name_id=fields.Many2one('res.partner',string='Witness name')
    date=fields.Date('تاريخ التقرير او الشهادة')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] =  self.env['ir.sequence'].next_by_code('certificates.specialty') or '/'
        return super(Certification, self).create(vals)


class LessonLeaned(models.Model):
    _name = 'lessons.learned.from'
    _rec_name='name'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, track_visibility='onchange', index=True,
                       default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', readonly=True, track_visibility='onchange',
                                 track_sequence=3, default=lambda self: self.env.company)

    lesson_name=fields.Char('Lesson Title')
    lesson_type_id = fields.Many2one('lesson.type')
    priority_level=fields.Many2one('priority.level')
    description=fields.Char()
    corrective_action=fields.Char()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('lessons.learned.from') or '/'
        return super(LessonLeaned, self).create(vals)


class Fatwaextrapolation(models.Model):
    _name = 'fatwa.extrapolation'
    _rec_name='name'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, track_visibility='onchange', index=True,
                       default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', readonly=True, track_visibility='onchange',
                                 track_sequence=3, default=lambda self: self.env.company)
    note_title=fields.Char('عنوان الملاحظة')
    priority_level=fields.Many2one('priority.level','درجة الاهمية')
    description = fields.Char('الوصف')
    note_type=fields.Char('نوع الملاحظة')
    note_effect=fields.Char('اثر الملاحظة')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fatwa.extrapolation') or '/'
        return super(Fatwaextrapolation, self).create(vals)
class PreviousNext(models.Model):
    _name = 'previous.next.store'
    _rec_name='name'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, track_visibility='onchange', index=True,
                       default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', readonly=True, track_visibility='onchange',
                                 track_sequence=3, default=lambda self: self.env.company)

    description = fields.Char('الوصف')
    title=fields.Char('العنوان ')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('previous.next.store') or '/'
        return super(PreviousNext, self).create(vals)


# class FatwaDepartment(models.Model):
#     _name = 'fatwa.department'
#     _rec_name='name'

#     name = fields.Char(string='القسم', required=True)

#     _sql_constraints = [
#         ('name_uniq', 'unique (name)', "department name already exists !"),
#     ]


class fatwa(models.Model):
    _inherit = 'helpdesk.ticket'

    department_id=fields.Many2one('fatwa.department',string='اقسام الفتوى')
    department_tree_id = fields.Many2one('fatwa.department', string='إختيار التصنيف')
    department_ids=fields.Many2many('fatwa.department',string='التصنيف')

    def add_to_departments(self):
        self.ensure_one()
        if self.department_tree_id:
            self.department_ids = [(4, self.department_tree_id.id)]
            self.department_tree_id = False
