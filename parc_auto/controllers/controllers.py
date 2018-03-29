# -*- coding: utf-8 -*-
from odoo import http

# class ParcAuto(http.Controller):
#     @http.route('/parc_auto/parc_auto/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/parc_auto/parc_auto/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('parc_auto.listing', {
#             'root': '/parc_auto/parc_auto',
#             'objects': http.request.env['parc_auto.parc_auto'].search([]),
#         })

#     @http.route('/parc_auto/parc_auto/objects/<model("parc_auto.parc_auto"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('parc_auto.object', {
#             'object': obj
#         })