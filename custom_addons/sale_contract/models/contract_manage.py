# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class SaleContractManage(models.Model):
    """销售合同管理"""
    _name = 'contract.sale_contract'
    _inherit = ['mail.thread']
    _description = 'sale contract manage model'
    _rec_name = 'name'

    name = fields.Char('Number', index=True, readonly=True)     # 合同号
    customer = fields.Many2one('res.partner', string='Customer', required=True)       # 客户
    contract_type = fields.Many2one(comodel_name="contract.contract_type", string="Contract type", required=True, )   # 合同类型

    # '我方签约人 关联公司联系人列表'  默认为当前登录账户 default=lambda self: self.env.user
    our_signatory = fields.Many2one('res.users', string='Our signatory', default=lambda self: self.env.user)     # 我方签约人
    inner_num = fields.Char(string="Inner Num", required=False, )   # 内部合同号
    # '客户签约人  关联客户联系人表'
    customer_signatory = fields.Many2one(comodel_name="res.partner", string="Customer signatory", required=True)     # 客户签约人

    # 合同开始时间
    contract_effective_date = fields.Datetime(string='Effective Time', required=True)     # 合同生效日期
    # 合同结束时间
    contract_failure_date = fields.Datetime(string='Failure time', required=True)     # 合同终止日期
    # 备注说明
    note = fields.Text(string='Remarks')   # 备注说明

    _sql_constraints = [
        ('contract_sale_contract_name_uniq', 'UNIQUE (name)', 'sale contract number must be unique!')
    ]

    @api.model
    def create(self, vals):
        """创建合同时，自动生成合同号"""
        vals['name'] = self.env['ir.sequence'].next_by_code('sale_contract')
        result = super(SaleContractManage, self).create(vals)
        return result

    @api.multi
    def create_sale_order(self):
        """新建销售订单"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Quotation Order'),
            'res_model': 'sale.order',
            'view_mode': 'form, tree',
            'view_type': 'form',
            'nodestory': True,
            'target': 'current'
        }

    @api.multi
    def action_confirm(self):
        """发送邮件给客户"""
        pass

    @api.multi
    def action_confirm(self):
        """确认按钮动作"""
        pass

    @api.multi
    def action_cancel(self):
        """取消生成报价单动作"""
        pass


    @api.multi
    def print_quotation(self):
        """打印报价单"""
        pass

    @api.multi
    def action_draft(self):
        """发送报价单"""
        pass

    @api.multi
    def action_done(self):
        """确认"""
        pass


class SaleContractType(models.Model):
    """ 销售合同类型 """
    _name = 'contract.contract_type'
    _description = 'sale contract type'
    _rec_name = 'name'

    # 备注说明
    remark = fields.Text(string='Remark')
    name = fields.Char(string="Type Name", required=True, )
    code = fields.Char(string="Code", required=True)

