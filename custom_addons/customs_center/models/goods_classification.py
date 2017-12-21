# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class GoodsClassification(models.Model):
    """ 商品归类（合规）"""
    _name = 'customs_center.goods_classify'
    _rec_name = 'cus_goods_code'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Goods Classification'

    cus_goods_code = fields.Char(string="Customer Goods Code", required=False, index=True)     # 客户料号
    # 关联商品列表
    dec_goods_list_ids = fields.One2many(comodel_name="customs_center.cus_goods_list",
                                         inverse_name="cus_goods_tariff_id", string="dec goods name")

    business_company_id = fields.Many2one(comodel_name="basedata.cus_register_company",
                                          string="business company name")  # 收发货人 / 经营单位
    cus_goods_tariff_id = fields.Many2one(comodel_name="basedata.cus_goods_tariff", string="cus goods Code TS", required=False, )  # 海关税则编码 / 商品编号 Code_ts 即 hs_code
    goods_name = fields.Char(string="goods name")  # 商品名称

    @api.onchange('cus_goods_tariff_id')
    def _generate_about_name(self):
        """根据当前海关税则编码的变化 改变商品名称 并通过onchange装饰器，自动执行_generate_about_name方法"""
        for goods_list in self:
            if goods_list.cus_goods_tariff_id:
                goods_list.goods_name = goods_list.cus_goods_tariff_id.NameCN

    goods_model = fields.Char(string="goods model", required=False, )  # 规格型号
    first_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="First Unit", )  # 第一计量单位
    second_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="second Unit", )  # 第二计量单位

    deal_unit_price = fields.Monetary(string="deal unit price", )  # 成交单价/申报单价
    currency_id = fields.Many2one(comodel_name="basedata.cus_currency", string="currency id", required=False, )  # 币制
    origin_country_id = fields.Many2one(comodel_name="delegate_country", string="origin country", )  # 原产国
    destination_country_id = fields.Many2one(comodel_name="delegate_country", string="destination country", )  # 目的国

    supervision_condition = fields.Char(string="supervision condition")  # 监管标识

    @api.onchange('cus_goods_tariff_id')
    def _generate_about_name(self):
        """根据当前海关税则编码的变化 改变监管条件 并通过onchange装饰器，自动执行_generate_about_name方法"""
        for goods_list in self:
            if goods_list.cus_goods_tariff_id:
                goods_list.goods_name = goods_list.cus_goods_tariff_id.NameCN
                goods_list.supervision_condition = goods_list.cus_goods_tariff_id.supervision_condition

    duty_mode_id = fields.Many2one(comodel_name="basedata.cus_duty_mode", string="Duty Mode", )  # 征免方式
    ManualNo = fields.Char(string="Manual No")  # 备案号 / 账册号
    ManualSN = fields.Char(string="Manual SN")  # 备案序号

    state = fields.Selection(selection=[('draft', 'Draft'),    # 草稿
                                        ('unsubmit', 'Unsubmit'),  # 待提交
                                        ('check_pending', 'Check Pending'),  # 待审核
                                        ('refused', 'Refused'),  # 审核不通过
                                        ('approve', 'approved')  # 通过审核
                                        ], string='status', readonly=True, default='draft')

    @api.multi
    def submit_review_btn(self):
        """ 商品归类信息提交审核 按钮"""
        pass

