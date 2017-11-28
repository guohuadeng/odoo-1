# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    business_type = fields.Many2many(comodel_name="business_type", string="Business Type", )
