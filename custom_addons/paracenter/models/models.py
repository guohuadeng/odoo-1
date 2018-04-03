# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..utils.redis_conn import conn

class District(models.Model):
    _name = 'paracenter.district'
    _rec_name = 'name'
    _description = 'District'

    code = fields.Char(string="Code", required=True, index=True)
    name = fields.Char(string="Name", compute='_get_name')
    version = fields.Char(string="Version", compute='_get_version')


    @api.multi
    def _get_name(self):
        """从Redis中获得名称"""
        for obj in self:
            obj.name = conn.hget('district:' + obj.code, 'name')

    @api.multi
    def _get_version(self):
        """从redis中获得版本"""
        for obj in self:
            obj.version = conn.hget('district:' + obj.code, 'version')