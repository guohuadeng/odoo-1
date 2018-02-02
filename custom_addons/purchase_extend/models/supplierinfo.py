# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SuppliferInfo(models.Model):
    _inherit = 'product.supplierinfo'

    purchase_currency_id = fields.Many2one(comodel_name="res.currency", string="Purchase Currency", required=False, )
    tag_ids = fields.Many2one(comodel_name="purchase.order_tag", string="Tag", required=False, )

