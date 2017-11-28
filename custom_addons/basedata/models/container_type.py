# -*- coding: utf-8 -*-
from odoo import models, fields


class ContainerType(models.Model):
    """箱型"""
    _name = 'container_type'
    _description = 'box container type'
    _table = 'container_type'
    _rec_name = "name"

    name = fields.Char(string="Name")
    active = fields.Boolean(string="enable/diable")
    description = fields.Text(string="description")