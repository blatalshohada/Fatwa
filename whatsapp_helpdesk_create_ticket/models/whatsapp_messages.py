from odoo import fields, models

class WhatsappMessages(models.Model):
    _name = 'whatsapp.messages'
    _description = "Whatsapp Messages"
    _order = 'time desc'

    name = fields.Char('Name', readonly=True, help='Whatsapp message')
    message_body = fields.Text('الرسالة', readonly=True, help='If whatsapp message have caption (for image,video,document) else add message body')
    message_id = fields.Text('Message Id', readonly=True, help='Whatsapp Message id')
    senderName = fields.Char('إسم الراسل', readonly=True, help='If message is coming then it contains name sender '
                                                                'else if message is sending from odoo then name/mobile of sender which has current instance attached')
    to = fields.Char('المرسل إليه', readonly=True)
    time = fields.Datetime('التاريخ', readonly=True, help='Time on which message is sent or receive')
    state = fields.Selection([('sent', 'Sent'), ('received', 'Received')], string='الحالة', readonly=True, help="It is based on message is sent or receive")
    helpdesk_id = fields.Many2one('helpdesk.ticket', 'Help Desk')
    whatsapp_message_provider = fields.Char(string="Whatsapp Service Provider",help='Whatsapp provider on which message is sent or received')

