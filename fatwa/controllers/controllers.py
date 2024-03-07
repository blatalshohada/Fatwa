# # -*- coding: utf-8 -*-
# from odoo import http

# class Fatwa(http.Controller):
    
#     @http.route("/landing/<id>", type='json', auth='public', methods=['GET', 'POST'], website=True)
#     def landing(self, id, **kw):
#         #kw.get('start_date')
#         results = {'actions': [91,72,13,44,52,60] }
#         return http.request.render("odoo_controller.view_helpdesk_team_custom", results)
        
#     @http.route('/fatwa/fatwa', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fatwa/fatwa/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fatwa.listing', {
#             'root': '/fatwa/fatwa',
#             'objects': http.request.env['fatwa.fatwa'].search([]),
#         })

#     @http.route('/fatwa/fatwa/objects/<model("fatwa.fatwa"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fatwa.object', {
#             'object': obj
#         })
