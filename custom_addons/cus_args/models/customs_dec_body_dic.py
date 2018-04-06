# -*- coding: utf-8 -*-
from odoo import models, fields, api

# 报关表体基础参数表

class DutyMode(models.Model):
    """ 征免方式表 """
    _name = 'cus_args.duty_mode'
    _description = 'Duty Mode Code Table'
    _rec_name = 'name_cn'

    code = fields.Char(string='DutyMode Code', required=True)  # 征免方式代码
    name_cn = fields.Char(string='DutyMode Chinese Name', size=50, required=True)  # 中文名称

    @api.multi
    @api.depends('code', 'name_cn')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s" % (record.code, record.name_cn))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('code', operator, name), ('name_cn', operator, name)]

        return super(DutyMode, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class Unit(models.Model):
    """ 单位表 """
    _name = 'cus_args.unit'
    _description = 'Unit Code Table'
    _rec_name = 'name_cn'

    code = fields.Char(string='Unit Code', required=True)  # 计量单位
    name_cn = fields.Char(string='Unit Chinese Name', size=50, required=True)  # 中文名称

    @api.multi
    @api.depends('code', 'name_cn')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s" % (record.code, record.name_cn))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('code', operator, name), ('name_cn', operator, name)]

        return super(Unit, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )
