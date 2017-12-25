# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.osv.orm import except_orm


class WorkSheet(models.Model):
    """继承工作单模型，创建工作单的时候 自动创建结算单"""
    _description = 'Work Sheet model extend auto Expense Statement'
    _inherit = 'work_sheet'

    expense_statement_ids = fields.One2many(comodel_name="settlement.expense_statement", inverse_name="work_sheet_no",
                                          string="expense_statement_ids")

    customer_bill = fields.One2many(comodel_name="settlement.customer_bill", inverse_name="work_sheet_no",
                                          string="customer bill")    # 费用清单 一对多关联账单

    @api.multi
    def jump_expense_statement(self):
        """从工作单的费用明细按钮 跳转到费用明细界面"""
        # work_sheet_no_obj = self[0].expense_statement_ids[0]
        for sheet in self:
            work_sheet_no_obj = sheet.expense_statement_ids
            return {
                'name': "settlement expense statement",
                'type': "ir.actions.act_window",
                'view_type': 'form',
                'view_mode': 'form, tree',
                'res_model': 'settlement.expense_statement',
                'views': [[False, 'form']],
                'res_id': work_sheet_no_obj.id,
                # 'context': {
                #     'default_work_sheet_no': self.ids,  # [line.expense_receivable_no for line in self]
                #     # 'default_settlement_object': [line.settlement_object for line in self]
                #     # 'settlement_object': self[0].settlement_object,
                #     # 'settlement_object': self[0].settlement_object for line in self
                #     # 'settlement_object': [line.settlement_object for line in self][0]
                # },
                'target': 'current'
            }

    @api.model
    def create(self, vals):
        """创建工作单的时候 生成结算单"""

        result = super(WorkSheet, self).create(vals)
        expense_statement = self.env['settlement.expense_statement'].create({
                'work_sheet_no': result.id
            })

        return result

    # 扩展工作单的 确认按钮
    @api.multi
    def confirm(self):
        """确认按钮 关联费用清单功能扩展"""

        result = super(WorkSheet, self).confirm()

        for sheet in self:
            expense_statement = sheet.expense_statement_ids

            print("******************###########费用清单 当前状态##########***********************")
            # expense_statement_obj = self.env['settlement.expense_statement'].browse(self._context.get('work_sheet_no'))
            print(expense_statement)
            print(expense_statement[0])
            print(expense_statement[0].state)
            # print(expense_statement_obj)
            # print(expense_statement_obj.state)
            print("******************###########***************##########***********************")
            if expense_statement:
                if expense_statement[0].state == 'cancel':
                    # expense_statement[0].state = 'cancel'
                    expense_statement[0].update({
                        'state': 'draft'
                    })
                else:
                    pass
            else:
                expense_statement = self.env['settlement.expense_statement'].create({
                    'work_sheet_no': sheet.id
                })
        return True

        # 工作单 确认按钮逻辑
        # 先确定当前工作单有没有关联的费用清单
        # 如果有 已关联的费用清单
        #   判断已关联的费用清单的状态
        #       如果该费用清单状态为“取消” 则把当前费用清单状态修改为“草稿”
        #       如果该费用清单状态不是“取消” 则什么都不做，pass
        # 如果没有 则创建新的费用清单
        # ####################################################################################

    # 扩展工作单的 取消按钮
    @api.multi
    def canceld(self):
        """取消按钮 关联费用清单功能扩展"""

        result = super(WorkSheet, self).canceld()

        for sheet in self:
            expense_statement = sheet.expense_statement_ids
            if expense_statement:
                expense_statement[0].update({
                    'state': 'cancel'
                })
        return True

        # 工作单 取消按钮逻辑
        # 先确定当前工作单有没有关联的费用清单
        # 如果有 已关联的费用清单
        #   判断已关联的费用清单的状态
        #       如果该费用清单状态为“取消” 则什么都不做，pass
        #       如果该费用清单状态是“草稿” 则把当前费用清单状态修改为“取消”
        # 如果没有 则pass


