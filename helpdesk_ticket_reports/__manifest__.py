# -*- coding: utf-8 -*-
# module template
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Helpdesk Ticket Reports',
    'version': '13.0',

    'depends': ['base','helpdesk','fatwa'],
    'data': [
           'security/ir.model.access.csv',
        'views/helpdesk_view.xml',
        'wizard/helpdesk_wizard_report1.xml',
        'views/helpdesk_report1.xml',



             ],
    'installable': True,
    'application': True,
}
