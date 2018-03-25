# -*- coding: utf-8 -*-
from odoo import http

# class Map2(http.Controller):
#     @http.route('/map2/map2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/map2/map2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('map2.listing', {
#             'root': '/map2/map2',
#             'objects': http.request.env['map2.map2'].search([]),
#         })

#     @http.route('/map2/map2/objects/<model("map2.map2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('map2.object', {
#             'object': obj
#         })