class ExpenseStatement(models.Model):
    """ 费用清单 """
    _name = "settlement.expense_statement"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'expense statement models'

    _rec_name = "work_sheet_no"

    # 关联工作单号 多对一 唯一约束 即：唯一约束
    work_sheet_no = fields.Many2one(comodel_name="work_sheet", string="work_sheet_no", required=False, )
    confirm_receivable_expense = fields.Boolean(string="Receivable Expense Type-in Status", default=False,)  # 确认应收费用
    confirm_expense_payable = fields.Boolean(string="Expense Payable Type-in Status", default=False,)        # 确认应付费用

    # 结算单模型里边需要 关联显示的工作单模型的相关字段
    # 1 业务选项
    booking = fields.Boolean(related='work_sheet_no.booking', string='Booking', readonly=True)   # 订舱
    fumigation = fields.Boolean(related='work_sheet_no.fumigation', string='Fumigation', readonly=True)             # 熏蒸
    inspection = fields.Boolean(related='work_sheet_no.inspection', string="Inspection", readonly=True)             # 报检
    land_trans = fields.Boolean(related='work_sheet_no.land_trans', string="Land Transportation", readonly=True)      # 陆运
    warehouse = fields.Boolean(related='work_sheet_no.warehouse', string="Warehouse", readonly=True)           # 仓储
    custom = fields.Boolean(related='work_sheet_no.custom', string="Custom", readonly=True)                 # 报关
    switch_bill = fields.Boolean(related='work_sheet_no.switch_bill', string='Switch Bill', readonly=True)            # 换单

    # 其他信息
    customer_id = fields.Many2one(related='work_sheet_no.customer', string="Customer", required=True,
                               domain=[('is_company', '=', True), ('customer', '=', True)], readonly=True)   # 客户
    contact_id = fields.Many2one(related='work_sheet_no.contact', string="Contact", readonly=True)  # 联系人
    goods_source = fields.Selection(related='work_sheet_no.goods_source', string="Goods Source", readonly=True)     # 揽货类型
    trade_mode_id = fields.Many2one(related='work_sheet_no.trade_mode_id', string='Trade Mode')  # 监管方式 贸易性质

    deal_type_id = fields.Many2one(related='work_sheet_no.deal_type', string="Deal Type", readonly=True)  # 贸易条款, Deal Type
    sale_order_no = fields.Many2one(related='work_sheet_no.sale_order_no',
                                    string="SaleOrder No", ondelete='set null', readonly=True)  # 销售订单号, SaleOrder No
    contract_no = fields.Many2one(related='work_sheet_no.contract_no', string="Contract No", readonly=True)  # 合同号, Contract No
    customer_project_no = fields.Char(related='work_sheet_no.customer_project_no', string='customer project no')  # 客户项目号
    # customer_internal_num = fields.Char(related='work_sheet_no.customer_internal_num', string='CustomerInnerNO', readonly=True)  # 客户内部编号

    company_id = fields.Many2one(related='work_sheet_no.company', string="Company", readonly=True)  # 公司, Company
    sale_man_id = fields.Many2one(related='work_sheet_no.sale_man', string='Saleman', readonly=True)  # 销售员, Saleman
    operation_requirements = fields.Text(related='work_sheet_no.operation_requirements', string="Operation Requirements"
                                         , readonly=True)  # 操作要求,Operation Requirements

    settlement_object_id = fields.Many2one(related='work_sheet_no.settlement_object', string="Settlement Object",
                                           required=True,)  # 结算对象

    qty = fields.Integer(related='work_sheet_no.qty', string='Qty')  # 委托件数
    gross_weight = fields.Float(related='work_sheet_no.gross_weight', string='GrossWeight')  # 委托毛重
    volume = fields.Float(related='work_sheet_no.volume', string='Volume')  # 委托体积
    charge_weight = fields.Float(related='work_sheet_no.charge_weight', string='Charge Weight')  # 委托计费重量

    business_type = fields.Many2one(related='work_sheet_no.business_type', string="Business Type")   # 业务类型
    mbl_no = fields.Char(related='work_sheet_no.mbl_no', string='MBL No')    # 空运主单号
    hbl_no = fields.Char(related='work_sheet_no.hbl_no', string='HBL No')    # 空运分单号
    mawb_no = fields.Char(related='work_sheet_no.mawb', string='MAWB ')       # 海运主单号
    hawb_no = fields.Char(related='work_sheet_no.hawb', string='HAWB')        # 海运分单号

    master_no = fields.Char(compute='_generate_add_master_no', string="master no",)  # 主单号
    house_no = fields.Char(compute='_generate_add_house_no', string="house no",)   # 分单号

    start_port_id = fields.Many2one(related='work_sheet_no.loading_port', string='LoadingPort')  # 起运港
    transit_port_id = fields.Many2one(related='work_sheet_no.transition_port', string='TransshipmentPort')      # 中转港
    final_port_id = fields.Many2one(related='work_sheet_no.destination_port', string='DeliveryPort')        # 目的港
    start_date = fields.Datetime(related='work_sheet_no.start_date', string='SailingDate')  # 开航日期
    arrive_date = fields.Datetime(related='work_sheet_no.arrive_date', string='Arrival Port Date')  # 到港日期
    customer_service_id = fields.Many2one(related='work_sheet_no.customer_service', string="Customer Service",
                                          readonly=True)   # 客服
    # state = fields.Selection(related='work_sheet_no.state', string='status', readonly=True, default='draft')  # 状态
    state = fields.Selection(selection=[('draft', 'Draft'),  # 草稿
                                        # ('confirm', 'Confirm'),  # 已确认
                                        ('cancel', 'Cancel')  # 已取消
                                        ], string='status', readonly=True, default='draft')

    @api.onchange('business_type', 'mbl_no', 'mawb_no')
    def _generate_add_master_no(self):
        """根据当前工作单的业务类型 选择主单号填充海运主单号 还是空运主单号"""
        # print("******************#####################***********************")
        # print(self[0].business_type.id)
        # print(self[0].mbl_no)
        # print(self[0].hbl_no)
        # print(self[0].business_type.transport_mode)
        # print("******************#####################***********************")
        for work_sheet in self:
            if work_sheet.business_type.code in ['SI', 'SE']:
                work_sheet.master_no = work_sheet.mbl_no
            elif work_sheet.business_type.code in ['AI', 'AE']:
                work_sheet.master_no = work_sheet.mawb_no

    @api.onchange('business_type', 'hbl_no', 'hawb_no')
    def _generate_add_house_no(self):
        # print("******************#####################***********************")
        # print(self[0].business_type)
        # print("******************#####################***********************")
        """根据当前工作单的业务类型 选择分单号填充海运分单号 还是空运分单号"""
        for work_sheet in self:
            if work_sheet.business_type.code in ['SI', 'SE']:
                work_sheet.house_no = work_sheet.hbl_no
            # elif work_sheet.business_type.transport_mode == 6:
            elif work_sheet.business_type.code in ['AI', 'AE']:
                work_sheet.house_no = work_sheet.hawb_no

    # 方式2 compute得到所有工作单的字段
    # wk_name = fields.Char(string="Name", compute='_compute_work_sheet')
    #
    # @api.multi
    # def _compute_work_sheet(self):
    #     """得到所有工作单的字段"""
    #     for item in self:
    #         item.wk_name = item.work_sheet_no.name



    # customer_bill = fields.Many2many(comodel_name='settlement.customer_bill', string='customer bill')  # 费用清单 多对多关联账单
    receivable_expense_no = fields.One2many(comodel_name="settlement.receivable_expense",
                                            inverse_name="expense_statement_no",
                                            string="应收费用Ids", required=False, )         # 应收费用Ids
    expense_payable_no = fields.One2many(comodel_name="settlement.expense_payable", inverse_name="expense_statement_no",
                                         string="应付费用Ids", required=False, )             # 应付费用Ids
    customer_bill_ids = fields.Many2many(comodel_name="settlement.customer_bill", string="账单Ids",
                                         required=False)   # 账单Ids
    payment_application_ids = fields.Many2many(comodel_name="settlement.pay_apply_sheet",
                                               string="付款申请单Ids", required=False)        # 付款申请Ids

    # #####################################################################################

    # 关联显示 应收费用的相关字段
    currency_id = fields.Many2one(related='receivable_expense_no.currency_id', string="Currency", required=False, )  # 原商品币种
    base_money_currency_id = fields.Many2one(related='receivable_expense_no.base_money_currency_id',
                                             string='Base Currency', readonly=True)  # 本位币币种
    # 原币种单行总价
    original_amount_total = fields.Monetary(related='receivable_expense_no.original_amount_total',
                                            string="original total price", required=True, readonly=True,)
    # 本位币单行总价
    base_money_amount_total = fields.Monetary(related='receivable_expense_no.base_money_amount_total',
                                              string="base money total price", required=True, readonly=True, )

    # 应收费用 折合人名币总价
    receivable_expense_total = fields.Monetary(string='receivable expense total',
                                               currency_field='base_money_currency_id',
                                               readonly=True, compute='_company_receivable_expense_total')

    # 应收费用　美元总价
    receivable_expense_usd_total = fields.Monetary(string='receivable expense USD total',
                                                   currency_field='currency_id',
                                                   readonly=True, compute='_company_receivable_expense_more_total')

    # 应收费用 欧元总价
    receivable_expense_eur_total = fields.Monetary(string='receivable expense EUR total',
                                                   currency_field='currency_id',
                                                   readonly=True, compute='_company_receivable_expense_more_total')
    # 应收费用 人名币总价
    receivable_expense_cny_total = fields.Monetary(string='receivable expense CNY total',
                                                   currency_field='currency_id',
                                                   readonly=True, compute='_company_receivable_expense_more_total')

    profit_total = fields.Monetary(string='profit total', currency_field='currency_id', readonly=True,
                                   compute='_company_profit_total')   # 根据应收费用和应付费用  计算出利润

    @api.onchange('receivable_expense_cny_total', 'expense_payable_cny_total')
    def _company_profit_total(self):
        """根据应收费用和应付费用  计算出利润"""
        for line in self:
            line.profit_total = line.receivable_expense_total - line.expense_payable_total

    @api.multi
    @api.depends('base_money_currency_id', 'base_money_amount_total')
    def _company_receivable_expense_total(self):
        """计算应收费用 折合人名币总价"""
        for expense_statement in self:
            total = 0
            for receivable_expense in expense_statement.receivable_expense_no:
                total += receivable_expense.base_money_amount_total
            expense_statement.receivable_expense_total = total
            # print(expense_statement.receivable_expense_total)
        return True

    @api.multi
    @api.depends('currency_id')
    def _company_receivable_expense_more_total(self):
        """分币种统计 计算应收费用 美元总价 欧元总价 人民币总价"""
        usd_obj = self.env.ref('base.USD')
        eur_obj = self.env.ref('base.EUR')
        cny_obj = self.env.ref('base.CNY')
        for line in self.receivable_expense_no:
            if line.currency_id.id == usd_obj.id:
                self.receivable_expense_usd_total += line.original_amount_total
            elif line.currency_id.id == eur_obj.id:
                self.receivable_expense_eur_total += line.original_amount_total
            elif line.currency_id.id == cny_obj.id:
                self.receivable_expense_cny_total += line.original_amount_total

    # #####################################################################################

    # 关联显示 应付费用的相关字段
    pay_currency_id = fields.Many2one(related='expense_payable_no.currency_id', string="Currency",
                                  required=False, )  # 原商品币种
    pay_base_money_currency_id = fields.Many2one(related='expense_payable_no.base_money_currency_id',
                                             string='Base Currency', readonly=True)  # 本位币币种
    # 原币种单行总价
    pay_original_amount_total = fields.Monetary(related='expense_payable_no.original_amount_total',
                                            string="original total price", required=True, readonly=True, )
    # 本位币单行总价
    pay_base_money_amount_total = fields.Monetary(related='expense_payable_no.base_money_amount_total',
                                              string="base money total price", required=True, readonly=True, )

    # 应付费用 折合人名币总价
    expense_payable_total = fields.Monetary(string='expense payable total',
                                            currency_field='pay_base_money_currency_id',
                                            readonly=True, compute='_company_expense_payable_total')

    # 应付费用　美元总价
    expense_payable_usd_total = fields.Monetary(string='expense payable USD total',
                                                currency_field='pay_currency_id',
                                                readonly=True, compute='_company_expense_payable_more_total')

    # 应付费用 欧元总价
    expense_payable_eur_total = fields.Monetary(string='expense payable  EUR total',
                                                currency_field='pay_currency_id',
                                                readonly=True, compute='_company_expense_payable_more_total')
    # 应付费用 人名币总价
    expense_payable_cny_total = fields.Monetary(string='expense payable CNY total',
                                                currency_field='pay_currency_id',
                                                readonly=True, compute='_company_expense_payable_more_total')

    @api.multi
    @api.depends('pay_base_money_currency_id', 'pay_base_money_amount_total')
    def _company_expense_payable_total(self):
        """计算应付费用 折合人名币总价"""
        # self.expense_payable_total = sum(line.base_money_amount_total for line in self.expense_payable_no)
        # self.write({'expense_payable_total': sum(line.base_money_amount_total for line in self.mapped('expense_payable_no'))})
        # payable_total = sum(line.base_money_amount_total for line in self.mapped('expense_payable_no'))
        # print("******************########XXXXXXXXXXX 单个费用清单 应付费用 折合人名币总价XXXXXXXXXXXXXXXXXXXXXXXx#############***********************")
        # print(payable_total)
        # self.update(
        #     {'expense_payable_total': payable_total})

        for expense_statement in self:
            payable_total = 0
            for payable_expense in expense_statement.expense_payable_no:
                payable_total += payable_expense.base_money_amount_total
            expense_statement.expense_payable_total = payable_total
        return True

    #######################################################################
    # 费用列表视图底部统计相关
    # 费用列表视图底部 应收费用  折合人名币总价
    receivable_expense_list_bottom_total = fields.Monetary(string='receivable expense list bottom total',
                                               currency_field='base_money_currency_id',
                                               readonly=True, compute='_company_receivable_expense_list_bottom_total')

    @api.multi
    @api.depends('base_money_currency_id', 'base_money_amount_total')
    def _company_receivable_expense_list_bottom_total(self):
        """结算列表视图 底部显示 应收费用总计"""
        list_bottom_total = sum(line.base_money_amount_total for line in self.mapped('receivable_expense_no'))
        self.update(
            {'receivable_expense_total': list_bottom_total})

    # 费用列表底部 应付费用  折合人名币总价
    expense_list_bottom_payable_total = fields.Monetary(string='expense list bottom payable total',
                                            currency_field='pay_base_money_currency_id',
                                            readonly=True, compute='_company_expense_list_bottom_payable_total')

    @api.multi
    @api.depends('pay_base_money_currency_id', 'pay_base_money_amount_total')
    def _company_expense_list_bottom_payable_total(self):
        """结算列表视图 底部显示 应付费用总计"""
        payable_total = sum(line.base_money_amount_total for line in self.mapped('expense_payable_no'))
        print("******************########XXXXXXXXXXX结算列表视图 底部显示 应付费用 折合人名币总价XXXXXXXXXXXXXXXXXXXXXXXx#############***********************")
        print(payable_total)
        self.update(
            {'expense_payable_total': payable_total})

    @api.multi
    @api.depends('pay_currency_id', 'pay_original_amount_total')
    def _company_expense_payable_more_total(self):
        """分币种统计 计算应付费用 美元总价 欧元总价 人民币总价"""
        usd_obj = self.env.ref('base.USD')
        eur_obj = self.env.ref('base.EUR')
        cny_obj = self.env.ref('base.CNY')
        for line in self.expense_payable_no:
            if line.currency_id.id == usd_obj.id:
                self.expense_payable_usd_total += line.original_amount_total
            elif line.currency_id.id == eur_obj.id:
                self.expense_payable_eur_total += line.original_amount_total
            elif line.currency_id.id == cny_obj.id:
                self.expense_payable_cny_total += line.original_amount_total


    # ###########################################################################################

    # 关联工作单号 唯一约束
    @api.constrains('work_sheet_no')
    def _check_work_sheet_no(self):
        for item in self:
            if len(item.work_sheet_no) > 1:
                raise except_orm(u'error', u'unique error')

    # 确认收入
    @api.multi
    def confirm_income_btn(self):
        self.update({'confirm_receivable_expense': True})

    # 取消确认收入
    @api.multi
    def cancel_confirm_income_btn(self):
        self.update({'confirm_receivable_expense': False})

    # 确认成本
    @api.multi
    def confirm_cost_btn(self):
        self.update({'confirm_expense_payable': True})

    # 取消确认成本
    @api.multi
    def cancel_confirm_cost_btn(self):
        self.update({'confirm_expense_payable': False})


