# -*- coding: utf-8 -*-
# module template
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'fatwa email',
    'depends': ['base','helpdesk','helpdesk_ticket_reports','fatwa'     ],
    'data': [
           'views/views.xml',
           'views/new_mail_message_cron.xml'
            ],
    'installable': True,
    'application': True,
}
