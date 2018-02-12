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


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.onchange('template_id')
    def onchange_template_id(self):
        if not self.template_id:
            return
        template = self.template_id.with_context(lang=self.partner_id.lang)

        order_lines = [(5, 0, 0)]
        for line in template.quote_line:
            # if self.pricelist_id:
            #     price = self.pricelist_id.with_context(uom=line.product_uom_id.id).get_product_price(line.product_id, 1, False)
            # else:
            price = line.quote_price_unit / line.rate         # 废掉价格表功能

            data = {
                'name': line.name,
                'price_unit': price,
                'discount': line.discount,
                'product_uom_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                'quote_currency_id': line.product_id.currency_id,    # 把产品的货币带到询价货币中去
                'quote_price_unit': line.quote_price_unit,      # 当产品发生改变时，报价单价也要发生改变
                'layout_category_id': line.layout_category_id,
                'product_uom': line.product_uom_id.id,
                'website_description': line.website_description,
                'state': 'draft',
                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
            }
            # if self.pricelist_id:
            #     data.update(self.env['sale.order.line']._get_purchase_price(self.pricelist_id, line.product_id, line.product_uom_id, fields.Date.context_today(self)))
            order_lines.append((0, 0, data))

        self.order_line = order_lines
        self.order_line._compute_tax_id()

        option_lines = []
        for option in template.options:
            # if self.pricelist_id:
            #     price = self.pricelist_id.with_context(uom=option.uom_id.id).get_product_price(option.product_id, 1, False)
            # else:
            price = line.quote_price_unit / line.rate         # 废掉价格表功能
            data = {
                'product_id': option.product_id.id,
                'layout_category_id': option.layout_category_id,
                'name': option.name,
                'quantity': option.quantity,
                'uom_id': option.uom_id.id,
                'price_unit': price,
                'discount': option.discount,
                'website_description': option.website_description,
            }
            option_lines.append((0, 0, data))
        self.options = option_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.to_string(datetime.now() + timedelta(template.number_of_days))

        self.website_description = template.website_description
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note
