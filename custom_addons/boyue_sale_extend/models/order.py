# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError
import odoo.addons.decimal_precision as dp
from datetime import datetime, timedelta

class Order(models.Model):
    """继承销售订单，添加通关数据字段"""
    _inherit = 'sale.order'

    contract = fields.Many2one(comodel_name="contract.sale_contract", string="Contract", required=False, copy=False)
    business_type = fields.Many2one(comodel_name="business_type", string="Business Type", required=True, )
    contact = fields.Many2many(comodel_name="res.partner", string="Contact", required=False, copy=False)
    contact_id = fields.Many2one(comodel_name="res.partner", string="Contact", required=False, coyp=False)
    servicer = fields.Many2one(comodel_name="res.partner", string="Servicer")
    customer_service = fields.Many2one(comodel_name="res.users", string="customer service", index=True, track_visibility='always')
    goods_name = fields.Text(string="Goods Name", required=False, )
    delivery_info = fields.One2many(comodel_name="boyue_sale_extend.delivery_info", inverse_name="order",
                                    string="Delivery Info", )
    # partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='onchange')

    # 进出口类型
    # import_and_export = fields.Selection(
    #     [('i', '进口'), ('e', '出口')],
    #     '进出口类型',
    #     required=True
    # )
    # transport = fields.Many2one('delegate_transport_mode', string='Transport Mode')     # 运输方式
    # exemption = fields.Many2one('delegate_exemption', string='Exemption')               # 免征性质
    # trade_term = fields.Many2one('delegate_trade_terms', string='Trade Term')           # 成交方式
    port = fields.Many2one('delegate_port', string='Port')                              # 装货/指运港
    num = fields.Integer('Num')                     # 件数
    gross_weight = fields.Float('Gross Weight')     # 毛重
    # mark_code = fields.Char('Mark Code')            # 标记唛码
    remarks = fields.Text('Remarks')                # 备注

    customs = fields.Many2many(comodel_name="delegate_customs", string="Custom", )    # 进出口岸
    trade_mode = fields.Many2one('delegate_trade_mode', string='Trade Mode')         # 监管方式
    trade_country = fields.Many2one('delegate_country', string=' Country')         # 贸易国别
    goods_attribute_id = fields.Many2one(comodel_name="goods_attribute", string="Goods Type", )     # 货物类型
    origin_arrival_country = fields.Many2one('delegate_country', string='Nation')
    region = fields.Many2one('delegate_region', string='Region')
    packing = fields.Many2one('delegate_packing', string='Wrap Type')
    # net_weight = fields.Float('净重')

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        # ('signed', 'Signed Contract'),
        ('sale', 'Sales Order'),
        # ('sheet', 'Work Sheet'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    work_sheet_id = fields.One2many(comodel_name="work_sheet", inverse_name="sale_order_no", string="Work Sheet")
    work_sheet_count = fields.Integer(string="Work Sheet Count", compute='_count_work_sheet')

    # 去除复制的字段
    validity_date = fields.Date(string='Expiration Date', readonly=True, copy=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.")
    message_follower_ids = fields.One2many(
        'mail.followers', 'res_id', string='Followers', copy=False,
        domain=lambda self: [('res_model', '=', self._name)])
    load_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Loading Port")     # 起运港
    trans_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Transition Port") # 中转港
    dest_port_id = fields.Many2one(comodel_name="basedata.internation_port", string="Destination Port") # 目的港
    decl_custom_id = fields.Many2one(comodel_name="delegate_customs", string="Declare Customs")         # 申报口岸


    @api.model
    def create(self, vals):
        """重新设计订单号的生成，加入进出口类型，运输方式，日期等参数"""

        if vals.get('name', _('New')) == _('New'):
            business_type = self.env['business_type'].browse(vals['business_type'])
            business_type_code = business_type.code

            import pytz
            tz = pytz.timezone('Asia/Shanghai')
            # tz = self.env.context.get('tz', 'Asia/Shanghai')
            local_time = fields.datetime.now(tz).strftime('%y%m')
            company_code = self.env.user.company_id.company_code
            if not company_code:
                raise UserError(_('Please check your company code firstly'))
            name = company_code + '-' + business_type_code + local_time
            qsets = self.search([('name', 'like', name+'%')])

            if len(qsets) == 0:
                num = 1
            else:
                name_sets = []
                for i in qsets:
                    s = i.name[-3:]
                    try:
                        name_sets.append(int(s))
                    except ValueError:
                        raise ValidationError(_('The last four num of order occur wrong, please make sure it is numbers'))
                num = max(name_sets) + 1
            vals['name'] = (name + '%03d') % num

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id',
                                                   partner.property_product_pricelist and
                                                   partner.property_product_pricelist.id)
        result = super(Order, self).create(vals)
        if 'customer_service' in vals:
            user_id = self.env['res.users'].browse(int(vals.get('customer_service')))
            result.message_subscribe_users(user_ids=user_id.ids)
        return result


        # # department = super(Department, self.with_context(mail_create_nosubscribe=True)).create(vals)
        # manager = self.env['hr.employee'].browse(vals.get("manager_id"))
        # if manager.user_id:
        #     department.message_subscribe_users(user_ids=manager.user_id.ids)
        # return department

    # employee = self.env['hr.employee'].browse(employee_id)
    # if employee.user_id:
    #     self.message_subscribe_users(user_ids=employee.user_id.ids)



    # @api.multi
    # def write(self, vals):
    #     for obj in self:
    #         if 'customer_service' in vals:
    #             partner_id = self.env['res.users'].browse(int(vals.get('customer_service'))).partner_id
    #             obj.message_subscribe_users(user_ids=partner_id.ids)
    #     return super(Order, self).write(vals)

    @api.multi
    def signed_contract(self):
        """为报价单签订合同"""
        self.ensure_one()
        context = {}

        return True


    @api.multi
    def pop_contract_action(self):
        """弹出合同窗口"""
        self.ensure_one()
        obj = self[0]
        contract = obj.contract
        if not contract:
            raise UserError(_("Can't find related contract"))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Contract'),
            'res_model': contract._name,
            'view_mode': 'form, tree',
            'view_type': 'form',
            'nodestory': True,
            'res_id': contract.id,
            'target': 'current'
        }

    @api.multi
    def pop_work_sheet_action(self):
        """弹出相关工作单"""
        self.ensure_one()
        obj = self[0]
        work_sheet = obj.work_sheet_id
        if not work_sheet:
            raise UserError(_("Can't find related work sheet"))

        tree_id = self.env.ref('service_center.view_work_sheet_tree_total').id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Work Sheet'),
            'res_model': work_sheet._name,
            'view_mode': 'tree, form',
            'views': [(tree_id, 'tree'), (False, 'form')],
            "domain": [["sale_order_no", "=", obj.id]],
            # 'view_id': self.env.ref('service_center.view_work_sheet_tree_total').id,
            'nodestory': True,
            'target': 'current'
        }

    # @api.multi
    # def action_confirm(self):
    #     """重写确认销售函数，加入生成工作单功能"""
    #     for obj in self:
    #         vals = {
    #             'customer': obj.partner_id.id,
    #             'business_type': obj.business_type.id,
    #             'sale_order_no': obj.id,
    #             'contract_no': obj.contract.id,
    #             'wrap_type': obj.packing.id,
    #             'deal_type': obj.trade_term.id,
    #             'trade_mode_id': obj.trade_mode.id,
    #             'qty': obj.num,
    #             'cn_name': obj.goods_name
    #         }
    #         vals = {i : vals[i] for i in vals if vals[i]}
    #         obj.work_sheet_id |= self.env['work_sheet'].with_context(default_business_type=obj.business_type.id).create(vals)
    #
    #     return super(Order, self).action_confirm()

    @api.multi
    def create_work_sheet(self):
        """创建工作单并更改状态"""
        for obj in self:
            vals = {
                'customer': obj.partner_id.id,
                'settlement_object': obj.partner_id.id,
                'business_type': obj.business_type.id,
                'sale_order_no': obj.id,
                'contract_no': obj.contract.id if obj.contract else False,
                'wrap_type': obj.packing.id if obj.packing else False,
                'deal_type': obj.incoterm.id if obj.incoterm else False,
                'trade_mode_id': obj.trade_mode.id if obj.trade_mode else False,
                'qty': obj.num,
                'cn_name': obj.goods_name,
                'sale_man': obj.user_id.id,
                'customer_service': obj.customer_service.id
            }
            vals = {i: vals[i] for i in vals if vals[i]}
            obj.work_sheet_id |= self.env['work_sheet']\
                .with_context(default_business_type=obj.business_type.id)\
                .create(vals)
        # self.write({'state': 'sheet'})

        return True

    @api.multi
    @api.depends('work_sheet_id')
    def _count_work_sheet(self):
        """计算工作单个数"""
        for obj in self:
            obj.work_sheet_count = len(obj.work_sheet_id)

    @api.multi
    @api.onchange('partner_id')
    def _get_custom_servise(self):
        """得到销售订单的客服"""
        for obj in self:
            if obj.partner_id and len(obj.partner_id.customer_service_ids) == 1:
                obj.update({'customer_service': obj.partner_id.customer_service_ids[0].id})


    @api.onchange('business_type')
    def _change_business_type(self):
        """根据业务类型改变单号规则"""
        if self.name and self.name != _('New'):
            de_time_name = self.name[0:-7]
            time = self.name[-7:]
            name = de_time_name.split('-')[0] + '-' + self.business_type.code + time
            self.name = name


    @api.multi
    def write(self, vals):
        """根据业务类型改变单号规则"""
        for obj in self:
            if 'business_type' in vals:
                business_type = self.env['business_type'].browse(vals['business_type'])
                de_time_name = self.name[0:-7]
                time = self.name[-7:]
                name = de_time_name.split('-')[0] + '-' + business_type.code + time
                order_sets = self.env['sale.order'].search([('name', '=', name)])
                if len(order_sets) == 0:
                    vals['name'] = name
                else:
                    q_name = name[0:-3]
                    order_sets = self.env['sale.order'].search([('name', 'like', q_name+'%')])
                    numbers_char = order_sets.mapped(lambda r: r.name[-3:])
                    numbers = [int(i) for i in numbers_char]
                    max_num = max(numbers) + 1
                    name = (name[0: -3] + '%03d') % max_num
                    vals['name'] = name

        return super(Order, self).write(vals)

