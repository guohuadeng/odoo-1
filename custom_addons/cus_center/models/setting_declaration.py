# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class CompanySettings(models.TransientModel):
    """ 企业报关单 相关设置"""
    _inherit = 'res.config.settings'
    _name = 'cus_center.settings'

    default_cop_code = fields.Char(default_model='customs_center.customs_dec')  # 录入单位企业组织机构代码
    default_cop_name = fields.Char(default_model='customs_center.customs_dec')  # 录入单位名称

    default_cop_code_scc = fields.Char(default_model='customs_center.customs_dec')  # 录入单位社会信用统一编码
    default_inputer_name = fields.Char(default_model='customs_center.customs_dec')  # 录入员姓名
    default_oper_name = fields.Char(default_model='customs_center.customs_dec')     # 操作员姓名
    default_certificate = fields.Char(default_model='customs_center.customs_dec')   # 操作员卡的证书号
    default_ic_code = fields.Char(default_model='customs_center.customs_dec')  # 操作员IC卡号

    default_dec_company_customs_code = fields.Char(default_model='customs_center.customs_dec')  # 申报单位海关编号

    @api.onchange('default_dec_company')
    def _get_customs_dec_company(self):
        """ 由于设置界面同时需要给通关清单模型相应的字段赋值 获取当前申报单位 赋值给通关清单模型"""
        for sheet in self:
            if sheet.default_dec_company:
                print('6666666666666666666666666666666666')




