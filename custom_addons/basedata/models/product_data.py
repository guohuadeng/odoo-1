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

    cus_goods_tariff_id = fields.Many2one(comodel_name="basedata.cus_goods_tariff", string="Customs Goods Tariff", required=True, )
    name = fields.Char('Element Name', size=255, required=True)   # 要素名
    sequence = fields.Integer('Num', required=True)   # 序号


class Country(models.Model):
    """国家、地区"""
    _name = 'delegate_country'
    _description = 'add the Country of originOrCountry of destination'
    _rec_name = 'NameCN'
    _table = 'b_hg_country'

    Code = fields.Char('Country Code', size=50)     # 国家代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称

    @api.multi
    @api.depends('Code', 'NameCN')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s"%(record.Code, record.NameCN))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('Code', operator, name), ('NameCN', operator, name)]

        return super(Country, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


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