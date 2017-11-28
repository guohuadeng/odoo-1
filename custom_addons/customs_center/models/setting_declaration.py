# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class SettingDeclaration(models.Model):
    """ 企业报关单 相关设置"""
    _name = 'customs_center.dec_settings'
    _rec_name = 'et_dec_catalog_name'
    _description = 'Setting Declaration catalog'

    et_dec_catalog_name = fields.Char(string="enterprise path", required=True, )
    # customs_declaration_id = fields.One2many(comodel_name="customs_center.customs_dec", inverse_name="et_dec_catalog_ids",
    #                                     string="Customs Declaration")


class YourSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'customs_center.settings'

    default_cop_code = fields.Char(default_model='customs_center.customs_dec')      # 录入单位代码 企业组织机构代码
    default_cop_name = fields.Char(default_model='customs_center.customs_dec')      # 录入单位名称
    default_inputer_name = fields.Char(default_model='customs_center.customs_dec')  # 录入员姓名
    default_oper_name = fields.Char(default_model='customs_center.customs_dec')     # 操作员姓名
    default_certificate = fields.Char(default_model='customs_center.customs_dec')   # 操作员卡的证书号
    default_cop_code_scc = fields.Char(default_model='customs_center.customs_dec')  # 录入单位社会信用统一编码
    default_owner_code_scc = fields.Char(default_model='customs_center.customs_dec')  # 货主单位/生产消费单位 社会信用统一编码
    default_trade_code_scc = fields.Char(default_model='customs_center.customs_dec')  # 经营单位 / 收发货人 统一编码
    default_ic_code = fields.Char(default_model='customs_center.customs_dec')  # 操作员IC卡号

    # company_name = fields.Char()
    # company_phone = fields.Char()
    #
    # @api.model
    # def get_default_company_values(self, fields):
    #     """
    #     Method argument "fields" is a list of names
    #     of all available fields.
    #     """
    #     company = self.env.user.company_id
    #     return {
    #         'company_name': company.name,
    #         'company_phone': company.phone,
    #     }
    #
    # @api.one
    # def set_company_values(self):
    #     company = self.env.user.company_id
    #     company.name = self.company_name
    #     company.phone = self.company_phone
