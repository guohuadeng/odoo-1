# -*- coding: utf-8 -*-
from odoo import http

# class CustomsClearance(http.Controller):
#     @http.route('/customs_clearance/customs_clearance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customs_clearance/customs_clearance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customs_clearance.listing', {
#             'root': '/customs_clearance/customs_clearance',
#             'objects': http.request.env['customs_clearance.customs_clearance'].search([]),
#         })

#     @http.route('/customs_clearance/customs_clearance/objects/<model("customs_clearance.customs_clearance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customs_clearance.object', {
#             'object': obj
#         })