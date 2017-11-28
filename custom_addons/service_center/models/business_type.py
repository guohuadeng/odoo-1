# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class BusinessType(models.Model):
    """向业务类型模型中加入工作单字段"""
    _inherit = 'business_type'

    work_sheet_ids = fields.One2many(comodel_name="work_sheet", inverse_name="business_type", string="work sheet")
    draft_sheet_no = fields.Integer(string="Draft Sheet nums", compute='_count_draft_work_sheet')
    confirmed_sheet_no = fields.Integer(string="Confirmed Sheet nums", compute='_count_confirmed_work_sheet')

    @api.multi
    def _count_draft_work_sheet(self):
        for obj in self:
            sheets= self.env['work_sheet'].search(
                [('business_type', '=', obj.id),
                 ('customer_service', '=', self.env.uid),
                 ('state', '=', 'draft')])
            obj.draft_sheet_no = len(sheets)

    @api.multi
    def _count_confirmed_work_sheet(self):
        for obj in self:
            sheets = self.env['work_sheet'].search(
                [('business_type', '=', obj.id),
                 ('customer_service', '=', self.env.uid),
                 ('state', '=', 'confirmed')])
            obj.complete_sheet_no = len(sheets)

    @api.multi
    def open_work_sheet_action(self):
        """点击按钮跳转到相应的工作单窗口"""
        action_dic = {
            'SI': 'service_center.work_sheet_sea_import',
            'SE': 'service_center.work_sheet_sea_export',
            'AI': 'service_center.work_sheet_air_import',
            'AE': 'service_center.work_sheet_air_export',
        }
        action_name = self._context.get('action_name')
        context = self._context.copy()
        action_xml_id = action_dic.get(action_name)
        [action] = self.env.ref(action_xml_id).read()
        action['context'] = context

        return action

    @api.multi
    def create_work_sheet(self):
        """从看板中创建新的工作单"""
        business_type = self._context.get('default_business_type')
        return {
            'name': _('Work Sheet'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'work_sheet',
            'context': {'default_business_type': business_type} if business_type else None,
        }
