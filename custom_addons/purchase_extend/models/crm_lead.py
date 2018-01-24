# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Lead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def pop_purchase_order(self):
        """弹出新建询价单界面"""

        ctx = {
            'default_sale_person_id': self.user_id,
        }

        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Order'),
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'view_type': 'form',
            'nodestory': True,
            'target': 'new',
            'context': ctx
        }
