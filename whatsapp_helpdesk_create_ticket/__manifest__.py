# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'whatsApp Helpdesk Ticket',
    'version': '13.0.0.0.0',
    'category': 'Operations/Helpdesk',
    'summary': 'Track help tickets',
    'depends': ['base_setup', 'helpdesk'],
    'description': """
whatsApp Helpdesk Ticket  Management App
========================================
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/send_wp_msg_views.xml',
        # 'data/whatsapp_templates_data.xml',
        'views/helpdesk_views.xml',
        'views/res_config_settings_views.xml',
        'views/whatsapp_templates_view.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
