# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp

class ConsignorConsigneeType(models.Model):
    _name = 'purchase_extend.consignor_nee_type'
    _rec_name = 'name'
    _description = 'Consignor Consignee Type'

    name = fields.Char(string='Name', )
    description = fields.Text(string="Description", required=False, )


class OrderDeliveryInfo(models.Model):
    _name = 'purchase.order_delivery_info'
    _rec_name = 'name'
    _description = 'Order Delivery Info'

    type_id = fields.Many2one(comodel_name="purchase_extend.consignor_nee_type", string="Type", required=False, )
    name = fields.Char(string='Name', required=True)
    address = fields.Char(string="Address", required=False, )
    qty = fields.Integer(string="Qty", required=False, )
    wrap_type_id = fields.Many2one(comodel_name="delegate_packing", string="Wrap Type", required=False, )
    gross_weight = fields.Float(string="Gross Quantity",  required=False, digits=dp.get_precision('Stock Weight'))
    remark = fields.Text(string="Remark", required=False, )
    purchase_order_id = fields.Many2one(comodel_name="purchase.service_quote_order", string="Purchase Order", required=False, )
    sequence = fields.Integer(string='Sequence', default=10)



