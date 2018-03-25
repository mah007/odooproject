# -*- coding: utf-8 -*-
from odoo import http

# class Mapps(http.Controller):
#     @http.route('/mapps/mapps/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mapps/mapps/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mapps.listing', {
#             'root': '/mapps/mapps',
#             'objects': http.request.env['mapps.mapps'].search([]),
#         })

#     @http.route('/mapps/mapps/objects/<model("mapps.mapps"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mapps.object', {
#             'object': obj
#         })