# -*- coding: utf-8 -*-

from odoo import models, fields


class DecResultStatus(models.Model):
    """报关单回执状态"""
    _name = 'cus_center.dec_res_status'
    _rec_name = 'name'
    _description = 'Result Status'

    code = fields.Char(string="Code", required=False, )
    name = fields.Char(string="Name", required=False, translate=True)
    sequence = fields.Integer(string="Sequence", required=False, )

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         'The status\'s code must be unique')
    ]
