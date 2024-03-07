# -*- coding: utf-8 -*-
{
    'name': "fatwa",

    'summary': """
        
        """,

    'description': """
        
    """,

    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' ,'helpdesk','fatwa_new_menus'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/quostion_status.xml',
        'views/helpdesk_view.xml',
        'views/email_data.xml',
        'data/sender_type_data.xml',
        'data/short_cut.xml',
        'views/fatwa_landing_page.xml',
        'views/fatwa_landing_page_buttons.xml',
        'views/fatwa_extend_menus.xml',
        'views/templates.xml',
        'views/fatwa_views.xml',
        'views/filter_menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
