from odoo import fields, models, api
from odoo.exceptions import ValidationError


class WhatsappTemplates(models.Model):
    _name = 'whatsapp.templates'
    _description = 'Whatsapp Template'

    name = fields.Selection([('new_ticket', 'New Ticket'), ('ticket_in_progress', 'Ticket In Progress'), ('ticket_in_solved', 'Ticket In Solved'), ('ticket_in_cancelled', 'Ticket In Cancelled')], string="إسم الرسالة", requird= True)
    message_content = fields.Text(string='محتوى الرسالة', required=True)

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            selection_value = dict(self._fields['name'].selection).get(record.name)
            if selection_value:
                name = selection_value
            result.append((record.id, name))
        return result

    @api.constrains('name')
    def _check_unique_selection_keys(self):
        for record in self:
            count = self.env['whatsapp.templates'].search_count([('name', '=', record.name)])
            if count > 1:
                raise ValidationError(f"Only one record allowed in one selection key.")



