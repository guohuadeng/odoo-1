# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
from collections import OrderedDict
_logger = logging.getLogger(__name__)


class CustomsOrder(models.Model):
    """ 通关清单 """
    _name = 'customs_center.customs_order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'name'
    _description = 'Customs Customs Order'

    name = fields.Char(string="Name")   # 通关清单流水号
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")                 # 客户 (委托单位)
    work_sheet_id = fields.Many2one(comodel_name="work_sheet", string="Work Sheet")              # 工作单ID

    inout = fields.Selection(string="InOut", selection=[('i', 'Import'), ('e', 'Export'), ], required=True)   # 进出口类型
    customs_id = fields.Many2one(comodel_name="delegate_customs", string="Customs")              # 进出口岸
    custom_master_id = fields.Many2one(comodel_name="delegate_customs", string="Declare Customs")  # 申报口岸/海关
    ManualNo = fields.Char(string="Manual No")                                                   # 备案号
    customer_contract_no = fields.Char(string="Customer Contract No")                            # 合同号
    LicenseNo = fields.Char(string="License No")                                                 # 许可证号

    business_company_id = fields.Char(string="business company name")                            # 收发货人 新建企业库表
    input_company_id = fields.Char(string="input company id")                                    # 生产消费单位 新建企业库表
    declare_company_id = fields.Char(string="declare company name")                              # 申报单位 新建企业库表

    transport_mode_id = fields.Many2one(comodel_name="delegate_transport_mode",
                                        string="Transport Mode")                                 # 运输方式
    transport_name = fields.Char(string="transport name")                                        # 运输工具名称
    VoyageNo = fields.Char(string="Voyage No")                                                   # 航次号

    trade_terms_id = fields.Many2one(comodel_name="delegate_trade_terms", string="Trade Term")   # 成交方式 or 贸易条款
    trade_mode_id = fields.Many2one(comodel_name="delegate_trade_mode", string="Trade Mode")     # 监管方式
    CutMode_id = fields.Char(string="CutMode id")                                                # 征免性质   征免性质表待新建
    packing_id = fields.Many2one(comodel_name="delegate_packing", string="Package Type")         # 包装方式
    trade_country_id = fields.Many2one(comodel_name="delegate_country",
                                       string="Trade Country")                                   # 贸易国别
    origin_arrival_country_id = fields.Many2one(comodel_name="delegate_country",
                                                string="Origin Arrival Country")                 # 启运/抵达国
    port_id = fields.Many2one(comodel_name="delegate_port", string="Port", )                     # 装货/指运港
    region_id = fields.Many2one(comodel_name="delegate_region", string="Region")                 # 境内目的/货源地
    qty = fields.Integer(string="Qty")                                                           # 件数
    gross_weight = fields.Float(string="Gross Weight")                                           # 毛重
    net_weight = fields.Float(string="Net Weight")                                               # 净重
    marks = fields.Text(string="Marks")                                                          # 标记备注

    # 关联报关单 1对多关系
    customs_declaration_ids = fields.One2many(comodel_name="customs_center.customs_dec",
                                              inverse_name="customs_order_id", string="customs declaration")
    # 关联通关清单商品列表 1对多关系
    cus_goods_list_ids = fields.One2many(comodel_name="customs_center.cus_goods_list",
                                         inverse_name="customs_order_id", string="cus goods name")
    customs_order_state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], default='draft')  # 通关清单

    @api.model
    def generate_customs_declaration(self):
        """ 生成报关单 """
        pass

    @api.model
    def create(self, vals):
        """设置原始清单命名规则"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('code_customs_order') or _('New')
        result = super(CustomsOrder, self).create(vals)

        return result


class WorkSheet(models.Model):
    """" 工作单 """
    _inherit = 'work_sheet'

    customs_order_ids = fields.One2many(comodel_name="customs_center.customs_order", inverse_name="work_sheet_id",
                                          string="Customs Order")
    customs_order_state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], compute='_get_customs_state')

    @api.depends('customs_order_ids')
    def _get_customs_state(self):
        """ 获取当前工作单对应的通关清单 状态"""
        for sheet in self:
            if sheet.customs_order_ids:
                customs_obj = sheet.customs_order_ids[0]
                sheet.customs_order_state = customs_obj.customs_order_state

    @api.constrains('customs_order_ids')
    def _check_clearance_one2one(self):
        """ 工作单 关联通关清单 一对一唯一约束校验"""
        for item in self:
            if len(item.customs_order_ids) > 1:
                raise ValidationError(_('work sheet must relate only one clearance draft'))








