# -*- coding: utf-8 -*-
from odoo import http

# class InterVehicule(http.Controller):
#     @http.route('/inter_vehicule/inter_vehicule/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inter_vehicule/inter_vehicule/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inter_vehicule.listing', {
#             'root': '/inter_vehicule/inter_vehicule',
#             'objects': http.request.env['inter_vehicule.inter_vehicule'].search([]),
#         })

#     @http.route('/inter_vehicule/inter_vehicule/objects/<model("inter_vehicule.inter_vehicule"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inter_vehicule.object', {
#             'object': obj
#         })