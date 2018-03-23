# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
#
#     contact_id = fields.Many2one(comodel_name="res.partner", string="Contact", required=False,
#                                  domain=[('customer', '=', True), ('is_company', '=', False)])
#     business_type_id = fields.Many2one(comodel_name="business_type", string="Business Type", required=False, )
#     validity_date = fields.Datetime(string="Validity Date", required=False, )
#     customer_service_id = fields.Many2one(comodel_name="res.users", string="Customer Service", required=False, )
#     sale_person_id = fields.Many2one(comodel_name="res.users", string="Sale Person", required=False, )
#     departure_place = fields.Char(string="Departure Place", required=False, )
#     destination_place = fields.Char(string="Destination Place", required=False, )
#     customs_id = fields.Many2one(comodel_name="delegate_customs", string="Customs", required=False, )
#     goods_name = fields.Char(string="Goods Name", required=False, )         # 货物名称
#     remarks = fields.Text(string="Remarks", required=False, )               # 备注
#     goods_attribute_id = fields.Many2one(comodel_name="goods_attribute", string="Goods Type", required=False, )
#     crm_lead_id = fields.Many2one(comodel_name="crm.lead", string="Lead", )     # 商机线索
#     loading_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Loading Port",)     # 起运港
#     transition_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Transition Port",)   # 中转港
#     destination_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Destination Port",) # 目的港
#     qty = fields.Integer(string="Qty")      # 件数
#     packing_id = fields.Many2one(comodel_name="delegate_packing", string="Pack")        # 包装方式
#     delivery_info_id = fields.One2many(comodel_name="purchase.order_delivery_info", inverse_name="purchase_order_id", string="Delivery Info", required=False, )
#     is_service = fields.Boolean(string="Service")           # 标志采购单是服务或是辅材
#     contract_id = fields.Many2one(comodel_name="purchase_extend.contract", string="Contract", required=False, )
#     state = fields.Selection([
#         ('draft', 'RFQ'),
#         ('sent', 'RFQ Sent'),
#         ('confirm', _('Confirm')),
#         ('to approve', 'To Approve'),
#         ('purchase', 'Purchase Order'),
#         ('done', 'Locked'),
#         ('cancel', 'Cancelled')
#         ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
#
#     @api.model
#     def create(self, vals):
#         result = super(PurchaseOrder, self).create(vals)
#         user_ids = [vals.get('customer_service_id'), vals.get('sale_person_id')]
#         user_ids = [item for item in user_ids if item]
#         if user_ids:
#             users = self.env['res.users'].search([('id', 'in', user_ids)])
#             result.message_subscribe_users(users.ids, subtype_ids=[])
#         return result
#
#     @api.multi
#     def confirm_price(self):
#         """确认报价"""
#         self.write({'state': 'confirm'})
#
#         return True
#
#     @api.multi
#     def button_confirm(self):
#         for order in self:
#             if order.state not in ['draft', 'sent', 'confirm']:
#                 continue
#             order._add_supplier_to_product()
#             # Deal with double validation process
#             if order.company_id.po_double_validation == 'one_step'\
#                     or (order.company_id.po_double_validation == 'two_step'\
#                         and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id))\
#                     or order.user_has_groups('purchase.group_purchase_manager'):
#                 order.button_approve()
#             else:
#                 order.write({'state': 'to approve'})
#         return True