class ReceivableExpense(models.Model):
    """ 应收费用"""
    _name = "settlement.receivable_expense"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'about receivable expense'
    # _rec_name = "receivable_expense_sheet_id"

    # receivable_expense_sheet_id = fields.Char(string='receivable expense Sheet ID', required=True, copy=False,
    #                                           state={'draft': [('readonly', False)]},
    #                                           default=lambda self: _('New'))   # 应收费用单号
    expense_statement_no = fields.Many2one(comodel_name='settlement.expense_statement',
                                           string='expense statement')  # 结算单号
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)],
                                 change_default=True, ondelete='restrict', required=True)  # 产品ID
    qty = fields.Integer(string="quantity", required=False, default=1)  # 数量
    unit_price = fields.Monetary(string="unit price", required=True)  # 原币种单价
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", required=True, default=lambda self: self._get_user_currency())  # 币种
    rate = fields.Float(string="Rate", related='currency_id.rate', required=False, readonly=True,)  # 汇率
    base_money_unit_price = fields.Monetary(compute='_compute_price_unit', string="base money unit price", required=True, readonly=True,)  # 本位币单价
    base_money_currency_id = fields.Many2one('res.currency', string='Base Currency', required=True, readonly=True,
                                             default=lambda self: self._get_user_currency())  # 本位币币种
    customer_bill_id = fields.Many2one(comodel_name="settlement.customer_bill", string="customer bill id", required=False,)  #关联账单 账单号
    # 备注 创建人 创建时间 系统自带 不需要创建

    # 需要显示的其他模型的字段
    # ExpenseStatement
    work_sheet_no = fields.Many2one(related='expense_statement_no.work_sheet_no', string="work_sheet_no", required=False)     # 工作单号
    customer_id = fields.Many2one(related='expense_statement_no.customer_id', string="Customer", required=True,
                               domain=[('is_company', '=', True), ('customer', '=', True)])   # 客户

    contract_no = fields.Many2one(comodel_name="contract.sale_contract", string="Contract No")  # 合同号, Contract No

    # 应收费状态 是否已经添加到账单 _generate_bill_status
    receivable_expense_status = fields.Boolean(compute='_generate_add_bill_status', string="Receivable Expense add bill Status", default=False)  # 应收费用状态

    # 账单状态
    bill_state = fields.Selection(related='customer_bill_id.state', string='status', readonly=True)
    # 结算单位
    settlement_object = fields.Many2one(comodel_name="res.partner", string="Settlement Object",
                                        required=True, )  # 结算对象
    # 费用

    # 原币种单条总价 = 原币种单价 X 数量
    original_amount_total = fields.Monetary(compute='_compute_total_original_price', string="original total price", required=True, readonly=True,)
    # 本位币单条总价 = 本位币单价 X 数量
    base_money_amount_total = fields.Monetary(compute='_compute_total_base_money_price', string="base money total price", required=True, readonly=True,)

    @api.onchange('rate', 'unit_price')
    def _compute_price_unit(self):
        """根据所选币种的汇率计算出本位币单价"""
        for receivable_expense in self:
            if receivable_expense.rate != 0:
                receivable_expense.base_money_unit_price = receivable_expense.unit_price / receivable_expense.rate

    @api.onchange('qty', 'unit_price')
    def _compute_total_original_price(self):
        """根据当前服务的原币种单价 X 数量 计算出原币种总价"""
        # print("******************#####################***********************")
        # print(self[0].unit_price)
        # print("******************#####################***********************")
        for receivable_expense in self:
            if receivable_expense.qty != 0:
                receivable_expense.original_amount_total = receivable_expense.qty * receivable_expense.unit_price

    @api.onchange('qty', 'base_money_unit_price')
    def _compute_total_base_money_price(self):
        """根据当前服务的本位币单价 X 数量 计算出单行本位币总价"""
        for receivable_expense in self:
            if receivable_expense.qty != 0:
                receivable_expense.base_money_amount_total = receivable_expense.qty * receivable_expense.base_money_unit_price

    @api.model
    def _get_euro(self):
        return self.env['res.currency.rate'].search([('rate', '=', 1)], limit=1).currency_id

    @api.model
    def _get_user_currency(self):
        """获取当前用户所在公司的币种 作为默认的本位币币种"""
        currency_id = self.env['res.users'].browse(self._uid).company_id.currency_id
        return currency_id or self._get_euro()

    @api.multi
    @api.onchange('customer_bill_id')
    def _generate_add_bill_status(self):
        print("******************#####################***********************")
        print(self[0].customer_bill_id)
        print("******************#####################***********************")
        """根据当前账单字段是否为空  判断是否已经生成了账单 然后修改费用生成账单状态"""
        for receivable_expense in self:
            if receivable_expense.customer_bill_id:
                receivable_expense.receivable_expense_status = True
            else:
                receivable_expense.receivable_expense_status = False

    @api.multi
    def generate_account_bill(self):
        """批量生成账单"""
        # if any(receivable_expense.state != 'draft' for receivable_expense in self):
        #     raise UserError(_("You cannot report twice the same line!"))
        if len(self.mapped('settlement_object')) != 1:
            # raise UserError(
            #     _("You cannot generate account bill for different settlement object in the same account bill!"))
            raise UserError(_("同一个账单中不能含有不同的结算对象，请重新选择！"))
        for account_bill in self:
            if account_bill.receivable_expense_status:
                raise UserError(
                    _("您选择的应收费用列表中，含有已生成账单的费用，请重新选择!"))
            # else:
            #     default_settlement_object = account_bill.settlement_object[0]
        print('*********************88888888888888888**********************************')
        default_settlement_object = self.mapped('settlement_object')[0]
        default_customer_id = self.mapped('customer_id')[0]
        print(default_customer_id.id)
        print(default_settlement_object.id)
        print(default_settlement_object.ids)
        print('*********************88888888888888888**********************************')
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'settlement.customer_bill',
            'target': 'current',
            'context': {
                'default_receivable_expense_no': self.ids,   # [line.expense_receivable_no for line in self]
                'default_settlement_object': default_settlement_object.id,
                'default_customer_id': default_customer_id.id
                # 'default_settlement_object': [line.settlement_object for line in self]
                # 'settlement_object': self[0].settlement_object,
                # 'settlement_object': self[0].settlement_object for line in self
                # 'settlement_object': [line.settlement_object for line in self][0]
            }
        }
            # list_receivable_expense = receivable_expense.receivable_expense_status
            # for i in list_receivable_expense:
            #     i.receivable_expense_status = True
            #     for_settlement_object = i.settlement_object
            #     return {
            #         'type': 'ir.actions.act_window',
            #         'view_mode': 'form',
            #         'res_model': 'settlement.customer_bill',
            #         'target': 'current',
            #         'context': {
            #             'default_expense_receivable_no': self.ids,   # [line.expense_receivable_no for line in self]
            #             # 'settlement_object': self[0].settlement_object,
            #             # 'settlement_object': self[0].settlement_object for line in self
            #             'settlement_object': for_settlement_object
            #         }
            #     }

    @api.multi
    def add_account_bill(self):
        """批量添加至已有账单"""
        if len(self.mapped('settlement_object')) != 1:
            # raise UserError(
            #     _("You cannot generate account bill for different settlement object in the same account bill!"))
            raise UserError(_("同一个账单中不能含有不同的结算对象，请重新选择！"))
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'settlement.customer_bill',
            'target': 'new',
            # 'context': {
            #     'default_expense_receivable_no': self.ids,   # [line.expense_receivable_no for line in self]
            #     # 'settlement_object': self[0].settlement_object,
            #     # 'settlement_object': self[0].settlement_object for line in self
            #     # 'settlement_object': [line.settlement_object for line in self][0]
            # }

        }

    # @api.model
    # def create(self, vals):
    #     """生成应收费用的时候 如果结算对象为空 抛出异常"""
    #
    #     if not vals.get('settlement_object', _('New')) == _('New'):
    #         raise UserError(_("结算对象不能为空！"))
    #
    #     return True


