# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class CompanySettings(models.TransientModel):
    """ 企业报关单 相关设置"""
    _inherit = 'res.config.settings'
    _name = 'cus_center.settings'

    default_cop_code = fields.Char(default_model='cus_center.customs_dec')  # 录入单位企业组织机构代码
    default_cop_name = fields.Char(default_model='cus_center.customs_dec')  # 录入单位名称
    # default_dec_company = fields.Many2one(comodel_name="basedata.cus_register_company" , default_model='customs_center.customs_dec')  # 报关单 申报单位名称
    # default_dec_company_order = fields.Many2one(comodel_name="basedata.cus_register_company", default_model='customs_center.customs_order')  # 通关清单 申报单位名称

    # default_dec_company = fields.Char(default_model='customs_center.customs_dec')  # 申报单位名称
    # default_dec_company_order = fields.Char(default_model='customs_center.customs_dec')  # 通关清单 申报单位名称

    default_cop_code_scc = fields.Char(default_model='cus_center.customs_dec')  # 录入单位社会信用统一编码
    default_inputer_name = fields.Char(default_model='cus_center.customs_dec')  # 录入员姓名
    default_oper_name = fields.Char(default_model='cus_center.customs_dec')     # 操作员姓名
    default_certificate = fields.Char(default_model='cus_center.customs_dec')   # 操作员卡的证书号
    default_ic_code = fields.Char(default_model='cus_center.customs_dec')  # 操作员IC卡号
    # default_cus_dec_dir = fields.Char(default_model='customs_center.customs_dec')  # 报文存放目录

    default_dec_company_customs_code = fields.Char(default_model='cus_center.customs_dec')  # 申报单位海关编号

    @api.onchange('default_dec_company')
    def _get_customs_dec_company(self):
        """ 由于设置界面同时需要给通关清单模型相应的字段赋值 获取当前申报单位 赋值给通关清单模型"""
        for sheet in self:
            if sheet.default_dec_company:
                print('6666666666666666666666666666666666')
                # print(sheet.default_dec_company)
                # sheet.default_dec_company_order = sheet.default_dec_company
                #sheet.default_dec_company_customs_code = sheet.default_dec_company.register_code



                #
                # # 测试
                # print(self.env.user.company_id.name)
                # print(self.env['basedata.cus_register_company'].search(
                #     [('register_name_cn', 'like', self.env.user.company_id.name[:4]+'%')])[0].id)
                # print(self.env['basedata.cus_register_company'].search(
                #     [('register_name_cn', 'like', '博越锦程' + '%')])[0])
                # print(self.env['basedata.cus_register_company'].search(
                #     [('register_name_cn', 'ilike', '博越'+'%')]))
                # print(self.env['basedata.cus_register_company'].search(
                #     [('register_name_cn', 'ilike', '博越')]))
                #
                # print(self.env['basedata.cus_register_company'].search(
                #     [('register_name_cn', 'ilike', '博越')]))
                #
                # # 博越锦程国际物流（北京）有限公司
                # # basedata.cus_register_company(505, 8085)
                # # basedata.cus_register_company(505, 8085)
                # # basedata.cus_register_company(505, 6157, 8085, 19784, 39841, 47740, 203094, 250703, 298609, 304804)
                # # basedata.cus_register_company(505, 6157, 8085, 19784, 39841, 47740, 203094, 250703, 298609, 304804)