class ServiceQuoteOrder(models.Model):
    """服务询价单"""
    _name = 'purchase.service_quote_order'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Service Order'

    name = fields.Char(string="Quotation Num", index=True, copy=False, default='New')
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, track_visibility='always')  # 供应商
    contact_id = fields.Many2one(comodel_name="res.partner", string="Contact", required=False,
                                 domain=[('customer', '=', True), ('is_company', '=', False)])  # 供应商联系人
    contract_id = fields.Many2one(comodel_name="purchase_extend.contract", string="Contract", required=False, ) # 采购合同
    partner_ref = fields.Char('SupplierQuoteOrderNo', copy=False,\
            help="Reference of the sales order or bid sent by the vendor. "
                "It's used to do the matching when you receive the "
                "products as this reference is usually written on the "
                "delivery order sent by your vendor.")      # 供应商单号
    business_type_id = fields.Many2one(comodel_name="business_type", string="Business Type", required=False, ) # 业务类型
    crm_lead_id = fields.Many2one(comodel_name="crm.lead", string="Lead", )     # 商机线索
    # tags_ids = fields.Many2many(comodel_name="purchase.order_tag", string="Tags", )  # 标签
    quote_date = fields.Datetime(string="Quote Date", copy=False, index=True, default=fields.Datetime.now)  # 询价日期
    validity_date = fields.Datetime(string="Validity Date", copy=False)     # 有效日期
    customer_service_id = fields.Many2one(comodel_name="res.users", string="Customer Service", required=False, ) # 客服服务
    sale_person_id = fields.Many2one(comodel_name="res.users", string="Sale Person", required=False, )      # 销售
    payment_term_id = fields.Many2one('account.payment.term', 'Payment Terms')

    loading_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Loading Port",)     # 起运港
    transition_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Transition Port",)   # 中转港
    destination_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Destination Port",) # 目的港
    incoterm_id = fields.Many2one('stock.incoterms', 'Incoterm', help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    goods_attribute_id = fields.Many2one(comodel_name="goods_attribute", string="Goods Type", required=False, )
    qty = fields.Integer(string="Qty")      # 件数
    packing_id = fields.Many2one(comodel_name="delegate_packing", string="Pack")        # 包装方式
    goods_name = fields.Text(string="Goods Name", required=False, )         # 货物名称
    remarks = fields.Text(string="Remarks", required=False, )               # 备注
    customs_ids = fields.Many2many(comodel_name="delegate_customs", string="Customs", )
    declare_customs_id = fields.Many2one(comodel_name="delegate_customs", string="Declare Customs", required=False, )
    delivery_info_id = fields.One2many(comodel_name="purchase.order_delivery_info", inverse_name="purchase_order_id",
                                       string="Delivery Info", required=False, )    # 收发货信息
    order_line = fields.One2many('purchase.service_quote_line', 'order_id', string='Order Lines', copy=True)
    notes = fields.Text('Terms and Conditions')     # 默认条款
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='always')     # 未含税金额
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')      # 含税金额
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')    # 总额
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position')
    state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('sent', 'Sent'),
                                                        ('comfired', 'Comfired'),
                                                        ('cancel', 'Cancel')], required=False,  default='draft')        # 状态
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)         # 公司货币单位
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.user.company_id.id)


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('service_quote_order') or '/'
        return super(ServiceQuoteOrder, self).create(vals)

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.multi
    def action_rfq_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('purchase_extend', 'email_template_edi_service_quote_order')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchase.service_quote_order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env['report'].get_action(self, 'purchase_extend.service_quotation_template')

    @api.multi
    def button_draft(self):
        self.write({'state': 'draft'})
        return True

    @api.multi
    def button_cancel(self):
        self.write({'state': 'cancel'})
        return True

    @api.multi
    def button_confirm(self):
        self.write({'state': 'comfired'})
        return True

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            self.fiscal_position_id = False
            self.payment_term_id = False
            self.currency_id = False
        else:
            self.fiscal_position_id = self.env['account.fiscal.position'].with_context(company_id=self.company_id.id).get_fiscal_position(self.partner_id.id)
            self.payment_term_id = self.partner_id.property_supplier_payment_term_id.id
            self.currency_id = self.partner_id.property_purchase_currency_id.id or self.env.user.company_id.currency_id.id
        return {}

#
# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
#
#     service_quote_id = fields.Many2one(comodel_name="purchase.service_quote_order", string="Service Quotation", required=False, )
#     purchase_price_unit = fields.Float(string="Purchase Price",  required=False, )
#     purchase_currency_id = fields.Many2one(comodel_name="res.currency", string="Purchase Currency", required=False, )
#     rate = fields.Float(string="Rate",  related='purchase_currency_id.rate' )
#     tag_ids = fields.Many2one(comodel_name="purchase.order_tag", string="Tag", required=False, )
#
#     @api.depends('product_qty', 'price_unit', 'taxes_id')
#     def _compute_amount(self):
#         if self.service_quote_id:
#             for line in self:
#                 taxes = line.taxes_id.compute_all(line.price_unit, line.service_quote_id .currency_id, line.product_qty, product=line.product_id, partner=line.service_quote_id.partner_id)
#                 line.update({
#                     'price_tax': taxes['total_included'] - taxes['total_excluded'],
#                     'price_total': taxes['total_included'],
#                     'price_subtotal': taxes['total_excluded'],
#                 })
#         else:
#             super(PurchaseOrderLine, self)._compute_amount()
#
    # @api.onchange('rate', 'purchase_price_unit', 'purchase_currency_id')
    # def _compute_price_unit(self):
    #     """根据汇率计算单价"""
    #     if self.rate != 0:
    #         self.price_unit = self.purchase_price_unit / self.rate
