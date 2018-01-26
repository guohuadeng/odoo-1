# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    contact_id = fields.Many2one(comodel_name="res.partner", string="Contact", required=False,
                                 domain=[('customer', '=', True), ('is_company', '=', False)])
    business_type_id = fields.Many2one(comodel_name="business_type", string="Business Type", required=False, )
    validity_date = fields.Datetime(string="Validity Date", required=False, )
    customer_service_id = fields.Many2one(comodel_name="res.users", string="Customer Service", required=False, )
    sale_person_id = fields.Many2one(comodel_name="res.users", string="Sale Person", required=False, )
    departure_place = fields.Char(string="Departure Place", required=False, )
    destination_place = fields.Char(string="Destination Place", required=False, )
    customs_id = fields.Many2one(comodel_name="delegate_customs", string="Customs", required=False, )
    goods_name = fields.Char(string="Goods Name", required=False, )
    remarks = fields.Text(string="Remarks", required=False, )
    goods_attribute = fields.Many2one(comodel_name="goods_attribute", string="Goods Type", required=False, )
    crm_lead_id = fields.Many2one(comodel_name="crm.lead", string="Lead", )

    @api.model
    def create(self, vals):
        result = super(PurchaseOrder, self).create(vals)
        user_ids = [vals.get('customer_service_id'), vals.get('sale_person_id')]
        user_ids = [item for item in user_ids if item]
        if user_ids:
            users = self.env['res.users'].search([('id', 'in', user_ids)])
            result.message_subscribe_users(users.ids, subtype_ids=[])
        return result

    @api.model
    def _change_sale_person(self):
        """当供应商改变时"""



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    purchase_price_unit = fields.Float(string="Purchase Price",  required=False, )
    purchase_currency_id = fields.Many2one(comodel_name="res.currency", string="Purchase Currency", required=False, )
    rate = fields.Float(string="Rate",  related='purchase_currency_id.rate' )

    @api.onchange('rate', 'purchase_price_unit')
    def _compute_price_unit(self):
        """根据汇率计算单价"""
        if self.rate != 0:
            self.price_unit = self.purchase_price_unit / self.rate

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = super(PurchaseOrderLine, self).onchange_product_id()
        self.purchase_price_unit = 0.0
        self.purchase_currency_id = self.product_id.currency_id
        return result
