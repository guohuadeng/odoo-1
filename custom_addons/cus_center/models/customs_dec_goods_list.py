# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DecGoodsList(models.Model):
    """ 通关清单 -商品列表 """
    _name = 'cus_center.dec_goods_list'
    # rec_name = 'goods_name'D
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Customs Dec Goods List'

    # 关联通关清单 多对一
    customs_dec_id = fields.Many2one(comodel_name="cus_center.customs_dec", string="Customs Declaration", copy=False)

    sequence = fields.Integer(string='Sequence')   # 商品序号

    # 关联商品归类信息
    goods_classification_id = fields.Many2one(comodel_name="cus_center.goods_classify", string="Goods Classification",
                                              required=False, )  # 客户料号搜索字段

    cust_goods_code = fields.Char(string="Customer Goods Code", related='goods_classification_id.cust_goods_code',
                                  store=False)  # 客户料号 录入字段

    manual_sn = fields.Char(string="Manual SN")  # 备案序号
    goods_tariff_id = fields.Many2one(comodel_name="cus_args.goods_tariff", string="HS Code",
                                      required=False, )  # 海关税则编码

    goods_name = fields.Char(string="Goods Name")  # 商品名称
    goods_model = fields.Char(string="Goods Model", required=False, )  # 规格型号

    deal_qty = fields.Float(string="Deal Quantity", required=False, default=1)  # 成交数量
    deal_unit_price = fields.Float(string="Deal Unit Price", )  # 成交单价/申报单价
    deal_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="Deal Unit", required=False, )  # 成交单位
    deal_total_price = fields.Float(compute='_compute_total_goods_price', string="Deal Total Price", )  # 成交总价

    @api.onchange('deal_qty', 'deal_unit_price')
    def _compute_total_goods_price(self):
        """根据当前商品列表的成交单价 X 成交数量数量 计算出商品单行总价"""
        for goods_list in self:
            if goods_list.deal_qty != 0:
                goods_list.deal_total_price = goods_list.deal_qty * goods_list.deal_unit_price

    currency_id = fields.Many2one(comodel_name="cus_args.currency", string="Currency", required=False, )  # 币制

    first_qty = fields.Float(string="first quantity", required=False, )  # 第一法定数量
    first_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="First Unit", )  # 第一计量单位

    second_qty = fields.Float(string="second quantity", )  # 第二法定数量
    second_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="second Unit", )  # 第二计量单位

    supervision_condition = fields.Char(string="supervision condition")  # 监管标识/监管标识

    origin_country_id = fields.Many2one(comodel_name="cus_args.country", string="origin country", )  # 原产国
    destination_country_id = fields.Many2one(comodel_name="cus_args.country", string="destination country", )  # 目的国
    duty_mode_id = fields.Many2one(comodel_name="cus_args.duty_mode", string="Duty Mode", )  # 征免方式

    version_no = fields.Char(string="Version No")  # 版本号
    product_no = fields.Char(string="Product No")  # 货号

    @api.onchange('goods_tariff_id')
    def _generate_about_name(self):
        """根据当前海关税则编码的变化 改变商品名称 并通过onchange装饰器，自动执行_generate_about_name方法"""
        for goods in self:
            if goods.goods_tariff_id:
                # 增加一个判断goods_classification_id是否为真 因为如果料号变化之后 商品编号会变，商品名称也会变，
                # 而本方法同样有这样的功能，如果料号变了，商品编号也变，商品名称显示的就是税则库中的名称
                # 而不是归类库中的名称了

                if goods.goods_classification_id:
                    break
                goods.goods_name = goods.goods_tariff_id.name_cn
                goods.first_unit_id = goods.goods_tariff_id.first_unit_id
                goods.second_unit_id = goods.goods_tariff_id.second_unit_id
                goods.supervision_condition = goods.goods_tariff_id.supervision_condition

    @api.onchange('goods_classification_id')
    def _generate_about_goods_info(self):
        """根据当前合规客户料号的变化 改变商品名称 商品编码等信息 并通过onchange装饰器，自动执行_generate_about_name方法"""
        for goods in self:
            if goods.goods_classification_id:
                goods.goods_tariff_id = goods.goods_classification_id.goods_tariff_id
                goods.manual_sn = goods.goods_classification_id.manual_sn
                goods.goods_name = goods.goods_classification_id.goods_name
                goods.goods_model = goods.goods_classification_id.goods_model
                goods.deal_unit_id = goods.goods_classification_id.deal_unit_id
                goods.deal_unit_price = goods.goods_classification_id.deal_unit_price
                goods.first_unit_id = goods.goods_classification_id.first_unit_id
                goods.second_unit_id = goods.goods_classification_id.second_unit_id
                goods.origin_country_id = goods.goods_classification_id.origin_country_id
                goods.destination_country_id = goods.goods_classification_id.destination_country_id
                goods.duty_mode_id = goods.goods_classification_id.duty_mode_id
                goods.supervision_condition = goods.goods_classification_id.supervision_condition