#
#     @api.onchange('product_id')
#     def onchange_product_id(self):
#         result = super(PurchaseOrderLine, self).onchange_product_id()
#         self.purchase_price_unit = 0.0
#         self.purchase_currency_id = self.product_id.currency_id
#         return result


class PurchaseOrderLine(models.Model):
    _name = 'purchase.service_quote_line'
    _description = 'Service Quotation Order Line'

    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


    purchase_price_unit = fields.Float(string="Purchase Price",  required=False, )
    purchase_currency_id = fields.Many2one(comodel_name="res.currency", string="Purchase Currency", required=False, )
    rate = fields.Float(string="Rate",  related='purchase_currency_id.rate' )

    name = fields.Text(string='Description', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    product_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True)
    taxes_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
    product_uom = fields.Many2one('product.uom', string='Product Unit of Measure', required=True)
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True, required=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Monetary(compute='_compute_amount', string='Tax', store=True)

    order_id = fields.Many2one('purchase.service_quote_order', string='Service Quotation', index=True, required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', related='order_id.company_id', string='Company', store=True, readonly=True)
    # state = fields.Selection(related='order_id.state', store=True)

    partner_id = fields.Many2one('res.partner', related='order_id.partner_id', string='Partner', readonly=True, store=True)
    currency_id = fields.Many2one(related='order_id.currency_id', store=True, string='Currency', readonly=True)
    date_order = fields.Datetime(related='order_id.quote_date', string='Order Date', readonly=True)



    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.price_unit = self.product_qty = 0.0
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        result['domain'] = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}

        product_lang = self.product_id.with_context({
            'lang': self.partner_id.lang,
            'partner_id': self.partner_id.id,
        })
        self.name = product_lang.display_name
        if product_lang.description_purchase:
            self.name += '\n' + product_lang.description_purchase

        fpos = self.order_id.fiscal_position_id
        if self.env.uid == SUPERUSER_ID:
            company_id = self.env.user.company_id.id
            self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id.filtered(lambda r: r.company_id.id == company_id))
        else:
            self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id)

        self.purchase_price_unit = 0.0
        self.purchase_currency_id = self.product_id.currency_id

        return result


    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        if not self.product_id:
            return

        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            uom_id=self.product_uom)

        if not seller:
            return

        price_unit = self.env['account.tax']._fix_tax_included_price(seller.price, self.product_id.supplier_taxes_id, self.taxes_id) if seller else 0.0
        if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
            price_unit = seller.currency_id.compute(price_unit, self.order_id.currency_id)

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit

    @api.onchange('rate', 'purchase_price_unit', 'purchase_currency_id')
    def _compute_price_unit(self):
        """根据汇率计算单价"""
        if self.rate != 0:
            self.price_unit = self.purchase_price_unit / self.rate



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
        order = self.env['purchase.service_quote_order'].browse(self._context.get('service_quote_order'))

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
        order.write({'contract_id': contract.id})

        return True

    @api.multi
    def choose_contract(self):
        """选择合同"""
        print('----------------------------- choose contract -----------------------------------')
        if not self.selected_contract_id:
            raise UserError(_('Please select contract'))
        order = self.env['purchase.service_quote_order'].browse(self._context.get('service_quote_order'))
        print(self._context.get('service_quote_order'))
        # order.write({'contract': self.selected_contract.id, 'state': 'sale'})
        order.write({'contract_id': self.selected_contract_id.id, })

        return True

    @api.multi
    @api.onchange('selected_contract_id')
    def _comput_contract(self):
        for item in self:
            if item.selected_contract_id:
                item.contract_type_id = item.selected_contract_id.contract_type_id
                item.our_signatory_id = item.selected_contract_id.our_signatory_id
                item.customer_signatory_id  = item.selected_contract_id.customer_signatory_id
                item.supplier_order_no = item.selected_contract_id.supplier_order_no
                item.supplier_id = item.selected_contract_id.supplier_id
                item.sign_date = item.selected_contract_id.sign_date
                item.effective_date = item.selected_contract_id.effective_date
                item.failure_date = item.selected_contract_id.failure_date
                item.remark = item.selected_contract_id.remark
