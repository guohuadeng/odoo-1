# -*- coding: utf-8 -*-
from odoo import http

# class BoyueSaleExtend(http.Controller):
#     @http.route('/boyue_sale_extend/boyue_sale_extend/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/boyue_sale_extend/boyue_sale_extend/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('boyue_sale_extend.listing', {
#             'root': '/boyue_sale_extend/boyue_sale_extend',
#             'objects': http.request.env['boyue_sale_extend.boyue_sale_extend'].search([]),
#         })

#     @http.route('/boyue_sale_extend/boyue_sale_extend/objects/<model("boyue_sale_extend.boyue_sale_extend"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('boyue_sale_extend.object', {
#             'object': obj
#         })