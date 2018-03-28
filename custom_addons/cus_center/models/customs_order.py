# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CustomsOrder(models.Model):
    """ 通关清单 """
    _name = 'cus_center.cus_order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'name'
    _description = 'Customs Order'

    name = fields.Char(string="Name", copy=False)   # 通关清单流水号
    # customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")                 # 客户 (委托单位)

    inout = fields.Selection(string="InOut", selection=[('i', u'进口'), ('e', u'出口'), ], required=True)   # 进出口类型
    customs_id = fields.Many2one(comodel_name="cus_args.customs", string="Customs")              # 进出口岸
    custom_master_id = fields.Many2one(comodel_name="cus_args.customs", string="Declare Customs")  # 申报口岸/海关
    ManualNo = fields.Char(string="Manual No")                                                   # 备案号
    customer_contract_no = fields.Char(string="Customer Contract No")                            # 合同号
    licenseNo = fields.Char(string="License No")                                                 # 许可证号
    declare_company_id = fields.Many2one(comodel_name="cus_args.register_company", string="declare company name")  # 申报单位
    input_company_id = fields.Many2one(comodel_name="cus_args.register_company", string="input company id")  # 消费使用单位
    business_company_id = fields.Many2one(comodel_name="cus_args.register_company", string="business company name")    # 收发货人

    transport_mode_id = fields.Many2one(comodel_name="cus_args.transport_mode",
                                       string="Transport Mode")                                 # 运输方式
    transport_name = fields.Char(string="transport name")                                        # 运输工具名称
    VoyageNo = fields.Char(string="Voyage No")                                                   # 航次号

    trade_terms_id = fields.Many2one(comodel_name="cus_args.trade_terms", string="Trade Term")   # 成交方式 or 贸易条款
    trade_mode_id = fields.Many2one(comodel_name="cus_args.trade_mode", string="Trade Mode")     # 监管方式
    CutMode_id = fields.Many2one(comodel_name="cus_args.cut_mode", string="CutMode id")      # 征免性质   征免性质表待新建
    packing_id = fields.Many2one(comodel_name="cus_args.packing", string="Package Type")         # 包装方式
    trade_country_id = fields.Many2one(comodel_name="cus_args.country",
                                       string="Trade Country")                                   # 贸易国别
    origin_arrival_country_id = fields.Many2one(comodel_name="cus_args.country",
                                                string="Origin Arrival Country")                 # 启运/抵达国
    port_id = fields.Many2one(comodel_name="cus_args.port", string="Port", )                     # 装货/指运港
    region_id = fields.Many2one(comodel_name="cus_args.region", string="Region")                 # 境内目的/货源地
    qty = fields.Integer(string="Qty")                                                           # 件数
    gross_weight = fields.Float(string="Gross Weight")                                           # 毛重
    net_weight = fields.Float(string="Net Weight")                                               # 净重
    marks = fields.Text(string="Marks")                                                          # 标记备注

    # 关联报关单 1对多关系
    # customs_declaration_ids = fields.One2many(comodel_name="",
    #                                           inverse_name="", string="customs declaration")
    # 关联通关清单商品列表 1对多关系
    # cus_goods_list_ids = fields.One2many(comodel_name="",
    #                                      inverse_name="", string="cus goods name")
    state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], default='draft')  # 通关清单状态
    # custom_count = fields.Integer(string='Custom Declaration', compute='_get_custom_count')