class delivery_info(models.Model):
    """收发货信息"""
    _name = 'boyue_sale_extend.delivery_info'
    _description = 'Delivery Info'

    order = fields.Many2one(comodel_name="sale.order", string="Order", required=True, ondelete='cascade')
    type_id = fields.Many2one(comodel_name="boyue_sale_extend.consignor_nee_type", string="Type", required=True)
    name = fields.Char(string="Name", required=True)
    address = fields.Char(string="Address", required=False, )
    qty = fields.Integer(string="Qty", required=False, )
    wrap_type = fields.Many2one(comodel_name="delegate_packing", string="Wrap Type", required=False, )
    gross_weight = fields.Float(string="Gross Quantity",  required=False, digits=dp.get_precision('Stock Weight'))
    remark = fields.Text(string="Remark", required=False, )


class ConsignorConsigneeType(models.Model):
    _name = 'boyue_sale_extend.consignor_nee_type'
    _rec_name = 'name'
    _description = 'Consignor Consignee Type'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description", required=False, )



class OrderLine(models.Model):
    """继承销售订单，加入多币种功能"""
    _inherit = 'sale.order.line'

    name = fields.Text(string="Description", required=False)
    quote_price_unit = fields.Float(string="Quoto Price Unit",  required=True, )
    # currency_field='quote_currency_id')      # 报价单价
    quote_currency_id = fields.Many2one(comodel_name="res.currency", string="Quote Currency", required=True,)  # 报价币种
    rate = fields.Float(string="Rate", related='quote_currency_id.rate',  required=False, )
    # price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'),
    #                           compute='_compute_price_unit' ,default=0.0)

    # @api.depends('rate')
    # def _compute_price_unit(self):
    #     """根据所选币种的汇率计算出当前单价"""
    #     for order_line in self:
    #         if order_line.rate != 0:
    #             order_line.price_unit = order_line.quote_price_unit / order_line.rate

    @api.onchange('rate', 'quote_price_unit')
    def _compute_price_unit(self):
        """根据所选币种的汇率计算出当前单价"""
        for order_line in self:
            if order_line.rate != 0:
                order_line.price_unit = order_line.quote_price_unit / order_line.rate

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = 1.0

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        self.quote_currency_id = self.product_id.currency_id    # 把产品的货币带到询价货币中去
        self.quote_price_unit = self.product_id.list_price * self.rate      # 当产品发生改变时，报价单价也要发生改变

        name = ' '
        if product.description_sale:
            name += product.description_sale
        vals['name'] = name

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price(self._get_display_price(product), product.taxes_id, self.tax_id)
        self.update(vals)

        title = False
        message = False
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            if product.sale_line_warn == 'block':
                self.product_id = False
            return {'warning': warning}
        return {'domain': domain}

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id.id,
                quantity=self.product_uom_qty,
                date_order=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.price_unit = self.env['account.tax']._fix_tax_included_price(self._get_display_price(product), product.taxes_id, self.tax_id)
            # self.quote_price_unit = self.price_unit     # 同时更改报价单价
            self.price_unit = self.quote_price_unit / self.rate    # 同时更改报价单价