class CustomerBill(models.Model):
    """ 账单"""
    _name = "settlement.customer_bill"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'about customer bill'
    _rec_name = "customer_bill_no"

    customer_bill_no = fields.Char(string="Customer Bill", required=False,)  # 账单号
    # customer_bill_no = fields.Char(string="Customer Bill", required=False, default=lambda self: _('New'))  # 账单号
    bill_type = fields.Many2one(comodel_name="settlement.bill_type",
                                string="bill type name", required=False, )   # 账单类型
    settlement_object = fields.Many2one(comodel_name="res.partner", string="Settlement Object", required=False, )   # 结算对象
    invoice_title = fields.Char(string="invoice title", required=False, )    # 开票抬头
    invoice_demand = fields.Char(string="invoice demand", required=False, )  # 开票要求
    account_checking_remark = fields.Char(string="account checking remark", required=False, )  # 对账备注
    review_remark = fields.Char(string="review remark", required=False, )    # 审核备注
    invoice_no = fields.Char(string="invoice number", required=False, )   # 发票号码
    base_money_invoice_amount = fields.Float(string="base money invoice amount",
                                             digits=dp.get_precision('Product Price'),)   # 本位币发票金额
    write_off_amount = fields.Float(string="base money invoice amount",
                                    digits=dp.get_precision('Product Price'),)  # 本位币销帐金额

    write_off_remark = fields.Text(string="write off remark", required=False, )     # 销帐备注
    state = fields.Selection(selection=[('draft', 'Draft'),    # 草稿
                                        ('submit', 'Submitted'),  # 待审核
                                        ('cancel', 'Refused'),  # 审核未通过
                                        ('approve', 'approved'),  # 通过审核
                                        ('sent', 'sent'),  # 已发邮件 待对账
                                        ('abnormal', 'abnormal'),  # 对账异常
                                        ('checked', 'checked'),  # 已对账 待付款
                                        ('paid', 'paid'),  # 已付款 待开票
                                        ('make-out', 'make-out'),  # 已开票 待销帐
                                        ('write-off', 'write-off')  # 已销账
                                        ], string='status', readonly=True, default='draft')
    receivable_expense_no = fields.One2many(comodel_name="settlement.receivable_expense", inverse_name="customer_bill_id",
                                            string="expense receivable", required=False, )  # 应收费用ID
    bill_amount = fields.One2many(comodel_name="settlement.bill_amount", inverse_name="amount_receivable",
                                  string="payment amount", required=False, )  # 关联账单金额
    # amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
    #                                  track_visibility='always') # 未含税金额
    # amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all',
    #                              track_visibility='always')  # 税金
    # amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
    #                                track_visibility='always')  # 账单总金额

    # # 多对多 关联 费用清单 相当于工作单
    # expense_statement_work_sheet_no = fields.Many2many(comodel_name='settlement.expense_statement',
    #                                                    string='expense statement no')  # 费用清单 多对多关联费用清单
    work_sheet_no = fields.Many2one(comodel_name='work_sheet', string="expense statement no", required=False, )

    # 关联显示 费用清单的相关字段
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True,
                               domain=[('is_company', '=', True), ('customer', '=', True)])  # 委托单位 客户

    trade_mode_id = fields.Many2one(related='work_sheet_no.trade_mode_id', string='Trade Mode')  # 监管方式 贸易性质

    # master_no = fields.Char(compute='_generate_add_master_no', string="master no", )  # 主单号
    # house_no = fields.Char(compute='_generate_add_house_no', string="house no", )  # 分单号

    sale_man_id = fields.Many2one(related='work_sheet_no.sale_man', string='Saleman', readonly=True)  # 销售员, Saleman

    business_type = fields.Many2one(related='work_sheet_no.business_type', string="Business Type")  # 业务类型

    qty = fields.Integer(related='work_sheet_no.qty', string='Qty')  # 委托件数
    gross_weight = fields.Float(related='work_sheet_no.gross_weight', string='GrossWeight')  # 委托毛重
    volume = fields.Float(related='work_sheet_no.volume', string='Volume')  # 委托体积
    charge_weight = fields.Float(related='work_sheet_no.charge_weight', string='Charge Weight')  # 委托计费重量

    contract_no = fields.Many2one(comodel_name="contract.sale_contract", string="Contract No")  # 合同号, Contract No

    # 关联显示 应收费用的相关字段
    currency_id = fields.Many2one(related='receivable_expense_no.currency_id', string="Currency",
                                  required=False, )  # 原商品币种
    base_money_currency_id = fields.Many2one(related='receivable_expense_no.base_money_currency_id',
                                             string='Base Currency', readonly=True)  # 本位币币种
    # 原币种单行总价
    original_amount_total = fields.Monetary(related='receivable_expense_no.original_amount_total',
                                            string="original total price", required=True, readonly=True, )
    # 本位币单行总价
    base_money_amount_total = fields.Monetary(related='receivable_expense_no.base_money_amount_total',
                                              string="base money total price", required=True, readonly=True, )

    # 应收费用 折合人名币总价
    receivable_expense_total = fields.Monetary(string='receivable expense total',
                                               currency_field='base_money_currency_id',
                                               readonly=True, compute='_company_receivable_expense_total')

    # 应收费用　美元总价
    receivable_expense_usd_total = fields.Monetary(string='receivable expense USD total',
                                                   currency_field='currency_id',
                                                   readonly=True, compute='_company_receivable_expense_more_total')

    # 应收费用 欧元总价
    receivable_expense_eur_total = fields.Monetary(string='receivable expense EUR total',
                                                   currency_field='currency_id',
                                                   readonly=True, compute='_company_receivable_expense_more_total')
    # 应收费用 人名币总价
    receivable_expense_cny_total = fields.Monetary(string='receivable expense CNY total',
                                                   currency_field='currency_id',
                                                   readonly=True, compute='_company_receivable_expense_more_total')

    @api.multi
    @api.depends('base_money_currency_id', 'base_money_amount_total')
    def _company_receivable_expense_total(self):
        """计算应收费用 折合人名币总价"""
        self.receivable_expense_total = sum(line.base_money_amount_total for line in self.receivable_expense_no)

    @api.multi
    @api.depends('currency_id')
    def _company_receivable_expense_more_total(self):
        """分币种统计 计算应收费用 美元总价 欧元总价 人民币总价"""
        usd_obj = self.env.ref('base.USD')
        eur_obj = self.env.ref('base.EUR')
        cny_obj = self.env.ref('base.CNY')
        for line in self.receivable_expense_no:
            if line.currency_id.id == usd_obj.id:
                self.receivable_expense_usd_total += line.original_amount_total
            elif line.currency_id.id == eur_obj.id:
                self.receivable_expense_eur_total += line.original_amount_total
            elif line.currency_id.id == cny_obj.id:
                self.receivable_expense_cny_total += line.original_amount_total

     ###################################################################################

    @api.model
    def create(self, vals):
        """自动生成账单号码"""
        if vals.get('customer_bill_no', _('New')) == _('New'):
            vals['customer_bill_no'] = self.env['ir.sequence'].next_by_code('customer_bill_no') or _('New')

        result = super(CustomerBill, self).create(vals)

    @api.model
    def create(self, vals):
        """创建账单的时候 生成指定格式的账单号"""
        customer_bill_no_pr = 'ZD'
        if vals.get('customer_bill_no', _('New')) == _('New'):
            import pytz
            tz = pytz.timezone('Asia/Shanghai')
            local_time = fields.datetime.now(tz).strftime('%Y%m')
            customer_bill_no = customer_bill_no_pr + local_time
            qsets = self.search([('customer_bill_no', 'like', customer_bill_no + '%')])

            if len(qsets) == 0:
                num = 1
            else:
                name_sets = []
                for i in qsets:
                    s = i.customer_bill_no[-4:]
                    try:
                        name_sets.append(int(s))
                    except ValueError:
                        raise ValidationError(
                            _('The last four num of order occur wrong, please make sure it is numbers'))
                num = max(name_sets) + 1
            vals['customer_bill_no'] = (customer_bill_no + '%04d') % num

        result = super(CustomerBill, self).create(vals)

        return result

    # ('draft', 'Draft'),  # 草稿
    # ('submit', 'Submitted'),  # 待审核
    # ('cancel', 'Refused'),  # 审核未通过
    # ('approve', 'approved'),  # 通过审核
    # ('sent', 'sent'),  # 已发邮件 待对账
    # ('abnormal', 'abnormal'),  # 对账异常
    # ('checked', 'checked'),  # 已对账 待付款
    # ('paid', 'paid'),  # 已付款 待开票
    # ('make-out', 'make-out'),  # 已开票 待销帐
    # ('write-off', 'write-off')  # 已销账

    @api.multi
    def action_submit_check(self):
        """提交审核按钮"""
        self.update({'state': 'submit'})
        for bill_sheet in self:
            body = (_("账单：%s 已提交, 请耐心等待审核 ！<br/>") % (bill_sheet.customer_bill_no))
            bill_sheet.message_post(body=body)

    @api.multi
    def action_resubmit_check(self):
        """重新提交审核按钮"""
        self.update({'state': 'submit'})
        for bill_sheet in self:
            body = (_("账单：%s 已重新提交, 请耐心等待审核 ！<br/>") % (bill_sheet.customer_bill_no))
            bill_sheet.message_post(body=body)

    @api.multi
    def action_approve_bill(self):
        """审核通过"""
        self.update({'state': 'approve'})
        for bill_sheet in self:
            body = (_("账单：%s 已通过审核, 请给客户发送邮件对账单 ！<br/>") % (bill_sheet.customer_bill_no))
            bill_sheet.message_post(body=body)

    @api.multi
    def action_checked_bill(self):
        """对账完成"""
        self.update({'state': 'checked'})
        for bill_sheet in self:
            body = (_("账单：%s 已完成对账, 请联系客户付款 ！<br/>") % (bill_sheet.customer_bill_no))
            bill_sheet.message_post(body=body)

    @api.multi
    def action_paid_bill(self):
        """客户已付款确认按钮"""
        self.update({'state': 'paid'})
        for bill_sheet in self:
            body = (_("账单：%s 客户已完成付款, 请进入开票流程 ！<br/>") % (bill_sheet.customer_bill_no))
            bill_sheet.message_post(body=body)

    @api.multi
    def action_make_out_bill(self):
        """已给客户开票 确认按钮"""
        self.update({'state': 'make-out'})
        for bill_sheet in self:
            body = (_("账单：%s 已给客户开票, 请进入销帐流程 ！<br/>") % (bill_sheet.customer_bill_no))
            bill_sheet.message_post(body=body)

    @api.multi
    def action_write_off_bill(self):
        """已销帐 确认按钮"""
        self.update({'state': 'write-off'})
        for bill_sheet in self:
            body = (_("账单：%s 已完成销帐 ！<br/>") % (bill_sheet.customer_bill_no))
            bill_sheet.message_post(body=body)

    @api.multi
    def action_cancel_write_off(self):
        """取消销帐 按钮"""
        self.update({'state': 'make-out'})
        for bill_sheet in self:
            body = (_("账单：%s 已取消销帐 ！<br/>") % (bill_sheet.customer_bill_no))
            bill_sheet.message_post(body=body)




