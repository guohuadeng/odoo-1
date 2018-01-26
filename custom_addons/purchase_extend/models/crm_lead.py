# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Lead(models.Model):
    _inherit = 'crm.lead'

    purchase_order_ids = fields.One2many(comodel_name="purchase.order", inverse_name="crm_lead_id", string="Purchase Order", )
    purchase_order_nums = fields.Integer(string="PO Nums", compute='_get_purchase_orders_nums')

    @api.multi
    def pop_purchase_order(self):
        """弹出新建询价单界面"""

        ctx = {
            'default_sale_person_id': self.user_id.id,
            'default_crm_lead_id': self.id,
            'default_customer_service_id': self.env.uid,
            'lead_id': self.id
        }

        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Order'),
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'context': ctx
        }

    @api.multi
    @api.depends('purchase_order_ids')
    def _get_purchase_orders_nums(self):
        """得到采购订单数"""

        for obj in self:
            print('------------------the nums:', len(obj.purchase_order_ids))
            obj.purchase_order_nums = len(obj.purchase_order_ids)