# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class DecResult(models.Model):
    """ 报关单回执 """
    _name = 'customs_center.dec_result'
    _rec_name = 'seq_No'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Custom Declaration Result'

    seq_No = fields.Char(string="SeqNo", required=False, size=18, index=True)                  # 数据中心统一编号
    status_id = fields.Many2one(comodel_name="customs_center.dec_res_status", string="Status", required=False, ) # 回执状态
    message = fields.Char(string="Message", required=False, size=255)  # 报关单服务错误信息（回执信息）
    notice_date = fields.Datetime(string="Notice Date", required=False, default=fields.Datetime.now)          # 回执时间
    sequence = fields.Integer(string="Sequence", compute='_compute_seq_no')

    customs_declaration_id = fields.Many2one(comodel_name="customs_center.customs_dec",
                                             string="Customs Declaration")          # 关联报关单

    @api.depends('status_id')
    def _compute_seq_no(self):
        """根据关联状态得到序号"""
        for obj in self:
            obj.sequence = obj.status_id.sequence

