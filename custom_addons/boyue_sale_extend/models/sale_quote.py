# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta


class SaleQuoteLine(models.Model):
    _inherit = 'sale.quote.line'

    quote_price_unit = fields.Float(string="Quoto Price Unit",  required=True, )
    quote_currency_id = fields.Many2one(comodel_name="res.currency", string="Quote Currency", required=True,)  # 报价币种
    rate = fields.Float(string="Rate", related='quote_currency_id.rate',  required=False, )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.ensure_one()
        if self.product_id:
            name = self.product_id.name_get()[0][1]
            if self.product_id.description_sale:
                name += '\n' + self.product_id.description_sale
            self.name = name
            self.price_unit = self.product_id.lst_price
            self.product_uom_id = self.product_id.uom_id.id
            self.website_description = self.product_id.quote_description or self.product_id.website_description or ''
            self.quote_currency_id = self.product_id.currency_id.id      # 加入币种
            self.quote_price_unit = self.product_id.list_price * self.rate      # 改变报价单价
            domain = {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
            return {'domain': domain}

    @api.onchange('rate', 'quote_price_unit')
    def _compute_price_unit(self):
        """根据所选币种的汇率计算出当前单价"""
        if self.rate != 0:
            self.price_unit = self.quote_price_unit / self.rate

