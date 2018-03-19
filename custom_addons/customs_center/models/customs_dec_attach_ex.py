# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    """ 扩展原附件模型 增加字段报关单附件类型"""
    _inherit = 'ir.attachment'

    dec_edoc_type = fields.Selection(string=u"随附单据类型",
                                         selection=[('00000001', u'发票'),
                                                    ('00000002', u'装箱单'),
                                                    ('00000003', u'提运单'),
                                                    ('00000004', u'合同'),
                                                    ('00000005', u'其他'),
                                                    ('10000001', u'代理委托协议'),
                                                    ('10000002', u'减免税货物税款担保证明'),
                                                    ('10000003', u'减免税货物税款担保延期证明')]
                                         ,required=False)   # 报关单附件类型