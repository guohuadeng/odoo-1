# -*- coding: utf-8 -*-
from odoo import models, fields, api



class InternationPort(models.Model):
    """国际标准港口"""
    _name = 'basedata.internation_port'
    _rec_name = 'name_cn'
    _description = 'International Port'

    name_cn = fields.Char('Chinese Name', size=50)
    name_en = fields.Char('English Name', size=50)
    code = fields.Char(string="Code")
    port_type = fields.Selection(string="Port Type", selection=[('airport', 'Airport'),
                                                                ('seaport', 'Seaport')])
    transport_mode = fields.Char(string="Transport Mode", compute='_get_transport_mode')
    city_name_cn = fields.Char(string="City Chinese Name")
    city_name_en = fields.Char(string="City English Name")
    city_code = fields.Char(string="City Code")

    @api.multi
    @api.depends('name_cn', 'name_en', 'code')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s %s"%(record.code, record.name_cn, record.name_en))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', '|', ('code', operator, name), ('name_cn', operator, name), ('name_en', operator, name)]

        return super(InternationPort, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )

    @api.depends('port_type')
    def _get_transport_mode(self):
        """得到运输方式"""
        for obj in self:
            if obj.port_type == 'airport':
                obj.transport_mode = self.env.ref('basedata.delegate_transport_mode_5').code
            elif obj.port_type == 'seaport':
                obj.transport_mode = self.env.ref('basedata.delegate_transport_mode_2').code