##################################
    @api.multi
    def cancel_account_review(self):
        """账单视图 取消审核按钮"""
        self.update({'state': 'draft', 'review_remark': ''})

    @api.multi
    def cancel_account_check(self):
        """账单视图 取消对账按钮"""
        self.update({'state': 'reviewed', 'account_checking_remark': ''})

    @api.multi
    def cancel_invoice_make_out(self):
        """账单视图 取消开票按钮"""
        self.update({'state': 'account checked', 'invoice_no': '', 'base_money_invoice_amount': ''})

    @api.multi
    def cancel_account_write_off(self):
        """账单视图 取消销帐按钮"""
        self.update({'state': 'invoice make out', 'write_off_amount': '', 'write_off_remark': ''})


    #######################################################
    # 发送邮件按钮
    @api.multi
    def action_quotation_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('settlement', 'email_template_edi_sale')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'settlement.customer_bill',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "sale.mail_template_data_notification_email_sale_order"
        })
        print(ctx)

        self.filtered(lambda s: s.state == 'approve').update({'state': 'sent'})

        return {
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
    def force_quotation_send(self):
        for order in self:
            email_act = order.action_quotation_send()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                email_ctx.update(default_email_from=order.company_id.email)
                order.with_context(email_ctx).message_post_with_template(email_ctx.get('default_template_id'))
        return True

    @api.multi
    def action_quotation_default_send(self):
        """账单状态审核通过后 就一直显示的普通发送邮件按钮"""
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('settlement', 'email_template_edi_sale')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'settlement.customer_bill',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "sale.mail_template_data_notification_email_sale_order"
        })
        print(ctx)

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


    ###############################################
    # 打印账单
    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self, 'sale.report_saleorder')


