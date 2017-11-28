# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class GoodSize(models.Model):
    _name = 'service_center.goods_size'

    length = fields.Integer(string="Length",  required=True, )
    width = fields.Integer(string="Width",  required=True, )
    height = fields.Integer(string="Height",  required=True, )
    qty = fields.Integer(string="Qty", required=True, default=1)
    work_sheet_id = fields.Many2one(comodel_name="work_sheet", string="Work Sheet")