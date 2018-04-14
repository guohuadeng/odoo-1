# -*- coding: utf-8 -*-

from odoo import models, fields


class EdocQueue(models.Model):
    _name = 'cus_center.edoc_queue'
    _rec_name = 'edoc_id'
    _description = 'Edoc Queue'

    edoc_id = fields.Char(string="EdocID", required=True)
    edoc_code = fields.Char(string="EdocCode", required=True)
    cus_dec_id = fields.Integer(string="Customs DEC ID", required=True, )

