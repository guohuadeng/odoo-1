# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TransportMode(models.Model):
    """运输方式"""
    _name = 'cus_args.transport_mode'
    _description = 'customs transport mode'
    _table = 'b_hg_traf_mode'
    _rec_name = 'name_cn'

    code = fields.Char(string='Transport Mode Code', size=50)       # 运输方式代码
    name_cn = fields.Char(string='Chinese Name', size=50)     # 中文名称


class TradeTerms(models.Model):
    """成交方式"""
    _name = 'cus_args.trade_terms'
    _description = 'customs trade terms'
    _table = 'b_hg_trans_mode'
    _rec_name = 'NameCN'

    Code = fields.Char('Trade Terms Code', size=50)   # 成交方式代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称

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
    _name = 'cus_args.port'
    _description = 'customs ports'
    _table = 'b_hg_port'
    _rec_name = 'NameCN'

    Code = fields.Char('Port Code', size=50)     # 装运港代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称

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
    """进出口岸"""
    _name = 'cus_args.customs'
    _description = 'customs of delegation'
    _table = 'b_hg_customs'
    _rec_name = 'NameCN'

    Code = fields.Char('Custom Code', size=50)     # 进出口岸代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称

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
    _name = 'cus_args.trade_mode'
    _description = 'trade mode of delegation'
    _table = 'b_hg_trade_mode'
    _rec_name = 'NameCN'

    Code = fields.Char('Trade Mode Code', size=50)     # 监管方式代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称

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
    _name = 'cus_args.region'
    _description = 'region of delegation'
    _table = 'b_hg_district_code'
    _rec_name = 'NameCN'

    Code = fields.Char('Region Code', size=50)     # 境内目的地代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称

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
    _name = 'cus_args.packing'
    _description = 'customs packing'
    _table = 'b_hg_wrap_type'
    _rec_name = 'NameCN'

    Code = fields.Char("Pack Code", size=50)     # 包装种类代码
    NameCN = fields.Char("Chinese Name", size=50)   # 中文名称

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
    """国家、地区"""
    _name = 'cus_args.country'
    _description = 'customs country'
    _rec_name = 'NameCN'
    _table = 'b_hg_country'

    Code = fields.Char('Country Code', size=50)     # 国家代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称

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


class CusCutMode(models.Model):
    """ 征免性质表 """
    _name = 'cus_args.cut_mode'
    _description = 'customs cut mode'
    _rec_name = 'NameCN'

    Code = fields.Char(string='Cut Mode Code', required=True)     # 征免性质代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)   # 中文名称


class CusDutyMode(models.Model):
    """ 征免方式表 """
    _name = 'cus_args.duty_mode'
    _description = 'Customs Duty Mode'
    _rec_name = 'NameCN'

    Code = fields.Char(string='DutyMode Code', required=True)  # 征免方式代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)  # 中文名称

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

        return super(CusDutyMode, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class CusUnit(models.Model):
    """ 单位表 """
    _name = 'cus_args.cus_unit'
    _description = 'customs unit'
    _rec_name = 'NameCN'

    Code = fields.Char(string='unit Code', required=True)     # 计量单位
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)   # 中文名称

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

        return super(CusUnit, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class CusCurrency(models.Model):
    """ 币制 """
    _name = 'cus_args.cus_currency'
    _description = 'Customs Currency'
    _rec_name = 'NameCN'

    Code = fields.Char(string='Currency Code', required=True)       # 币制代码
    symbol = fields.Char(string='Symbol',)     # 符号
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)   # 中文名称

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

        return super(CusCurrency, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


class CusEntryType(models.Model):
    """ 报关单类型表  """
    _name = 'cus_args.entry_type'
    _description = 'Customs EntryType'
    _rec_name = 'NameCN'

    Code = fields.Char(string='EntryType Code', required=True)       # 报关单类型代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)   # 中文名称


class CusFilingBillType(models.Model):
    """ 备案清单类型表 """
    _name = 'cus_args.filing_bill_type'
    _description = 'Customs Filing Bill Type'
    _rec_name = 'NameCN'

    Code = fields.Char(string='Filing Bill Type Code', required=True)       # 备案清单类型代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)     # 中文名称


class CusGoodsTariff(models.Model):
    """ 海关税则 """
    _name = 'cus_args.goods_tariff'
    _description = 'Customs goods tariff'
    _rec_name = 'Code_ts'

    Code_t = fields.Char(string='tax regulations Code',)       # 税则号
    Code_s = fields.Char(string='Attach Code',)       # 附加编号
    Code_ts = fields.Char(string='goods Code', required=True)       # 商品编号
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)     # 中文名称
    first_unit = fields.Many2one(comodel_name="cus_args.cus_unit", string="First Unit", )  # 第一计量单位
    second_unit = fields.Many2one(comodel_name="cus_args.cus_unit", string="second Unit", )  # 第二计量单位
    supervision_condition = fields.Char(string="supervision condition")  # 监管条件 / 监管标识

class DecLicenseDocType(models.Model):
    """ 随附单证类型 """
    _name = 'cus_args.dec_license_doc_type'
    _description = 'Customs DecLicenseDoc Type'
    _rec_name = 'NameCN'

    Code = fields.Char(string='Filing Bill Type Code', required=True)       # 随附单证类型代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)     # 中文名称


class DeclareElement(models.Model):
    """报关商品申报要素"""
    _name = 'cus_args.declare_element'
    _description = 'declare element'
    _rec_name = 'name'
    _table = 'b_hg_complex_criterion'

    cus_goods_tariff_id = fields.Many2one(comodel_name="cus_args.goods_tariff", string="Customs Goods Tariff", required=True, )
    name = fields.Char('Element Name', size=255, required=True)   # 要素名
    sequence = fields.Integer('Num', required=True)   # 序号
