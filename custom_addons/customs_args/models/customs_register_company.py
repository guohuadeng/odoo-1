# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CusRegisterCompany(models.Model):
    """ 企业库表 """
    _name = 'cus_args.register_company'
    _description = 'Customs register company'
    _rec_name = 'register_name_cn'

    register_code = fields.Char(string='Customs register Code', required=True)       # 海关编码
    unified_social_credit_code = fields.Char(string='Customs unified social credit code', required=True)  # 社会信用统一编码
    register_name_cn = fields.Char(string='Customs Register Name', size=50, required=True)     # 企业海关名称

    @api.multi
    @api.depends('register_code', 'register_name_cn')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s" % (record.register_code, record.register_name_cn))
                #(record.id, u"%s:%s" % ('name', record.register_name_cn))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('register_code', operator, name), ('register_name_cn', operator, name)]

        return super(CusRegisterCompany, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )

