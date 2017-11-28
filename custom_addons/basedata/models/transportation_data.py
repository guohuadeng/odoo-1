# -*- coding: utf-8 -*-
from odoo import models, fields


class Route(models.Model):
    """航线"""
    _name = 'route'
    _description = 'air line route'
    _table = 'route'
    _rec_name = "NameCN"

    code = fields.Char(string="航班编码")
    NameCN = fields.Char('Chinese Name', size=30)  # 中文名称
    NameEN = fields.Char('English Name', size=30)  # 英文名称
    description = fields.Text(string="description")


class TransportationTerm(models.Model):
    """运输条款"""
    _name = 'transportation_term'
    _description = 'Transportation Term'
    _table = 'transportation_term'
    _rec_name = 'en_name'

    cn_name = fields.Char(string="CNName", required=False, )  # 中文名称
    en_name = fields.Char(string="ENName", required=False, )  # 英文名陈
    description = fields.Text(string="description", required=False, )   # 说明
