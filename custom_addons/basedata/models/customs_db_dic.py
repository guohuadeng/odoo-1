# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CusCutMode(models.Model):
    """ 征免性质表 """
    _name = 'basedata.cus_cut_mode'
    _description = 'customs cut mode'
    _rec_name = 'NameCN'

    Code = fields.Char(string='Cut Mode Code', required=True)     # 征免性质代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)   # 中文名称


class CusDutyMode(models.Model):
    """ 征免方式表 """
    _name = 'basedata.cus_duty_mode'
    _description = 'Customs Duty Mode'
    _rec_name = 'NameCN'

    Code = fields.Char(string='DutyMode Code', required=True)  # 征免方式代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)  # 中文名称


class CusUnit(models.Model):
    """ 单位表 """
    _name = 'basedata.cus_unit'
    _description = 'customs unit'
    _rec_name = 'NameCN'

    Code = fields.Char(string='unit Code', required=True)     # 计量单位代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)   # 中文名称


class CusCurrency(models.Model):
    """ 币制 """
    _name = 'basedata.cus_currency'
    _description = 'Customs Currency'
    _rec_name = 'NameCN'

    Code = fields.Char(string='Currency Code', required=True)       # 币制代码
    symbol = fields.Char(string='Symbol',)     # 符号
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)   # 中文名称


class CusEntryType(models.Model):
    """ 报关单类型表  """
    _name = 'basedata.cus_entry_type'
    _description = 'Customs EntryType'
    _rec_name = 'NameCN'

    Code = fields.Char(string='EntryType Code', required=True)       # 报关单类型代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)   # 中文名称


class CusFilingBillType(models.Model):
    """ 备案清单类型表 """
    _name = 'basedata.cus_filing_bill_type'
    _description = 'Customs Filing Bill Type'
    _rec_name = 'NameCN'

    Code = fields.Char(string='Filing Bill Type Code', required=True)       # 备案清单类型代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)     # 中文名称


class CusRegisterCompany(models.Model):
    """ 企业库表 """
    _name = 'basedata.cus_register_company'
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


class CusGoodsTariff(models.Model):
    """ 海关税则 """
    _name = 'basedata.cus_goods_tariff'
    _description = 'Customs goods tariff'
    _rec_name = 'Code_ts'

    Code_t = fields.Char(string='tax regulations Code', required=True)       # 税则号
    Code_s = fields.Char(string='Attach Code',)       # 附加编号
    Code_ts = fields.Char(string='goods Code',)       # 商品编号
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)     # 中文名称
    first_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="First Unit", )  # 第一计量单位
    second_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="second Unit", )  # 第二计量单位

class DecLicenseDocType(models.Model):
    """ 随附单证类型 """
    _name = 'basedata.dec_license_doc_type'
    _description = 'Customs DecLicenseDoc Type'
    _rec_name = 'NameCN'

    Code = fields.Char(string='Filing Bill Type Code', required=True)       # 随附单证类型代码
    NameCN = fields.Char(string='Chinese Name', size=50, required=True)     # 中文名称
