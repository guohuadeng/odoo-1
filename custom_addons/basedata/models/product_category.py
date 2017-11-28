# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    @api.multi
    def unlink(self):
        rec = [self.env.ref('basedata.product_category_service_fees').id,
               self.env.ref('basedata.product_category_materials').id]
        # rec = []
        for cat in self:
            if cat.id in rec:
                raise UserError(_("you can't delete this root category"))
        return super(ProductCategory, self).unlink()

    @api.multi
    def write(self, vals):
        rec = [self.env.ref('basedata.product_category_service_fees').id,
               self.env.ref('basedata.product_category_materials').id]
        # rec = []
        for cat in self:
            if cat.id in rec:
                raise UserError(_("you can't modify this root category"))
        return super(ProductCategory, self).write(vals)