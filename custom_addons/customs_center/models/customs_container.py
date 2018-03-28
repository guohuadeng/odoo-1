# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class DecContainer(models.Model):
    """ 关务中心 集装箱信息 """
    _name = 'customs_center.dec_container'
    rec_name = 'containerNo'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'customs center container'

    # 关联报关单 多对一
    customs_declaration_id = fields.Many2one(comodel_name="customs_center.customs_dec", string="customs declaration",
                                             copy=False)
    containerNo = fields.Char(string="container No")  # 集装箱号
    weight = fields.Float(string="Gross Weight")      # 自重
    spec_code = fields.Selection(string="State", selection=[('S', 'Small Container'),('L', 'Large Container')], default='S')  # 规格

    @api.constrains('containerNo', 'spec_code')
    def _check_container_no(self):
        """集装箱号规则"""
        char_code = "0123456789A?BCDEFGHIJK?LMNOPQRSTU?VWXYZ"
        for container in self:
            str_code = container.containerNo
            str_spec_code = container.spec_code
            if not str_code and str_spec_code:
                raise ValidationError(_(u'如果需要录入集装箱信息，装箱号不能为空!'))
            elif len(str_code) != 11:
                raise ValidationError(_('The length of container num is wrong!'))
            num = 0
            for i in range(0, 10):
                idx = char_code.find(str_code[i])
                if idx == -1 or char_code[idx] == '?':
                    raise ValidationError(_("The container num contains invalid char"))
                idx = idx * (2 ** i)
                num += idx
            num = (num % 11) % 10
            if num != int(str_code[-1]):
                raise ValidationError(_("The validate code is wrong!"))