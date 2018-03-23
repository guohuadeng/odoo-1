# -*- coding: utf-8 -*-
from odoo import models, fields, api


# class HSCode(models.Model):
#     """报关商品编码数据"""
#     _name = 'product_hs_code'
#     _description = 'add the Country of originOrCountry of destination'
#     _rec_name = 'Code_TS'
#     _table = 'b_hg_complex'
#
#     Code_TS = fields.Char('HS Code', size=50)  # 海关编码
#     G_Name = fields.Char('Chinese Name', size=100)    # 中文品名
#     # LegalUN = fields.Char('法定单位', size=50)
#     # SecondUN = fields.Integer('第二单位')
#     # Control_Ma = fields.Char('Regulatory Tag', size=255)  # 监管标识


class DeclareElement(models.Model):
    """报关商品申报要素"""
    _name = 'declare_element'
    _description = 'declare element'
    _rec_name = 'name'
    _table = 'b_hg_complex_criterion'

    cus_goods_tariff_id = fields.Many2one(comodel_name="basedata.cus_goods_tariff", string="HS Code", required=True, )
    name = fields.Char('Element Name', size=255, required=True)   # 要素名
    sequence = fields.Integer('Num', required=True)   # 序号





# class Unit(models.Model):
#     """商品单位"""
#     _name = 'turnover_unit'
#     _description = 'add special unit for delegation'
#     _rec_name = 'NameCN'
#     _table = 'b_hg_unit'
#
#     NameCN = fields.Char('Chinese Name', size=50)   # 中文名称
#     Code = fields.Char('Unit Code', size=50)        # 单位代码


# class CurrencySystem(models.Model):
#     """币种"""
#     _name = 'currency_system'
#     _description = 'add special currency system for delegation'
#     _rec_name = 'NameCN'
#     _table = 'b_hg_currency'
#
#     NameCN = fields.Char('Chinese Name', size=50)   # 中文名称
#     Code = fields.Char('Currency Code', size=50)     # 币种代码


class GoodsAttribute(models.Model):
    """货物属性"""
    _name = 'goods_attribute'
    _description = 'add special goods attribute for delegation'
    _rec_name = 'attribute_name'
    _table = 'b_hg_goods_attribute'

    attribute_name = fields.Char('Attribute Name', size=20)  # 属性名称
    description = fields.Text(string="description")