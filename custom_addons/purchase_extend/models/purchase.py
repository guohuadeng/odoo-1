# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


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
    goods_name = fields.Char(string="Goods Name", required=False, )         # 货物名称
    remarks = fields.Text(string="Remarks", required=False, )               # 备注
    goods_attribute_id = fields.Many2one(comodel_name="goods_attribute", string="Goods Type", required=False, )
    crm_lead_id = fields.Many2one(comodel_name="crm.lead", string="Lead", )     # 商机线索
    loading_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Loading Port",)     # 起运港
    transition_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Transition Port",)   # 中转港
    destination_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Destination Port",) # 目的港
    qty = fields.Integer(string="Qty")      # 件数
    packing_id = fields.Many2one(comodel_name="delegate_packing", string="Pack")        # 包装方式
    delivery_info_id = fields.One2many(comodel_name="purchase.order_delivery_info", inverse_name="purchase_order_id", string="Delivery Info", required=False, )
    is_service = fields.Boolean(string="Service")           # 标志采购单是服务或是辅材
    contract_id = fields.Many2one(comodel_name="purchase_extend.contract", string="Contract", required=False, )
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('confirm', _('Confirm')),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')

    @api.model
    def create(self, vals):
        result = super(PurchaseOrder, self).create(vals)
        user_ids = [vals.get('customer_service_id'), vals.get('sale_person_id')]
        user_ids = [item for item in user_ids if item]
        if user_ids:
            users = self.env['res.users'].search([('id', 'in', user_ids)])
            result.message_subscribe_users(users.ids, subtype_ids=[])
        return result

    @api.multi
    def confirm_price(self):
        """确认报价"""
        self.write({'state': 'confirm'})

        return True

    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'confirm']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    purchase_price_unit = fields.Float(string="Purchase Price",  required=False, )
    purchase_currency_id = fields.Many2one(comodel_name="res.currency", string="Purchase Currency", required=False, )
    rate = fields.Float(string="Rate",  related='purchase_currency_id.rate' )
    tag_ids = fields.Many2one(comodel_name="purchase.order_tag", string="Tag", required=False, )

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


class OrderTag(models.Model):
    _name = 'purchase.order_tag'
    _rec_name = 'name'
    _description = 'Purchase Order Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string="Color Index",)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class OrderLineTag(models.Model):
    _name = 'purchase.order_line_tag'
    _rec_name = 'name'
    _description = 'Service Item Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string="Color Index", required=False, )


class ContractWizard(models.TransientModel):
    _name = 'purchase_extend.contract_wizard'
    _description = 'Purchase Contract'

    contract_type_id = fields.Many2one(comodel_name="purchase_extend.contract_type", string="Type", required=True, )
    our_signatory_id = fields.Many2one(comodel_name="res.users", string="Our Signatory",)
    customer_signatory_id = fields.Many2one(comodel_name="res.partner", string="Customer signatory",
                                         required=True)  # 客户签约人
    supplier_order_no = fields.Char(string="SupplierQuoteOrderNo", required=False, )
    supplier_id = fields.Many2one(comodel_name="res.partner", string="Supplier", domain="[('supplier', '=', True)]")
    sign_date = fields.Date(string="Create Date", required=False, )
    effective_date = fields.Date(string="Effective Date", required=False, )
    failure_date = fields.Date(string="Failure Date", required=False, )
    remark = fields.Text(string="Remark", required=False, )

    create_contract_select = fields.Selection(string="Select Contract",
                                        selection=[('create', 'Create Contract'), ('selecte', 'Selecte Contract'), ],
                                        default='create')
    selected_contract_id = fields.Many2one(comodel_name="purchase_extend.contract", string="Selecte Contract", required=False, )

    @api.multi
    def create_contract(self):
        """生成合同"""
        order = self.env['purchase.order'].browse(self._context.get('purchase_order'))
        print(order)

        vals = {
            'supplier_id': self.supplier_id.id,
            'contract_type_id': self.contract_type_id.id,
            'customer_signatory_id': self.customer_signatory_id.id,
            'our_signatory_id': self.our_signatory_id.id,
            'supplier_order_no': self.supplier_order_no,
            'sign_date': self.sign_date,
            'effective_date': self.effective_date,
            'failure_date': self.failure_date,
            'remark': self.remark
        }

        contract = self.env["purchase_extend.contract"].create(vals)
        print(contract)
        order.write({'contract_id': contract.id})

        return True

    @api.multi
    def choose_contract(self):
        """选择合同"""
        if not self.selected_contract_id:
            raise UserError(_('Please select contract'))
        order = self.env['sale.order'].browse(self._context.get('purchase_order'))
        # order.write({'contract': self.selected_contract.id, 'state': 'sale'})
        order.write({'contract_id': self.selected_contract_id.id, })

        return True

