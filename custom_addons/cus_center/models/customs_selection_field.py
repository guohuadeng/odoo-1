# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CusPaymentMarkType(models.Model):
    """ 纳税单位标识类型 """
    _name = 'cus_center.pay_mark_type'
    _description = 'customs Payment MarkType'
    _rec_name = 'NameCN'

    Code = fields.Char(string='PaymentMarkType Code', required=True)     # 代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)  # 中文名称


class CusExpensesMarkType(models.Model):
    """ 费用标识类型 """
    _name = 'cus_center.exp_mark_type'
    _description = 'customs CusExpensesMarkType'
    _rec_name = 'NameCN'

    Code = fields.Char(string='CusExpensesMarkType Code', required=True)  # 代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)   # 中文名称


class CusWhetherMarkType(models.Model):
    """ 是否标识类型 """
    _name = 'cus_center.whet_mark_type'
    _description = 'customs ExpensesMarkType'
    _rec_name = 'NameCN'

    Code = fields.Char(string='WhetherMarkType Code', required=True)     # 代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)  # 中文名称