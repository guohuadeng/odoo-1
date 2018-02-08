# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ContractType(models.Model):
    """合同类型"""
    _name = 'purchase_extend.contract_type'
    _rec_name = 'name'
    _description = 'Purchase Contract Type'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string="Code", )
    remarks = fields.Text(string="Remarks")


class PurchaseContract(models.Model):
    """采购合同"""
    _name = 'purchase_extend.contract'
    _rec_name = 'name'
    _description = 'Purchase Contract'

    name = fields.Char(string='Name')
    supplier_id = fields.Many2one(comodel_name="res.partner", string="Supplier", domain="[('supplier', '=', True)]")
    contract_type_id = fields.Many2one(comodel_name="purchase_extend.contract_type", string="Type", required=True, )
    customer_signatory_id = fields.Many2one(comodel_name="res.partner", string="Customer Signatory",
                                            domain="[('parent_id', '=', supplier_id.id), ('is_company', '=', False), ('type', '=', 'contact')]")
    our_signatory_id = fields.Many2one(comodel_name="res.users", string="Our Signatory",)
    supplier_order_no = fields.Char(string="SupplierQuoteOrderNo", required=False, )
    sign_date = fields.Date(string="Create Date", required=False, )
    effective_date = fields.Date(string="Effective Date", required=False, )
    failure_date = fields.Date(string="Failure Date", required=False, )
    remark = fields.Text(string="Remark", required=False, )

    @api.model
    def create(self, vals):
        """定义命名规则"""
        vals['name'] = self.env['ir.sequence'].next_by_code('purchase_contract')
        result = super(PurchaseContract, self).create(vals)
        return result
