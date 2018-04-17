# -*- coding: utf-8 -*-

from odoo import models,fields,api, _
import odoo.exceptions
import logging
_logger = logging.getLogger(__name__)

class ComplianceModel(models.Model):
    """清单模板"""
    _name = 'compliance.model'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'name_model'
    _description = 'Compliance Model'

    #模板名称
    name_model = fields.Char(string="Model Name",required=True)
    """以下为模版内的相关信息"""

    inout = fields.Selection(string="InOut", selection=[('i', u'进口'), ('e', u'出口'), ], required=True)   # 境内目的/货源地

    customs_id = fields.Many2one(comodel_name="cus_args.customs", string="Customs") # 进出口岸

    manual_no = fields.Char(string="Manual No")  # 备案号

    customer_contract_no = fields.Char(string="Customer Contract No")   # 合同号

    license_no = fields.Char(string="License No")    # 许可证号

    business_company_id = fields.Char(string="business company name")   # 客户公司

    transport_mode_id = fields.Many2one(comodel_name="cus_args.transport_mode", string="Transport Mode")    # 运输方式

    transport_name = fields.Char(string="transport name")   # 运输工具名称

    voyage_no = fields.Char(string="Voyage No")  # 航次号

    trade_terms_id = fields.Many2one(comodel_name="cus_args.trade_terms", string="Trade Term")  # 成交方式 or 贸易条款

    trade_mode_id = fields.Many2one(comodel_name="cus_args.trade_mode", string="Trade Mode")    # 监管方式

    cut_mode_id = fields.Many2one(comodel_name="cus_args.cut_mode", string="CutMode id") # 征免性质   征免性质表待新建

    packing_id = fields.Many2one(comodel_name="cus_args.wrap_type", string="Package Type")    # 包装方式

    trade_country_id = fields.Many2one(comodel_name="cus_args.country", string="Trade Country") # 贸易国别

    origin_arrival_country_id = fields.Many2one(comodel_name="cus_args.country", string="Origin Arrival Country")   # 启运/抵达国

    port_id = fields.Many2one(comodel_name="cus_args.port", string="Port")  # 装货/指运港

    region_id = fields.Many2one(comodel_name="cus_args.internal_district", string="Region")    # 境内目的/货源地
