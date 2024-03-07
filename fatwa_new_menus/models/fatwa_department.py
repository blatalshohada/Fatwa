from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

class FatwaDepartment(models.Model):
    _name = "fatwa.department"
    _description = "Fatwa Department"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Name', index=True, required=True)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',
        store=True)
    parent_id = fields.Many2one('fatwa.department', 'Parent Department', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('fatwa.department', 'parent_id', 'Child Departments')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for department in self:
            if department.parent_id:
                department.complete_name = '%s / %s' % (department.parent_id.complete_name, department.name)
            else:
                department.complete_name = department.name

    @api.constrains('parent_id')
    def _check_department_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive departments.'))
        return True

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]
