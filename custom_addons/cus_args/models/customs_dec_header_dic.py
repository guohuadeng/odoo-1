# -*- coding: utf-8 -*-
from odoo import models, fields, api


# 报关表头基础参数表
class Customs(models.Model):
    """关区代码(即进出口岸)"""
    _name = 'cus_args.customs'
    _description = 'Customs Code Table'
    _rec_name = 'name_cn'

    code = fields.Char('Custom Code', size=50)  # 进出口岸代码
    name_cn = fields.Char('Custom Chinese Name', size=50)  # 中文名称

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

        return super(Customs, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class TransportMode(models.Model):
    """运输方式"""
    _name = 'cus_args.transport_mode'
    _description = 'Transport Mode Table'
    _rec_name = 'name_cn'

    code = fields.Char(string='Transport Mode Code', size=50)  # 运输方式代码
    name_cn = fields.Char(string='Transport Mode Chinese Name', size=50)  # 中文名称

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

        return super(TransportMode, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class TradeMode(models.Model):
    """监管方式"""
    _name = 'cus_args.trade_mode'
    _description = 'Trade Mode Code Table'
    _rec_name = 'name_cn'

    code = fields.Char('Trade Mode Code', size=50)  # 监管方式代码
    name_cn = fields.Char('Trade Mode Chinese Name', size=50)  # 中文名称

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

        return super(TradeMode, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class CusCutMode(models.Model):
    """ 征免性质表 """
    _name = 'cus_args.cut_mode'
    _description = 'Cut Mode Code Table'
    _rec_name = 'name_cn'

    code = fields.Char(string='Cut Mode Code', required=True)  # 征免性质代码
    name_cn = fields.Char(string='Cut Chinese Name', size=50, required=True)  # 中文名称

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

        return super(CusCutMode, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class Country(models.Model):
    """国别地区代码（用于报关单中的启运/抵达国、贸易国别）"""
    _name = 'cus_args.country'
    _description = 'Country Code Table'
    _rec_name = 'name_cn'

    code = fields.Char('Country Code', size=50)  # 国家代码
    name_cn = fields.Char('Country Chinese Name', size=50)  # 中文名称

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

        return super(Country, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class InternalDistrict(models.Model):
    """国内地区代码（用于报关单境内目的/货源地）"""
    _name = 'cus_args.internal_district'
    _description = 'Internal District Code Table'
    _rec_name = 'name_cn'

    code = fields.Char('Internal District Code', size=50)  # 国内地区代码
    name_cn = fields.Char('Internal District Chinese Name', size=50)  # 中文名称

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

        return super(InternalDistrict, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class Port(models.Model):
    """港口代码（用于报关单装货/指运港）"""
    _name = 'cus_args.port'
    _description = 'Port Code Table'
    _rec_name = 'name_cn'

    code = fields.Char('Port Code', size=50)  # 装运港代码
    name_cn = fields.Char('Port Chinese Name', size=50)  # 中文名称

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

        return super(Port, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class TradeTerms(models.Model):
    """成交方式"""
    _name = 'cus_args.trade_terms'
    _description = 'Trade Terms Code Table'
    _rec_name = 'name_cn'

    code = fields.Char('Trade Terms Code', size=50)  # 成交方式代码
    name_cn = fields.Char('Trade Terms Chinese Name', size=50)  # 中文名称

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

        return super(TradeTerms, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class WrapType(models.Model):
    """包装种类"""
    _name = 'cus_args.wrap_type'
    _description = 'Wrap Type Code Table'
    _rec_name = 'name_cn'

    code = fields.Char("Wrap Type Code", size=50)  # 包装种类代码
    name_cn = fields.Char("Wrap Type Chinese Name", size=50)  # 中文名称

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

        return super(WrapType, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class Currency(models.Model):
    """ 货币代码表"""
    _name = 'cus_args.currency'
    _description = 'Currency Code Table'
    _rec_name = 'name_cn'

    code = fields.Char(string='Currency Code', required=True)  #货币代码
    symbol = fields.Char(string='Currency Symbol', )  # 符号
    name_cn = fields.Char(string='Currency Chinese Name', size=50, required=True)  # 中文名称

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

        return super(Currency, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )

class CusEntryType(models.Model):
    """ 报关单类型表  """
    _name = 'cus_args.entry_type'
    _description = 'Customs Entry Type Table'
    _rec_name = 'name_cn'

    code = fields.Char(string='Entry Type Code', required=True)  # 报关单类型代码
    name_cn = fields.Char(string='Entry Type Chinese Name', size=50, required=True)  # 中文名称


class CusFilingBillType(models.Model):
    """ 备案清单类型表 """
    _name = 'cus_args.filing_bill_type'
    _description = 'Filing Bill Type Table'
    _rec_name = 'name_cn'

    code = fields.Char(string='Filing Bill Type Code', required=True)  # 备案清单类型代码
    name_cn = fields.Char(string='Filing Bill Type Chinese Name', size=50, required=True)  # 中文名称


class DecLicenseDocType(models.Model):
    """ 随附单证类型 """
    _name = 'cus_args.dec_license_doc_type'
    _description = 'DecLicenseDoc Type Table'
    _rec_name = 'name_cn'

    code = fields.Char(string='Filing Bill Type Code', required=True)  # 随附单证类型代码
    name_cn = fields.Char(string='Filing Bill Type Chinese Name', size=50, required=True)  # 中文名称
