# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleContract(models.Model):
    _inherit = 'contract.sale_contract'

    @api.model
    def create(self, vals):
        """覆盖合同的创建方法，重写合同名生成规则"""
        result = super(SaleContract, self).create(vals)
        name = result.name
        result.name = self.env.user.company_id.company_code + '-' + name[0:4] + result.contract_type.code +name[4:]
        return result