class BillAmount(models.Model):
    """ 账单金额_分币种统计"""
    _name = "settlement.bill_amount"
    _description = 'about bill amount'

    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", required=False, )  # 币种
    amount_receivable = fields.Many2one(comodel_name="settlement.customer_bill", string="receivable amount", required=False, )    # 应收金额
    actual_price = fields.Monetary(string="actual price", required=True, readonly=True,)   # 实收金额


class BillType(models.Model):
    """ 账单类型"""
    _name = "settlement.bill_type"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'about bill type'
    _rec_name = "type_name"

    type_name = fields.Char(string="bill type name", required=False, )   # 账单类型名称
    review_remark = fields.Char(string="bill type remark", required=False, )  # 账单类型备注


class AccountRefusedWizard(models.TransientModel):
    """账单状态 审核拒绝 未通过 按钮"""
    _name = 'settlement.submit_refused_wizard'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'bill confirm account review'

    review_remark = fields.Char(string="account review remark", required=False, )  # 未通过审核备注


    @api.multi
    def confirm_submit_refused(self):
        """更新账单模型中的审核备注信息"""
        customer_bill = self.env['settlement.customer_bill'].browse(self._context.get('customer_bill_no'))
        print('*************************1234567*********************************')
        print(customer_bill)
        print(customer_bill.customer_bill_no)
        for item in self:
            customer_bill.review_remark = item.review_remark
            customer_bill.state = 'cancel'
            body = (_("账单：%s 未通过审核 ！<br/><ul class=o_timeline_tracking_value_list><li>Reason<span> : </span><span class=o_timeline_tracking_value>%s</span></li></ul>") % (customer_bill.customer_bill_no, item.review_remark))
            item.message_post(body=body)

        return True


class AccountCheckAbnormalWizard(models.TransientModel):
    """账单状态 对账异常按钮"""
    _name = 'settlement.checked_bill_abnormal_wizard'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'bill confirm account check abnormal'

    account_checking_remark = fields.Char(string="account checking remark", required=False, )  # 对账备注

    @api.multi
    def checked_bill_abnormal(self):
        """更新账单模型中的 账单状态异常 备注信息"""
        customer_bill = self.env['settlement.customer_bill'].browse(self._context.get('customer_bill_no'))

        for item in self:
            # customer_bill.state = 'cancel'
            customer_bill.state = 'abnormal'
            customer_bill.account_checking_remark = item.account_checking_remark
            body = (_("账单：%s 对账状态异常 ！<br/><ul class=o_timeline_tracking_value_list><li>Reason<span> : </span><span class=o_timeline_tracking_value>%s</span></li></ul>") % (
                    customer_bill.customer_bill_no, item.account_checking_remark))
            item.message_post(body=body)

        return True


# class InvoiceMakeOutWizard(models.TransientModel):
#     """账单状态 确认开票按钮"""
#     _name = 'settlement.invoice_make_out_wizard'
#     _description = 'bill confirm invoice make out'
#
#     invoice_no = fields.Char(string="invoice number", required=False, )   # 发票号码
#     base_money_invoice_amount = fields.Float(string="base money invoice amount",
#                                              digits=dp.get_precision('Product Price'),)   # 本位币发票金额
#
#     @api.multi
#     def confirm_invoice_make_out(self):
#         """更新账单模型中 确认开票状态"""
#         customer_bill = self.env['settlement.customer_bill'].browse(self._context.get('customer_bill_no'))
#
#         for item in self:
#             customer_bill.state = 'invoice make out'
#             customer_bill.invoice_no = item.invoice_no
#             customer_bill.base_money_invoice_amount = item.base_money_invoice_amount
#
#         return True


