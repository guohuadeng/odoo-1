# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CusGoodsTariff(models.Model):
    """ 海关商品税则 """
    _name = 'cus_args.goods_tariff'
    _description = 'Goods Tariff Table'
    _rec_name = 'code_ts'

    code_t = fields.Char(string='Tax Regulations Code', )  # 税号
    code_s = fields.Char(string='Attach Code', )  # 附加编码
    code_ts = fields.Char(string='HS Code', required=True)  # 商品编号
    name_cn = fields.Char(string='Goods Chinese Name', size=50, required=True)  # 中文名称
    first_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="First Unit", )  # 第一计量单位
    second_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="Second Unit", )  # 第二计量单位
    supervision_condition = fields.Char(string="Supervision Condition")  # 监管条件 / 监管标识


class DeclareElement(models.Model):
    """商品申报要素"""
    _name = 'cus_args.goods_declare_element'
    _description = 'Goods Declare Element'
    _rec_name = 'name_cn'

    goods_tariff_id = fields.Many2one(comodel_name="cus_args.goods_tariff", string="HS Code", required=True, )
    name_cn = fields.Char('Element Name', size=50, required=True)  # 要素名
    sequence = fields.Integer('Num', required=True)  # 序号
