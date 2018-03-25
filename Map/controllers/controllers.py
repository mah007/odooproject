# -*- coding: utf-8 -*-
from odoo import http

# class Map(http.Controller):
#     @http.route('/map/map/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/map/map/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('map.listing', {
#             'root': '/map/map',
#             'objects': http.request.env['map.map'].search([]),
#         })

#     @http.route('/map/map/objects/<model("map.map"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('map.object', {
#             'object': obj
#         })