class AccountWriteOffWizard(models.TransientModel):
    """账单状态 销帐按钮"""
    _name = 'settlement.account_write_off_wizard'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'bill confirm account write off'

    write_off_amount = fields.Float(string="base money invoice amount",
                                    digits=dp.get_precision('Product Price'),)  # 本位币销帐金额
    write_off_remark = fields.Text(string="write off remark", required=False, )     # 销帐备注

    @api.multi
    def confirm_account_write_off(self):
        """更新账单模型中 确认销帐"""
        customer_bill = self.env['settlement.customer_bill'].browse(self._context.get('customer_bill_no'))

        for item in self:
            customer_bill.state = 'write-off'
            customer_bill.write_off_amount = item.write_off_amount
            customer_bill.write_off_remark = item.write_off_remark
            body = (_("账单：%s 已销帐 ！<br/><ul class=o_timeline_tracking_value_list><li>Reason<span> : </span><span class=o_timeline_tracking_value>%s</span></li></ul>") % (
                    customer_bill.customer_bill_no, item.write_off_remark))
            item.message_post(body=body)
        return True


class ExpensePayable(models.Model):
    """ 应付费用"""
    _name = "settlement.expense_payable"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'about expense payable'
    # _rec_name = "expense_payable_sheet_id"
    #
    # expense_payable_sheet_id = fields.Char(string='expense payable Sheet ID', required=True, copy=False,
    #                                           state={'draft': [('readonly', False)]},
    #                                           default=lambda self: _('New'))   # 应付费用单号
    expense_statement_no = fields.Many2one(comodel_name='settlement.expense_statement',
                                           string='expense statement')  # 结算单号
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)],
                                 change_default=True, ondelete='restrict', required=True)  # 产品ID 费用
    qty = fields.Integer(string="quantity", required=False, default=1)  # 数量
    unit_price = fields.Float(string="unit price", required=False, )  # 原币种单价
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", required=True,  default=lambda self: self._get_user_currency())  # 多币种 默认为人民币 本位币
    rate = fields.Float(string="Rate", related='currency_id.rate', required=False, readonly=True, )  # 汇率
    base_money_unit_price = fields.Monetary(compute='_compute_price_unit', string="base money unit price",
                                            required=True, readonly=True, )  # 本位币单价
    base_money_currency_id = fields.Many2one('res.currency', string='Currency', required=True, readonly=True,
                                             default=lambda self: self._get_user_currency())  # 本位币币种
    payment_application_no = fields.Many2one(comodel_name="settlement.pay_apply_sheet",
                                                string="payment application sheet number", required=False, )  # 关联付款申请单
    # 备注 创建人 创建时间 系统自带 不需要创建

    # 需要显示的其他模型的字段
    # ExpenseStatement
    work_sheet_no = fields.Many2one(related='expense_statement_no.work_sheet_no', string="work_sheet_no", required=False)     # 工作单号
    customer_id = fields.Many2one(related='expense_statement_no.customer_id', string="Customer", required=True,
                               domain=[('is_company', '=', True), ('customer', '=', True)])   # 客户

    # 应付费用状态 是否已经添加到付款申请单
    expense_payable_status = fields.Boolean(compute='_generate_pay_apply_sheet', string="payable expense add application Status", default=False, readonly=True )  # 应付费用状态

    # 付款申请单状态
    application_sheet_state = fields.Selection(related='payment_application_no.state', string='status', readonly=True)
    # 付款单位
    payment_company_name = fields.Many2one(comodel_name="res.partner", string="Settlement Object",
                                           required=True, )  # 付款公司名称

    # 原币种单条总价 = 原币种单价 X 数量
    original_amount_total = fields.Monetary(compute='_compute_total_original_price',
                                            string="original total price", required=True, readonly=True,)
    # 本位币单条总价 = 本位币单价 X 数量
    base_money_amount_total = fields.Monetary(compute='_compute_total_base_money_price',
                                              string="base money total price", required=True, readonly=True,)

    @api.onchange('rate', 'unit_price')
    def _compute_price_unit(self):
        """根据所选币种的汇率计算出本位币单价"""
        for receivable_expense in self:
            if receivable_expense.rate != 0:
                receivable_expense.base_money_unit_price = receivable_expense.unit_price / receivable_expense.rate

    @api.onchange('qty', 'unit_price')
    def _compute_total_original_price(self):
        """根据当前服务的原币种单价 X 数量 计算出原币种总价"""
        for receivable_expense in self:
            if receivable_expense.qty != 0:
                receivable_expense.original_amount_total = receivable_expense.qty * receivable_expense.unit_price

    @api.onchange('qty', 'base_money_unit_price')
    def _compute_total_base_money_price(self):
        """根据当前服务的本位币单价 X 数量 计算出单行本位币总价"""
        for receivable_expense in self:
            if receivable_expense.qty != 0:
                receivable_expense.base_money_amount_total = receivable_expense.qty * receivable_expense.base_money_unit_price

    @api.model
    def _get_euro(self):
        return self.env['res.currency.rate'].search([('rate', '=', 1)], limit=1).currency_id

    @api.model
    def _get_user_currency(self):
        """获取当前用户所在公司的币种 作为默认的本位币币种"""
        currency_id = self.env['res.users'].browse(self._uid).company_id.currency_id
        return currency_id or self._get_euro()

    @api.multi
    def generate_pay_apply_sheet(self):
        """批量生成付款申请单"""
        if len(self.mapped('payment_company_name')) != 1:
            # raise UserError(
            #     _("You cannot generate account bill for different settlement object in the same account bill!"))
            raise UserError(_("同一个付款申请单中不能含有不同的结算对象，请重新选择！"))
        # for payment_expense in self:
        #     payment_expense.expense_payable_status = True
            # for_settlement_object = receivable_expense.settlement_object

        for pay_apply_sheet in self:
            if pay_apply_sheet.expense_payable_status:
                raise UserError(
                    _("您选择的应付费用列表中，含有已生成付款申请单的费用，请重新选择!"))

        default_payment_company_name = self.mapped('payment_company_name')[0]

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'settlement.pay_apply_sheet',
            'target': 'current',
            'context': {
                'default_expense_payable_no': self.ids,
                'default_payment_company_name': default_payment_company_name.id
            }
        }

    @api.multi
    def add_pay_apply_sheet(self):
        pass

    @api.onchange('payment_application_no')
    def _generate_pay_apply_sheet(self):
        """根据当前付款申请单字段是否为空  判断是否已经生成了付款申请单 然后修改应付费用的状态"""
        for pay_apply_sheet in self:
            if pay_apply_sheet.payment_application_no:
                pay_apply_sheet.expense_payable_status = True
            else:
                pay_apply_sheet.expense_payable_status = False


