# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TransportMode(models.Model):
    """运输方式"""
    _name = 'delegate_transport_mode'
    _description = 'Mode of transport'
    _table = 'b_hg_traf_mode'
    _rec_name = 'name_cn'

    code = fields.Char(string='Transport Mode Code', size=50)       # 运输方式代码
    name_cn = fields.Char(string='Transport Mode Chinese Name', size=50)     # 中文名称

    @api.multi
    @api.depends('code', 'name_cn')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s"%(record.code, record.name_cn))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('code', operator, name), ('name_cn', operator, name)]

        return super(TransportMode, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


# class Exemption(models.Model):
#     """征免性质"""
#     _name = 'delegate_exemption'
#     _description = 'exemption nature of delegation'
#     _table = 'b_hg_cut_mode'
#     _rec_name = 'NameCN'
#
#     Code = fields.Char('Exemption Code', size=50)       # 征免方式代码
#     NameCN = fields.Char('Chinese Name', size=50)       # 中文名称


class TradeTerms(models.Model):
    """成交方式"""
    _name = 'delegate_trade_terms'
    _description = 'trade terms of delegation'
    _table = 'b_hg_trans_mode'
    _rec_name = 'NameCN'

    Code = fields.Char('Trade Terms Code', size=50)   # 成交方式代码
    NameCN = fields.Char('Trade Terms Chinese Name', size=50)   # 中文名称

    @api.multi
    @api.depends('Code', 'NameCN')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s"%(record.Code, record.NameCN))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('Code', operator, name), ('NameCN', operator, name)]

        return super(TradeTerms, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class Port(models.Model):
    """装运港"""
    _name = 'delegate_port'
    _description = 'ports of delegation'
    _table = 'b_hg_port'
    _rec_name = 'NameCN'

    Code = fields.Char('Port Code', size=50)     # 装运港代码
    NameCN = fields.Char('Port Chinese Name', size=50)   # 中文名称

    @api.multi
    @api.depends('Code', 'NameCN')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s"%(record.Code, record.NameCN))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('Code', operator, name), ('NameCN', operator, name)]

        return super(Port, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class Customs(models.Model):
    """关区代码(即进出口岸)"""
    _name = 'delegate_customs'
    _description = 'customs of delegation'
    _table = 'b_hg_customs'
    _rec_name = 'NameCN'

    Code = fields.Char('Custom Code', size=50)     # 进出口岸代码
    NameCN = fields.Char('Custom Chinese Name', size=50)   # 中文名称

    @api.multi
    @api.depends('Code', 'NameCN')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s"%(record.Code, record.NameCN))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('Code', operator, name), ('NameCN', operator, name)]

        return super(Customs, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class TradeMode(models.Model):
    """监管方式"""
    _name = 'delegate_trade_mode'
    _description = 'trade mode of delegation'
    _table = 'b_hg_trade_mode'
    _rec_name = 'NameCN'

    Code = fields.Char('Trade Mode Code', size=50)     # 监管方式代码
    NameCN = fields.Char('Trade Mode Chinese Name', size=50)   # 中文名称

    @api.multi
    @api.depends('Code', 'NameCN')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s"%(record.Code, record.NameCN))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('Code', operator, name), ('NameCN', operator, name)]

        return super(TradeMode, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class Region(models.Model):
    """境内目的地"""
    _name = 'delegate_region'
    _description = 'region of delegation'
    _table = 'b_hg_district_code'
    _rec_name = 'NameCN'

    Code = fields.Char('Region Code', size=50)     # 境内目的地代码
    NameCN = fields.Char('Region Chinese Name', size=50)   # 中文名称

    @api.multi
    @api.depends('Code', 'NameCN')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s"%(record.Code, record.NameCN))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('Code', operator, name), ('NameCN', operator, name)]

        return super(Region, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class Packing(models.Model):
    """包装方式"""
    _name = 'delegate_packing'
    _description = 'packing of delegation'
    _table = 'b_hg_wrap_type'
    _rec_name = 'NameCN'

    Code = fields.Char("Pack Code", size=50)     # 包装种类代码
    NameCN = fields.Char("Pack Chinese Name", size=50)   # 中文名称

    @api.multi
    @api.depends('Code', 'NameCN')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s"%(record.Code, record.NameCN))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('Code', operator, name), ('NameCN', operator, name)]

        return super(Packing, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )

class Country(models.Model):
    """国别地区代码"""
    _name = 'delegate_country'
    _description = 'add the Country of originOrCountry of destination'
    _rec_name = 'NameCN'
    _table = 'b_hg_country'

    Code = fields.Char('Country Code', size=50)     # 国家代码
    NameCN = fields.Char('Country Chinese Name', size=50)   # 中文名称

    @api.multi
    @api.depends('Code', 'NameCN')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s"%(record.Code, record.NameCN))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('Code', operator, name), ('NameCN', operator, name)]

        return super(Country, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )