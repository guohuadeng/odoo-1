# -*- coding: utf-8 -*-
from odoo import http

# class Paracenter(http.Controller):
#     @http.route('/paracenter/paracenter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/paracenter/paracenter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('paracenter.listing', {
#             'root': '/paracenter/paracenter',
#             'objects': http.request.env['paracenter.paracenter'].search([]),
#         })

#     @http.route('/paracenter/paracenter/objects/<model("paracenter.paracenter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('paracenter.object', {
#             'object': obj
#         })