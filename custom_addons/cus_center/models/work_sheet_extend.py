# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class WorkSheet(models.Model):
    """" 工作单 """
    _inherit = 'work_sheet'

    # 工作单与通关清单的关联关系是一对一
    customs_order_ids = fields.One2many(comodel_name="cus_center.customs_order", inverse_name="work_sheet_id",
                                        string="Customs Order")

    @api.constrains('customs_order_ids')
    def _check_clearance_one2one(self):
        """ 工作单 关联通关清单 一对一唯一约束校验"""
        for item in self:
            if len(item.customs_order_ids) > 1:
                raise ValidationError(_('work sheet must relate only one clearance draft'))

    @api.model
    def create(self, vals):
        """当创建工作单时，如果“报关”被选上 则创建通关清单"""
        obj = super(WorkSheet, self).create(vals)
        if vals.get('custom'):
            dic = {
                'customer_id': obj.customer,
                'work_sheet_id': obj.id,
                'inout': obj.business_type.in_out,
                # 'business_company_id': obj.consignee if obj.in_out == 'i' else obj.consignor,
                'customer_contract_no': obj.customer_contract_no,
                'trade_terms_id': obj.deal_type.trade_term_id if obj.deal_type else False,
                'trade_mode_id': obj.trade_mode_id,
                'transport_mode_id': obj.business_type.transport_mode,
                'qty': obj.qty,
                'gross_weight': obj.gross_weight,
                'customs_id': obj.sale_order_no.customs[0] if obj.sale_order_no and obj.sale_order_no.customs else False,
                'trade_country_id': obj.sale_order_no.trade_country if obj.sale_order_no else False,
                'port_id': obj.sale_order_no.port if obj.sale_order_no else False,
                'region_id': obj.sale_order_no.region if obj.sale_order_no else False,
                'wrap_type': obj.wrap_type
            }

            dic = {item: dic[item] for item in dic if dic[item]}  # 清除False
            _dic = {}  # 把object转换为id
            for item in dic:
                if item in {'customer_id', 'trade_terms_id', 'trade_mode_id',
                            'transport_mode_id', 'customs_id', 'trade_country_id', 'port_id', 'region_id'}:
                    _dic[item] = dic[item].id
            dic.update(_dic)
            self.env['cus_center.customs_order'].create(dic)
        return obj

    @api.multi
    def write(self, vals):
        """重写修改方法，实现再次编辑工作单的时候 勾选报关 也创建通关清单"""
        for obj in self:
            if 'custom' in vals:
                if not obj.custom and not obj.customs_order_ids:  # 如果报关选项 没有勾选且没有关联的通关清单
                    dic = {
                        'customer_id': obj.customer,
                        'work_sheet_id': obj.id,
                        'inout': obj.business_type.in_out,
                        'business_type': obj.business_type.id,
                        # 'business_company_id': obj.consignee if obj.in_out == 'i' else obj.consignor,
                        'customer_contract_no': obj.customer_contract_no,
                        'trade_terms_id': obj.deal_type.trade_term_id if obj.deal_type else False,
                        'trade_mode_id': obj.trade_mode_id,
                        'transport_mode_id': obj.business_type.transport_mode,
                        'qty': obj.qty,
                        'gross_weight': obj.gross_weight,
                        'customs_id': obj.sale_order_no.customs[
                            0] if obj.sale_order_no and obj.sale_order_no.customs else False,
                        'trade_country_id': obj.sale_order_no.trade_country if obj.sale_order_no else False,
                        'port_id': obj.sale_order_no.port if obj.sale_order_no else False,
                        'region_id': obj.sale_order_no.region if obj.sale_order_no else False,
                        'wrap_type': obj.wrap_type
                    }

                    dic = {item: dic[item] for item in dic if dic[item]}  # 清除False
                    _dic = {}  # 把object转换为id
                    for item in dic:
                        if item in {'customer_id', 'trade_terms_id', 'trade_mode_id',
                                    'transport_mode_id', 'customs_id', 'trade_country_id', 'port_id', 'region_id'}:
                            _dic[item] = dic[item].id
                    dic.update(_dic)
                    self.env['cus_center.customs_order'].create(dic)
        return super(WorkSheet, self).write(vals)

    @api.multi
    def cus_center_clearance(self):
        """从服务中心 跳转到关务中心通关清单界面"""
        for obj in self:
            if not obj.customs_order_ids:
                return

            customs_clearance_obj = obj.customs_order_ids[0]
            return {
                'name': "Customs Center Clearance",
                'type': "ir.actions.act_window",
                'view_type': 'form',
                'view_mode': 'form, tree',
                'res_model': 'cus_center.customs_order',
                'views': [[False, 'form']],
                'res_id': customs_clearance_obj.id,
                'target': 'current'
            }
