# -*- coding: utf-8 -*-

from odoo import models,fields,api, _
import odoo.exceptions
import logging
_logger = logging.getLogger(__name__)

class GoodsCompliance(models.Model):
    """货物合规"""
    _name = 'goods.compliance'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'custom_part_number'
    _description = 'Goods Companlice'


    custom_part_number = fields.Char(string="Goods Compliance", required=False, copy=False) # 企业料号

    spec_description = fields.Char(string="Spec Description")   # 规格描述

    identification_goods = fields.Char(string="Identify Goods") # 货物标识

    goods_code = fields.Many2one(comodel_name="cus_args.goods_tariff", string="HS Goods Code", required=True, ) # 商品编码

    chinese_name = fields.Char(string="Chinese Name")   # 中文名称

    # business_company_id = fields.Many2one(comodel_name="cus_args.register_company", string="business company name", required=True)  # 收发货人 / 经营单位

    goods_model = fields.Char(string="Goods model", required=False, )   # 规格型号

    declare_unit_price = fields.Float(string="Declare unit price", )    # 申报单价

    currency_id = fields.Many2one(comodel_name="cus_args.currency", string="Currency id", required=False, ) # 币制

    supervision_condition = fields.Char(string="Supervision condition", related='goods_code.supervision_condition', store=False)    # 监管标识/监管标识

    origin_country_id = fields.Many2one(comodel_name="cus_args.country", string="Origin country", ) # 原产国/目的国

    origin_country_id_us = fields.Many2one(comodel_name="cus_args.country",string="Origin country english") # 原产国/目的国英文

    deal_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="Deal unit", required=False)    # 成交单位

    first_unit = fields.Many2one(comodel_name="cus_args.unit", related='goods_code.first_unit_id', string="First Unit",store=False)    # 法定单位

    second_unit = fields.Many2one(comodel_name="cus_args.unit", related='goods_code.second_unit_id', string="Second Unit", store=False)    # 第二单位

    rate_first_unit = fields.Char(string="First Unit rate") # 法定单位转换率

    rate_second_unit = fields.Char(string="Second Unit rate")   # 第二单位转换率

    electric_type = fields.Char(string=" Electric type", required=False)    # 3C类别

    electric_term = fields.Char(string=" Electric term", required=False)    # 3C条件

    duty_paragraph_change_views = fields.Char(string="Duty paragraph change view", required=False)  # 税号变更记录

    part_remarks = fields.Text(string="Part remarks")   # 备注

    state = fields.Selection(selection=[('draft', 'Draft'),  # 草稿
                                        ('submitted', 'Submitted'),  # 提交 待审核
                                        ('refused', 'Refused'),  # 审核不通过
                                        ('approve', 'approved')  # 通过审核
                                        ], string='states', readonly=True, default='draft')

    @api.onchange('goods_code')
    def _generate_about_name(self):
        for goods_list in self:
            if goods_list.goods_code:
                goods_list.chinese_name = goods_list.goods_code.name_cn
                # goods_list.first_unit = goods_list.goods_code.first_unit
                # goods_list.second_unit = goods_list.goods_code.second_unit

    @api.multi
    def submit_review_btn(self):
        """ 商品归类信息提交审核 按钮"""
        self.update({'state': 'submitted'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类审核已提交, 请耐心等待管理员审核 ！<br/>") % (goods_cls_list.goods_code.code_ts))
            goods_cls_list.message_post(body=body)

    @api.multi
    def re_submit_review_btn(self):
        """ 商品归类信息 重新提交审核 按钮"""
        self.update({'state': 'submitted'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类审核已重新提交, 请耐心等待管理员审核 ！<br/>") % (goods_cls_list.goods_code.code_ts))
            goods_cls_list.message_post(body=body)

    @api.multi
    def already_reviewed_btn(self):
        """ 商品归类信息 审核通过 按钮"""
        self.update({'state': 'approve'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类，已审核通过！<br/>") % (goods_cls_list.goods_code.code_ts))
            goods_cls_list.message_post(body=body)

    @api.multi
    def refused_reviewed_btn(self):
        """ 商品归类信息 审核拒绝 按钮"""
        self.update({'state': 'refused'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类，未审核通过！<br/>") % (goods_cls_list.goods_code.code_ts))
            goods_cls_list.message_post(body=body)