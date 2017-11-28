# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError


class Incoterm(models.Model):
    """添加成交方式"""
    _inherit = 'stock.incoterms'

    trade_term_id = fields.Many2one(comodel_name="delegate_trade_terms", string="Trade Term")

