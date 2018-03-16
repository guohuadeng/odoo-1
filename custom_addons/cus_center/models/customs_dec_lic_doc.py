# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DecLicenseDoc(models.Model):
    """ 随附单证 """
    _name = 'cus_center.dec_lic_doc'
    _rec_name = 'dec_license_no'
    _description = 'DecLicenseDoc'

    dec_license_no = fields.Char(string="License No")  # 单证编号
    # 多对一关联 报关单
    customs_declaration_id = fields.Many2one(comodel_name="cus_center.customs_dec", string="customs declaration")
    dec_license_doc_type_id = fields.Many2one(comodel_name="cus_args.dec_license_doc_type", string="DecLicenseDoc type")   # 单证类型/单证代码

