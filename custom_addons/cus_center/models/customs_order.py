# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CustomsOrder(models.Model):
    """ 通关清单 """
    _name = 'cus_center.customs_order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'name'
    _description = 'Customs Order'

    name = fields.Char(string="Name", copy=False)  # 通关清单流水号
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")  # 客户 (委托单位)
    custom_master_id = fields.Many2one(comodel_name="cus_args.customs", string="Declare Customs")  # 申报地海关
    work_sheet_id = fields.Many2one(comodel_name="work_sheet", string="Work Sheet")  # 工作单ID

    inout = fields.Selection(string="InOut", selection=[('i', u'进口'), ('e', u'出口'), ], required=True)  # 进出口类型
    customs_id = fields.Many2one(comodel_name="cus_args.customs", string="InOut Customs")  # 进出口岸

    manual_no = fields.Char(string="Manual No")  # 备案号
    customer_contract_no = fields.Char(string="Customer Contract No")  # 合同协议号
    license_no = fields.Char(string="License No")  # 许可证号

    input_company_id = fields.Many2one(comodel_name="cus_args.register_company", string="Input Company")  # 消费使用单位
    business_company_id = fields.Many2one(comodel_name="cus_args.register_company",
                                          string="business company name")  # 收发货人
    declare_company_id = fields.Many2one(comodel_name="cus_args.register_company",
                                         string="Declare Company Name")  # 申报单位

    transport_mode_id = fields.Many2one(comodel_name="cus_args.transport_mode",
                                        string="Transport Mode")  # 运输方式
    transport_name = fields.Char(string="Transport Name")  # 运输工具名称
    voyage_no = fields.Char(string="Voyage No")  # 航次号

    origin_arrival_country_id = fields.Many2one(comodel_name="cus_args.country",
                                                string="Origin Arrival Country")  # 启运国/抵达国
    port_id = fields.Many2one(comodel_name="cus_args.port", string="Port", )  # 装货港/指运港
    internal_district_id = fields.Many2one(comodel_name="cus_args.internal_district",
                                           string="Internal District")  # 境内目的地/货源地

    trade_country_id = fields.Many2one(comodel_name="cus_args.country",
                                       string="Trade Country")  # 贸易国别
    trade_terms_id = fields.Many2one(comodel_name="cus_args.trade_terms", string="Trade Term")  # 成交方式
    qty = fields.Integer(string="Qty")  # 件数

    wrap_type_id = fields.Many2one(comodel_name="cus_args.wrap_type", string="Wrap Type")  # 包装方式
    gross_weight = fields.Float(string="Gross Weight")  # 毛重
    net_weight = fields.Float(string="Net Weight")  # 净重

    marks = fields.Text(string="Marks")  # 标记备注

    # 关联通关清单商品列表
    order_goods_list = fields.One2many(comodel_name="cus_center.order_goods_list", inverse_name="customs_order_id", )

    # 关联报关单列表
    customs_dec_list = fields.One2many(comodel_name="cus_center.customs_dec",
                                       inverse_name="customs_order_id", )
    # 关联的报关单数量
    custom_dec_list_count = fields.Integer(string='Custom Declaration',
                                           compute='_get_custom_dec_list_count')

    state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('cancel', 'Cancel')], default='draft')  # 通关清单状态

    @api.depends('customs_dec_list')
    def _get_custom_dec_list_count(self):
        self.custom_dec_list_count = len(self.customs_dec_list.ids)

    @api.model
    def create(self, vals):
        """设置通关清单命名规则"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('code_customs_order') or _('New')
        result = super(CustomsOrder, self).create(vals)
        return result
