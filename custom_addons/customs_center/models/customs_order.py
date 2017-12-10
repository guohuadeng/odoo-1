# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
from collections import OrderedDict
_logger = logging.getLogger(__name__)


class CustomsOrder(models.Model):
    """ 通关清单 """
    _name = 'customs_center.customs_order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'name'
    _description = 'Customs Customs Order'

    name = fields.Char(string="Name")   # 通关清单流水号
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")                 # 客户 (委托单位)
    work_sheet_id = fields.Many2one(comodel_name="work_sheet", string="Work Sheet")              # 工作单ID

    business_type = fields.Many2one(comodel_name="business_type", string="Business Type")   # 业务类型
    inout = fields.Selection(string="InOut", selection=[('i', 'Import'), ('e', 'Export'), ], required=True)   # 进出口类型
    customs_id = fields.Many2one(comodel_name="delegate_customs", string="Customs")              # 进出口岸
    custom_master_id = fields.Many2one(comodel_name="delegate_customs", string="Declare Customs")  # 申报口岸/海关
    ManualNo = fields.Char(string="Manual No")                                                   # 备案号
    customer_contract_no = fields.Char(string="Customer Contract No")                            # 合同号
    licenseNo = fields.Char(string="License No")                                                 # 许可证号

    declare_company_id = fields.Many2one(comodel_name="basedata.cus_register_company", string="declare company name")  # 申报单位 新建企业库表
    input_company_id = fields.Many2one(comodel_name="basedata.cus_register_company", string="input company id")  # 消费使用单位 新建企业库表
    business_company_id = fields.Many2one(comodel_name="basedata.cus_register_company", string="business company name")    # 收发货人 新建企业库表

    transport_mode_id = fields.Many2one(comodel_name="delegate_transport_mode",
                                        string="Transport Mode")                                 # 运输方式
    transport_name = fields.Char(string="transport name")                                        # 运输工具名称
    VoyageNo = fields.Char(string="Voyage No")                                                   # 航次号

    trade_terms_id = fields.Many2one(comodel_name="delegate_trade_terms", string="Trade Term")   # 成交方式 or 贸易条款
    trade_mode_id = fields.Many2one(comodel_name="delegate_trade_mode", string="Trade Mode")     # 监管方式
    CutMode_id = fields.Many2one(comodel_name="basedata.cus_cut_mode", string="CutMode id")      # 征免性质   征免性质表待新建
    packing_id = fields.Many2one(comodel_name="delegate_packing", string="Package Type")         # 包装方式
    trade_country_id = fields.Many2one(comodel_name="delegate_country",
                                       string="Trade Country")                                   # 贸易国别
    origin_arrival_country_id = fields.Many2one(comodel_name="delegate_country",
                                                string="Origin Arrival Country")                 # 启运/抵达国
    port_id = fields.Many2one(comodel_name="delegate_port", string="Port", )                     # 装货/指运港
    region_id = fields.Many2one(comodel_name="delegate_region", string="Region")                 # 境内目的/货源地
    qty = fields.Integer(string="Qty")                                                           # 件数
    gross_weight = fields.Float(string="Gross Weight")                                           # 毛重
    net_weight = fields.Float(string="Net Weight")                                               # 净重
    marks = fields.Text(string="Marks")                                                          # 标记备注

    # 关联报关单 1对多关系
    customs_declaration_ids = fields.One2many(comodel_name="customs_center.customs_dec",
                                              inverse_name="customs_order_id", string="customs declaration")
    # 关联通关清单商品列表 1对多关系
    cus_goods_list_ids = fields.One2many(comodel_name="customs_center.cus_goods_list",
                                         inverse_name="customs_order_id", string="cus goods name")
    customs_order_state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], default='draft')  # 通关清单
    # 第一种写法 通关清单点击保存的时候 更改状态为成功
    # @api.multi
    # def write(self, vals):
    #     obj = super(CustomsOrder, self).write(vals)
    #     self.env['customs_center.customs_order'].update({'customs_order_state': 'succeed'})
    #     return obj

    # @api.multi
    # def write(self, vals):
    #     obj = super(CustomsOrder, self).write(vals)
    #     obj.update({'customs_order_state': 'succeed'})
    #     print('hahahhahahahahhahahahhahahahaahahahha')
    #     return True

    def generate_customs_declaration(self, vals):
        """ 生成报关单 """
        for line in self:
            # goods = line.cus_goods_list_ids
            # goods_dic = {}
            # for goods_dic_item in goods:
            #     goods_dic = {
            #         'cus_goods_tariff_id': goods_dic_item.cus_goods_tariff_id,
            #         'goods_model': goods_dic_item.goods_model,
            #         'deal_qty': goods_dic_item.deal_qty,
            #         'deal_unit_price': goods_dic_item.deal_unit_price,
            #     }
            # # dic = {item: dic[item] for item in dic if dic[item]}
            # # dic.update(dic)

            dic = {
                'inout': line.inout,
                'customs_order_id': line.id,
                'customs_id': line.customs_id.id,
                'custom_master_id': line.custom_master_id.id,
                'ManualNo': line.ManualNo,
                'customer_contract_no': line.customer_contract_no,
                'licenseNo': line.licenseNo,
                'declare_company_id': line.declare_company_id.id,
                'input_company_id': line.input_company_id.id,
                'business_company_id': line.business_company_id.id,
                'transport_mode_id': line.transport_mode_id.id,
                'transport_name': line.transport_name,
                'VoyageNo': line.VoyageNo,
                'trade_terms_id': line.trade_terms_id.id,
                'trade_mode_id': line.trade_mode_id.id,
                'CutMode_id': line.CutMode_id.id,
                'packing_id': line.packing_id.id,
                'trade_country_id': line.trade_country_id.id,
                'origin_arrival_country_id': line.origin_arrival_country_id.id,
                'port_id': line.port_id.id,
                'region_id': line.region_id.id,
                'qty': line.qty,
                'gross_weight': line.gross_weight,
                'net_weight': line.net_weight,
                'remarks': line.marks,
               #  'dec_goods_list_ids': goods_dic,
                'dec_goods_list_ids': line.cus_goods_list_ids,
            }
            print("PPPPPPPPPPPPP PPPPPPPPP PPPPPPPPPPP")
            print(line.cus_goods_list_ids)
            print(line.cus_goods_list_ids.ids)
            print(self.env['customs_center.cus_goods_list'].customs_order_id.ids)
            # customs_center.cus_goods_list(1, 2)
            # [1, 2]
            # []


            dic = {item: dic[item] for item in dic if dic[item]}
            dic.update(dic)

            @api.multi
            def create(self, vals):
                obj = super(CustomsDeclaration, self).create(vals)
                return obj
            customs_declaration_obj = self.env['customs_center.customs_dec'].create(dic)

            # 获取当前对象下的报关单ID
            # customs_order_obj = self.env['customs_center.customs_order']
            # print(customs_order_obj)
            # customs_clearance_obj = customs_order_obj.customs_declaration_ids
            print(customs_declaration_obj)
            return {
                'name': "Customs Center Clearance",
                'type': "ir.actions.act_window",
                'view_type': 'form',
                'view_mode': 'form, tree',
                'res_model': 'customs_center.customs_dec',
                'views': [[False, 'form']],
                'res_id': customs_declaration_obj.id,
                # 'target': 'current'
                'target': 'main'
            }

    # @api.multi
    # def customs_center_clearance(self):
    #     """从通关清单 跳转到报关单界面"""
    #     for obj in self:
    #         customs_clearance_obj = obj.customs_declaration_ids[0]
    #         return {
    #             'name': "Customs Center Clearance",
    #             'type': "ir.actions.act_window",
    #             'view_type': 'form',
    #             'view_mode': 'form, tree',
    #             'res_model': 'customs_center.customs_dec',
    #             'views': [[False, 'form']],
    #             'res_id': customs_clearance_obj.id,
    #             'target': 'current'
    #         }




    # @api.multi
    # def generate_customs_declaration(self):
    #     """ 生成报关单 """
    #     # if len(self.mapped('cus_goods_list_ids')) != 1:
    #     #     raise UserError(_("有多个商品"))
    #     customs_order_info_dic = dict()
    #     for line in self:
    #         customs_order_info_dic.update({
    #             'default_inout': line.inout,
    #             'default_customs_id': line.customs_id.id,
    #             'default_custom_master_id': line.custom_master_id.id,
    #             'default_ManualNo': line.ManualNo,
    #             'default_customer_contract_no': line.customer_contract_no,
    #             'default_licenseNo': line.licenseNo,
    #             'default_declare_company_id': line.declare_company_id.id,
    #             'default_input_company_id': line.input_company_id.id,
    #             'default_business_company_id': line.business_company_id.id,
    #             'default_transport_mode_id': line.transport_mode_id.id,
    #             'default_transport_name': line.transport_name,
    #             'default_VoyageNo': line.VoyageNo,
    #             'default_trade_terms_id': line.trade_terms_id.id,
    #             'default_trade_mode_id': line.trade_mode_id.id,
    #             'default_CutMode_id': line.CutMode_id.id,
    #             'default_packing_id': line.packing_id.id,
    #             'default_trade_country_id': line.trade_country_id.id,
    #             'default_origin_arrival_country_id': line.origin_arrival_country_id.id,
    #             'default_port_id': line.port_id.id,
    #             'default_region_id': line.region_id.id,
    #             'default_qty': line.qty,
    #             'default_gross_weight': line.gross_weight,
    #             'default_net_weight': line.net_weight,
    #             'default_remarks': line.marks,
    #         })
    #     # print('**************^^^^^^^^^^^&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&^^^^^^^^^^^^^^****************')
    #     for item in customs_order_info_dic.items():
    #         print(item)
    #
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'customs_center.customs_dec',
    #         'target': 'current',
    #         'context': customs_order_info_dic,
    #     }


    @api.model
    def create(self, vals):
        """设置原始清单命名规则"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('code_customs_order') or _('New')
        result = super(CustomsOrder, self).create(vals)
        return result


class WorkSheet(models.Model):
    """" 工作单 """
    _inherit = 'work_sheet'

    customs_order_ids = fields.One2many(comodel_name="customs_center.customs_order", inverse_name="work_sheet_id",
                                          string="Customs Order")
    customs_order_state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], compute='_get_customs_state')

    @api.depends('customs_order_ids')
    def _get_customs_state(self):
        """ 获取当前工作单对应的通关清单 状态"""
        for sheet in self:
            if sheet.customs_order_ids:
                customs_obj = sheet.customs_order_ids[0]
                sheet.customs_order_state = customs_obj.customs_order_state

    @api.constrains('customs_order_ids')
    def _check_clearance_one2one(self):
        """ 工作单 关联通关清单 一对一唯一约束校验"""
        for item in self:
            if len(item.customs_order_ids) > 1:
                raise ValidationError(_('work sheet must relate only one clearance draft'))

    @api.model
    def create(self, vals):
        """当创建工作单时，如果“关务中心报关”被选上 则创建通关清单"""
        obj = super(WorkSheet, self).create(vals)
        if vals.get('custom_center'):
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
            self.env['customs_center.customs_order'].create(dic)
        return obj

    @api.multi
    def customs_center_clearance(self):
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
                'res_model': 'customs_center.customs_order',
                'views': [[False, 'form']],
                'res_id': customs_clearance_obj.id,
                'target': 'current'
            }






