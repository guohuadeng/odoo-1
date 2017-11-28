# -*- coding: utf-8 -*-
from odoo import models, fields, api


# class BusinessStatus(models.Model):
#     _name = 'service_center.business_status'
#     _rec_name = 'name'
#
#     name = fields.Char(string='Name')
#     state_type = fields.Selection(string="Type", selection=[
#         ('todo', 'ToDo'),
#         ('doing', 'Doing'),
#         ('done', 'Done'),
#         ('exception', 'Exception')
#     ], default='todo')
#     business_stage = fields.Many2one(comodel_name="service_center.business_stage", string="Business Stage")
#     remark = fields.Text(string="Remark")


# class BusinessStage(models.Model):
#     _name = 'service_center.business_stage'
#     _rec_name = 'name'
#     _order = 'sequence, name'
#
#     name = fields.Char(string='Name', copy=True)
#     sequence = fields.Integer(string="Sequence")
#     business_status = fields.One2many(comodel_name="service_center.business_status", inverse_name="business_stage",
#                                     string="Business Status", copy=True)
#     stage_type = fields.Selection(string="", selection=[
#         ('delegate', 'Delegate'),
#         ('booking', 'Booking'),
#         ('boxing', 'Boxing'),
#         ('transform', 'Transform'),
#         ('sheeting', 'Sheeting'),
#         ('other', 'Other')], required=False, copy=True)
#     remark = fields.Text(string="Remark", copy=True)
#     status = fields.Many2one(comodel_name="service_center.business_status", string="Type", copy=False)  # domain=[('id', 'in', business_status)]
#     is_template = fields.Boolean(string="Is Template", default=False, copy=False)
#     template_stage = fields.Many2one(comodel_name="service_center.business_stage", string="Sub stage",
#                                      copy=False, ondelete='cascade', )
#     child_stage = fields.One2many(comodel_name="service_center.business_stage", inverse_name="template_stage",
#                                   string="Child stage", copy=False)
#     work_sheet = fields.Many2one(comodel_name="work_sheet", string="work sheet", required=False, copy=False )
#
#
#     @api.model
#     def create(self, vals):
#         """重写创建方法，如果此对象是模板则在每个工作单对象中的业务阶段中插入此对象"""
#         res = super(BusinessStage, self).create(vals)
#         is_template = vals.get('is_template')
#         if is_template == True:
#             work_sheets = self.env['work_sheet'].search([])
#             for work_sheet in work_sheets:
#                 obj = res.copy()
#                 res.child_stage |= obj
#                 work_sheet.business_stage |= obj
#
#         return res
#
#     @api.multi
#     def write(self, vals):
#         """重写修改方法，如果此对象是模板则在每个工作单对象中的业务阶段中对应的对象进行修改"""
#         res = super(BusinessStage, self).write(vals)
#         for stage in self:
#             if stage.is_template == True:
#                 for item in self.child_stage:
#                     item.write(vals)
#
#         return res


class BusinessStatus(models.Model):
    _name = 'service_center.business_status'
    _rec_name = 'name'
    _order = 'sequence, name'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", required=True)
    remark = fields.Text(string="Remark")
    active = fields.Boolean(string="Active", default=True)
    state_type = fields.Selection(string="Type", selection=[
        ('todo', 'ToDo'),
        ('doing', 'Doing'),
        ('done', 'Done'),
        ('exception', 'Exception')
    ], default='todo')
    business_stage_id = fields.Many2one(comodel_name="service_center.business_stage",
                                        string="Business Stage", required=True, ondelete='cascade')


class BusinessStage(models.Model):
    _name = 'service_center.business_stage'
    _rec_name = 'name'
    _order = 'business_type, sequence'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", required=True)
    type = fields.Selection(string="Type", selection=[
        ('delegate', 'Delegate'),
        ('booking', 'Booking'),
        ('warehouse', 'Warehouse'),
        ('boxing', 'Boxing'),
        ('transform', 'Transform'),
        ('sheeting', 'Sheeting'),
        ('other', 'Other')], required=False, )
    remark = fields.Text(string="Remark")
    active = fields.Boolean(string="Active", default=True)
    business_status_id = fields.One2many(comodel_name="service_center.business_status",
                                         inverse_name="business_stage_id", string="Business Status")
    business_type = fields.Many2one(comodel_name="business_type", string="Business Type", required=True)


class CurrentState(models.Model):
    _name = 'service_center.current_state'
    _inherit = ['mail.thread']
    _description = 'Current State'

    work_sheet_id = fields.Many2one(comodel_name="work_sheet", string="Work Sheet", required=True, ondelete='cascade')
    business_stage_id = fields.Many2one(comodel_name="service_center.business_stage",
                                        string="Business Stage", required=True, readonly=True)
    business_status_id = fields.Many2one(comodel_name="service_center.business_status",
                                         string="Business Status", track_visibility=True)
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Integer(string="Sequence", compute='_get_sequence')

    @api.depends('business_stage_id')
    def _get_sequence(self):
        for item in self:
            item.sequence = item.business_stage_id.sequence

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u'%s-%s'%(record.work_sheet_id.name, record.business_stage_id.name))
            )
        return result

