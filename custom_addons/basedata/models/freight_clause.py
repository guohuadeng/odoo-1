# -*- coding: utf-8 -*-
from odoo import models, fields


class FreightClause(models.Model):
    """运费条款"""
    _name = 'freight_clause'
    _description = 'Freight Clause'
    _table = 'freight_clause'
    _rec_name = 'cn_name'

    cn_name = fields.Char(string="CNName", required=False, )    # 中文名称
    en_name = fields.Char(string="ENName", required=False, )    # 英文名陈
    description = fields.Text(string="description", required=False, )  # 说明