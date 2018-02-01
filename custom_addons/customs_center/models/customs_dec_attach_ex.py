# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    """ 扩展原附件模型 增加字段报关单附件类型"""
    _inherit = 'ir.attachment'

    attach_type = fields.Selection([('00000001', u'00000001:发票'),
                                 ('00000002', u'00000002:装箱单'),
                                 ('00000003', u'00000003:提运单'),
                                 ('00000004', u'00000004:合同'),
                                 ('00000005', u'00000005:其他'),
                                 ('10000001', u'10000001:代理委托协议'),
                                 ('10000002', u'10000002:减免税货物税款担保证明'),
                                 ('10000003', u'10000003:减免税货物税款担保延期证明')], string="DEC attach type") # 报关单附件类型