# -*- coding: utf-8 -*-
# module template
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Fatwa Enhancement (new menus)',
    'version': '14.0',
    'depends': ['base','helpdesk' ],
    'data': [
        'security/ir.model.access.csv',
        'views/sequence.xml',
        'views/certificate.xml',
        'views/lesson_learned.xml',
        'views/fatwa_department.xml',
        'views/previous_next.xml',
        'views/fatwa.xml',
        'views/helpdesk.xml',

             ],
    'installable': True,
    'application': True,
}