class ContractWizard(models.TransientModel):
    _name = 'boyue_sale_extend.contract_wizard'
    _description = 'choose or create contract'

    choose_type = fields.Selection(string="Choose Type", selection=[('create', 'Create'), ('select', 'Select'),],
                                   default='create')
    contract_name = fields.Char('Inner Num')  # 客户内部合同号
    customer = fields.Many2one('res.partner', string='Customer', required=True)  # 客户
    contract_type = fields.Many2one(comodel_name="contract.contract_type", string="Contract type",
                                   required=True, )  # 合同类型
    our_signatory = fields.Many2one('res.users', string='Our signatory', default=lambda self: self.env.user)  # 我方签约人
    customer_signatory = fields.Many2one(comodel_name="res.partner", string="Customer signatory",
                                         required=True)  # 客户签约人
    contract_effective_date = fields.Datetime(string='Effective Time', default=fields.Datetime.now, required=True)  # 合同生效日期
    contract_failure_date = fields.Datetime(string='Failure time', required=True)  # 合同终止日期
    note = fields.Text(string='Remarks')  # 备注说明

    selected_contract = fields.Many2one(comodel_name="contract.sale_contract", string="Contract")

    @api.multi
    def create_contract(self):
        """利用向导生成合同"""
        order = self.env['sale.order'].browse(self._context.get('sale_order'))

        vals = {
            'inner_num': self.contract_name,
            'customer': self.customer.id,
            'contract_type': self.contract_type.id,
            'our_signatory': self.our_signatory.id,
            'customer_signatory': self.customer_signatory.id,
            'contract_effective_date': self.contract_effective_date,
            'contract_failure_date': self.contract_failure_date,
        }
        contract = self.env['contract.sale_contract'].create(vals)
        # order.write({'contract': contract.id, 'state': 'sale'})
        order.write({'contract': contract.id, })

        return True

    @api.multi
    def choose_contract(self):
        """选择合同"""
        if not self.selected_contract:
            raise UserError(_('Please select contract'))
        order = self.env['sale.order'].browse(self._context.get('sale_order'))
        # order.write({'contract': self.selected_contract.id, 'state': 'sale'})
        order.write({'contract': self.selected_contract.id, })

        return True

    @api.multi
    @api.onchange('selected_contract')
    def _comput_contract(self):
        for item in self:
            if item.selected_contract:
                item.contract_name = item.selected_contract.name
                item.customer = item.selected_contract.customer
                item.contract_type = item.selected_contract.contract_type
                item.our_signatory = item.selected_contract.our_signatory
                item.customer_signatory = item.selected_contract.customer_signatory
                item.contract_effective_date = item.selected_contract.contract_effective_date
                item.contract_failure_date = item.selected_contract.contract_failure_date


class Company(models.Model):
    """增加公司代码"""
    _name = 'res.company'
    _inherit = 'res.company'

    company_code = fields.Char(string="Code", required=False)