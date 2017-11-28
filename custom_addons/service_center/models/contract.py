# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleContractManage(models.Model):
    _inherit = 'contract.sale_contract'

    @api.multi
    def create_work_sheet(self):
        """创建工作单"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Work Sheet'),
            'res_model': 'work_sheet',
            'view_mode': 'form, tree',
            'view_type': 'form',
            'nodestory': True,
            'target': 'current'
        }