class PaymentApplicationSheet(models.Model):
    """ 付款申请单"""
    _name = "settlement.pay_apply_sheet"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'about payment application sheet'
    _rec_name = "payment_application_no"

    payment_application_no = fields.Char(string="payment application number", required=False, )  # 付款申请单号
    payment_method = fields.Many2one(comodel_name="settlement.payment_method",
                                string="payment method", required=False, )   # 付款方式
    payment_company_name = fields.Many2one(comodel_name="res.partner", string="Settlement Object",
                                           required=False, )  # 付款公司名称
    supplier_invoice_no = fields.Char(string="supplier invoice number", required=False, )  # 供应商发票号
    base_money_payment_amount = fields.Float(string="base money payment amount",
                                             digits=dp.get_precision('Product Price'),)   # 本位币付款金额
    application_remark = fields.Text(string="application remark", required=False, )     # 申请审核备注
    review_remark = fields.Text(string="review remark", required=False, )     # 审核备注
    payment_remark = fields.Text(string="payment remark", required=False, )     # 支付备注
    state = fields.Selection(selection=[('draft', 'Draft'),    # 草稿
                                        ('submitted', 'Submitted'),  # 已提交
                                        ('reviewed', 'Reviewed'),  # 已审核
                                        ('paid', 'Paid'),     # 已付款
                                        ], string='status', readonly=True, default='draft')
    expense_payable_no = fields.One2many(comodel_name="settlement.expense_payable", inverse_name="payment_application_no",
                                         string="expense payable", required=False, )  # 应付费用ID

    payment_amount = fields.One2many(comodel_name="settlement.payment_amount", inverse_name="amount_payment",
                                     string="payment amount", required=False, )  # 关联付款金额
    ###############################################################################
    # 增加附件上传功能
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')


    ################################################################################
    # 关联显示 应付费用的相关字段
    pay_currency_id = fields.Many2one(related='expense_payable_no.currency_id', string="Currency",
                                      required=False, )  # 原商品币种
    pay_base_money_currency_id = fields.Many2one(related='expense_payable_no.base_money_currency_id',
                                                 string='Base Currency',)  # 本位币币种
    # 原币种单行总价
    pay_original_amount_total = fields.Monetary(related='expense_payable_no.original_amount_total',
                                                string="original total price", required=True, )
    # 本位币单行总价
    pay_base_money_amount_total = fields.Monetary(related='expense_payable_no.base_money_amount_total',
                                                  string="base money total price", required=True, )

    # 应付费用 折合人名币总价
    expense_payable_total = fields.Monetary(string='expense payable total',
                                            currency_field='pay_base_money_currency_id',
                                            readonly=True, compute='_company_expense_payable_total')

    # 应付费用　美元总价
    expense_payable_usd_total = fields.Monetary(string='expense payable USD total',
                                                currency_field='pay_currency_id',
                                                readonly=True, compute='_company_expense_payable_more_total')

    # 应付费用 欧元总价
    expense_payable_eur_total = fields.Monetary(string='expense payable  EUR total',
                                                currency_field='pay_currency_id',
                                                readonly=True, compute='_company_expense_payable_more_total')
    # 应付费用 人名币总价
    expense_payable_cny_total = fields.Monetary(string='expense payable CNY total',
                                                currency_field='pay_currency_id',
                                                readonly=True, compute='_company_expense_payable_more_total')

    # 计算应付费用 折合人名币总价

    @api.multi
    @api.depends('pay_base_money_currency_id', 'pay_base_money_amount_total')
    def _company_expense_payable_total(self):
        self.expense_payable_total = sum(line.base_money_amount_total for line in self.expense_payable_no)

    # 分币种统计 计算应付费用 美元总价 欧元总价 人民币总价

    @api.multi
    @api.depends('pay_currency_id', 'pay_original_amount_total')
    def _company_expense_payable_more_total(self):
        usd_obj = self.env.ref('base.USD')
        eur_obj = self.env.ref('base.EUR')
        cny_obj = self.env.ref('base.CNY')
        for line in self.expense_payable_no:
            if line.currency_id.id == usd_obj.id:
                self.expense_payable_usd_total += line.original_amount_total
            elif line.currency_id.id == eur_obj.id:
                self.expense_payable_eur_total += line.original_amount_total
            elif line.currency_id.id == cny_obj.id:
                self.expense_payable_cny_total += line.original_amount_total


    #######################################################################################

    @api.model
    def create(self, vals):
        """创建付款申请单的时候 生成指定格式的付款申请单号"""
        payment_application_no_pr = 'FKD'
        if vals.get('payment_application_no', _('New')) == _('New'):
            import pytz
            tz = pytz.timezone('Asia/Shanghai')
            local_time = fields.datetime.now(tz).strftime('%Y%m')
            payment_application_no = payment_application_no_pr + local_time
            qsets = self.search([('payment_application_no', 'like', payment_application_no + '%')])

            if len(qsets) == 0:
                num = 1
            else:
                name_sets = []
                for i in qsets:
                    s = i.payment_application_no[-4:]
                    try:
                        name_sets.append(int(s))
                    except ValueError:
                        raise ValidationError(
                            _('The last four num of order occur wrong, please make sure it is numbers'))
                num = max(name_sets) + 1
            vals['payment_application_no'] = (payment_application_no + '%04d') % num

        result = super(PaymentApplicationSheet, self).create(vals)

        return result

    @api.multi
    def _compute_attachment_number(self):
        """附件上传"""
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'settlement.pay_apply_sheet'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)

    @api.multi
    def action_get_attachment_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'settlement.pay_apply_sheet'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'settlement.pay_apply_sheet', 'default_res_id': self.id}
        return res

    @api.multi
    def btn_cancel_submit_audit(self):
        """付款申请单视图 撤销提交审核按钮"""
        self.update({'state': 'draft', 'application_remark': ''})

    @api.multi
    def btn_cancel_audited(self):
        """付款申请单视图 撤销审核按钮"""
        self.update({'state': 'submitted', 'review_remark': ''})

    @api.multi
    def btn_cancel_payment(self):
        """付款申请单视图 撤销支付按钮"""
        self.update({'state': 'reviewed', 'payment_remark': '', 'base_money_payment_amount': ''})


class SubmitAuditWizard(models.TransientModel):
    """付款申请单状态 提交审核申请按钮"""
    _name = 'settlement.submit_audit_wizard'
    _description = 'payment amount submit audit'

    application_remark = fields.Char(string="submit application remark", required=False, )  # 提交审核备注

    @api.multi
    def confirm_submit_audit(self):
        """更新付款申请单模型中的 提交审核申请备注信息"""
        pay_apply_sheet = self.env['settlement.pay_apply_sheet'].browse(self._context.get('payment_application_no'))

        for item in self:
            pay_apply_sheet.state = 'submitted'
            pay_apply_sheet.application_remark = item.application_remark

        return True


class PassAuditWizard(models.TransientModel):
    """付款申请单状态 通过审核按钮"""
    _name = 'settlement.pass_audit_wizard'
    _description = 'payment amount pass audit'

    review_remark = fields.Char(string="pass audit remark", required=False, )  # 通过审核备注

    @api.multi
    def confirm_pass_audit(self):
        """更新付款申请单模型中的 通过审核备注信息"""
        pay_apply_sheet = self.env['settlement.pay_apply_sheet'].browse(self._context.get('payment_application_no'))

        for item in self:
            pay_apply_sheet.state = 'reviewed'
            pay_apply_sheet.review_remark = item.review_remark

        return True


class ConfirmPaymentWizard(models.TransientModel):
    """付款申请单状态 确认支付按钮"""
    _name = 'settlement.confirm_payment_wizard'
    _description = 'payment amount confirm payment'

    base_money_payment_amount = fields.Float(string="base money payment amount",
                                             digits=dp.get_precision('Product Price'),)   # 本位币付款金额
    payment_remark = fields.Text(string="payment remark", required=False, )  # 支付备注

    @api.multi
    def confirm_payment(self):
        """更新付款申请单模型中的 确认支付备注信息"""
        pay_apply_sheet = self.env['settlement.pay_apply_sheet'].browse(self._context.get('payment_application_no'))

        for item in self:
            pay_apply_sheet.state = 'paid'
            pay_apply_sheet.base_money_payment_amount = item.base_money_payment_amount
            pay_apply_sheet.payment_remark = item.payment_remark

        return True


class PaymentAmount(models.Model):
    """ 付款金额"""
    _name = "settlement.payment_amount"
    _description = 'about payment amount'

    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", required=False, )  # 币种
    amount_payment = fields.Many2one(comodel_name="settlement.pay_apply_sheet", string="payment amount", required=False, )    # 应付金额
    actual_price = fields.Monetary(string="actual price", required=True, readonly=True,)   # 实收金额


class PaymentMethod(models.Model):
    """ 付款方式"""
    _name = "settlement.payment_method"
    _description = 'about payment method'
    _rec_name = "payment_method"

    payment_method = fields.Char(string="bill type name", required=False, )   # 付款方式







