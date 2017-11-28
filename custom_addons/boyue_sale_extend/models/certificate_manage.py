# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class CertificateType(models.Model):
    """ 证书类型 """
    _name = 'certificate_type'
    _description = 'certificate type'
    _rec_name = 'certificate_type'

    certificate_type = fields.Char(string='Certificate Type', translate=True)
    level = fields.One2many(comodel_name='certificate_level', inverse_name='certificate_type',
                            string='Level', required=True)


class CertificateLevel(models.Model):
    """ 证书等级 """
    _name = 'certificate_level'
    _description = 'certificate level'
    _rec_name = 'certificate_level'

    certificate_type = fields.Many2one(comodel_name='certificate_type', string='Certificate Type', required=False)
    certificate_level = fields.Char(string='Level', required=False)


class CertificateManagement(models.Model):
    """ 证书管理 """
    _name = 'certificate_management'
    _description = 'certificate management'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'certificate_no'

    customer = fields.Many2one(comodel_name='res.partner', string='Customer')
    issuing_authority = fields.Char(string='Issuing Authority',   required=True)
    authorization_date = fields.Datetime(string='AuthorizationDate', required=True)
    expiration_date = fields.Datetime(string='ExpirationDate', required=True)
    certificate_no = fields.Char(string='Code', translate=True, required=True)
    certificate_type = fields.Many2one(comodel_name='certificate_type', string='Type', required=True)
    certificate_level = fields.Many2one(comodel_name='certificate_level', string='Level', required=False)
    remark = fields.Text(string='Remark')
    state = fields.Selection(selection=[('new', 'New'),    # 新建
                                        ('pending', 'ending'),  # 挂起/即将过期
                                        ('cancel', 'Cancel'),  # 取消
                                        ], string='status', default='new', track_visibility='onchange')
    #  domain=[('certificate_type', '=', certificate_type)]

    @api.multi
    def create_certificate(self):
        """ 创建证书 """
        pass

    @api.multi
    def action_confirm(self):

        pass

    @api.multi
    def action_cancel(self):

        pass

    @api.multi
    def action_done(self):
        """ 确认 """
        pass

    @api.multi
    @api.onchange('certificate_type')
    def _compute_certificate_level(self):
        for item in self:
            levels = item.certificate_type.level
            item.certificate_level = (levels[0] if levels else False)

    @api.multi
    def setting_certificate_expiration(self):
        """设置证书为即将过期"""
        self.update({'state': 'pending'})
        for certificate in self:
            body = (_(u"客户：%s 的证书:%s 即将过期 ！<br/>") % (certificate.customer.name, certificate.certificate_type.certificate_type))
            certificate.message_post(body=body, message_type='email')

