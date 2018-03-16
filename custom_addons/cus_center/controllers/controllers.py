# -*- coding: utf-8 -*-
from odoo import http

# class CusCenter(http.Controller):
#     @http.route('/cus_center/cus_center/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cus_center/cus_center/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cus_center.listing', {
#             'root': '/cus_center/cus_center',
#             'objects': http.request.env['cus_center.cus_center'].search([]),
#         })

#     @http.route('/cus_center/cus_center/objects/<model("cus_center.cus_center"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cus_center.object', {
#             'object': obj
#         })