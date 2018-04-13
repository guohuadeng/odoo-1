# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SyncTask(models.Model):
    _name = 'customs.sync_task'
    _rec_name = 'sync_model'
    _description = 'Data Sync Task'

    scheme = fields.Selection(string="Scheme", selection=[('http', 'Http'), ('https', 'Https'), ], required=True, )
    base_url = fields.Char(string="Source URL", required=True, )
    data_uri = fields.Char(string="URI", required=True, )
    sync_model = fields.Char(string="Model", required=True, )
    port = fields.Char(string="Port", required=True, )


    @api.multi
    def sync_data(self):
        """同步数据"""
        print(u"开始同步数据!")
        codes = self.env[self.sync_model].search().map(lambda r: r.code)
