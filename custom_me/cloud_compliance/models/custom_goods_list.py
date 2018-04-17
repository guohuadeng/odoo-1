# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging,xmlrpclib
from . import custom_models,compliance_config
from collections import OrderedDict
_logger = logging.getLogger(__name__)

class Custom_Goods_List(models.Model):
    """云合规——通关清单"""
    _name = 'goods.list'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'name'
    _description = 'Custom Goods List'

    name = fields.Char(string="Name", copy=False)   # 清单序号   # copy=False 防止服务器动作复制报关单信息时复制

    inout = fields.Selection(string="InOut", selection=[('i', u'进口'), ('e', u'出口'), ], required=True)   # 进出口类型

    customs_id = fields.Many2one(comodel_name="cus_args.customs", string="Customs") # 进出口岸

    custom_master_id = fields.Many2one(comodel_name="cus_args.customs", string="Declare Customs")   # 申报口岸/海关

    manual_no = fields.Char(string="Manual No") # 备案号

    customer_contract_no = fields.Char(string="Customer Contract No")   # 合同号

    license_no = fields.Char(string="License No")    # 许可证号

    business_company_id = fields.Char(string="business company name")   # 客户公司

    transport_mode_id = fields.Many2one(comodel_name="cus_args.transport_mode", string="Transport Mode")    # 运输方式

    transport_name = fields.Char(string="transport name")   # 运输工具名称

    voyage_no = fields.Char(string="Voyage No") # 航次号

    trade_terms_id = fields.Many2one(comodel_name="cus_args.trade_terms", string="Trade Term")  # 成交方式 or 贸易条款

    trade_mode_id = fields.Many2one(comodel_name="cus_args.trade_mode", string="Trade Mode")    # 监管方式

    cut_mode_id = fields.Many2one(comodel_name="cus_args.cut_mode", string="CutMode id") # 征免性质   征免性质表待新建

    packing_id = fields.Many2one(comodel_name="cus_args.wrap_type", string="Package Type")    # 包装方式

    trade_country_id = fields.Many2one(comodel_name="cus_args.country", string="Trade Country") # 贸易国别

    origin_arrival_country_id = fields.Many2one(comodel_name="cus_args.country", string="Origin Arrival Country")   # 启运/抵达国

    port_id = fields.Many2one(comodel_name="cus_args.port", string="Port")  # 装货/指运港

    region_id = fields.Many2one(comodel_name="cus_args.internal_district", string="Region")    # 境内目的/货源地

    qty = fields.Integer(string="Qty")  # 件数

    gross_weight = fields.Float(string="Gross Weight")  # 毛重

    net_weight = fields.Float(string="Net Weight")  # 净重

    marks = fields.Text(string="Marks") # 标记备注

    list_model = fields.Many2one(comodel_name="compliance.model", string="Compliance Model", )  # 清单模版

    state = fields.Selection(selection=[('draft', 'Draft'),  # 草稿
                                        ('sented', 'Sented')  # 已发送
                                        ], string='states', readonly=True, default='draft')

    user_name = fields.Char(string="User Name")  # 用户登录名

    user_pwd = fields.Char(string="User Password")   # 用户登录密码

    user_dbname = fields.Char(string="User Database Name")# 用户登陆数据库名

    url_post = fields.Char(string="Url")    # 目标url地址

    @api.onchange('list_model')
    def _generate_about_model(self):
        """根据当前选择模板的变化 改变其它相关内容 通过onchange装饰器，自动执行_generate_about_name方法"""
        for goods_list in self:
            if goods_list.list_model:
                """调用模板中内容"""
                goods_list.inout = goods_list.list_model.inout
                goods_list.customs_id = goods_list.list_model.customs_id
                goods_list.manual_no = goods_list.list_model.manual_no
                goods_list.customer_contract_no = goods_list.list_model.customer_contract_no
                goods_list.license_no = goods_list.list_model.license_no
                goods_list.business_company_id = goods_list.list_model.business_company_id
                goods_list.transport_mode_id = goods_list.list_model.transport_mode_id
                goods_list.transport_name = goods_list.list_model.transport_name
                goods_list.voyage_no = goods_list.list_model.voyage_no
                goods_list.trade_terms_id = goods_list.list_model.trade_terms_id
                goods_list.cut_mode_id = goods_list.list_model.cut_mode_id
                goods_list.packing_id = goods_list.list_model.packing_id
                goods_list.trade_country_id = goods_list.list_model.trade_country_id
                goods_list.origin_arrival_country_id = goods_list.list_model.origin_arrival_country_id
                goods_list.port_id = goods_list.list_model.port_id
                goods_list.region_id = goods_list.list_model.region_id

    @api.multi
    def sent_url(self):
        """发送云合规版的通关清单到关务中心的通关清单"""
        username = 'admin'  # 用户登录名
        pwd = 'admin'  # 用户的登录密码，测试时请换成自己的密码
        dbname = 'custom'  # 数据库帐套名，测试时请换成自己的帐套名
        # 第一步，取得uid
        sock_common = xmlrpclib.ServerProxy('http://0.0.0.0:8069/xmlrpc/common')
        uid = sock_common.login(dbname, username, pwd)
        # replace localhost with the address of the server
        sock = xmlrpclib.ServerProxy('http://0.0.0.0:8069/xmlrpc/object')

        # 调用cus_center.customs_order对象的create方法在数据库中插入一个业务伙伴
        goods_list_text = {

            'inout': self.inout,
            'customs_id': self.customs_id.id,
            'manual_no': self.manual_no,
            'custom_master_id': self.custom_master_id.id,
            'customer_contract_no': self.customer_contract_no,
            'license_no': self.license_no,
            'transport_mode_id': self.transport_mode_id.id,
            'voyage_no': self.voyage_no,
            'origin_arrival_country_id': self.origin_arrival_country_id.id,
            'port_id': self.port_id.id,
            'internal_district_id': self.region_id.id,
            'qty': self.qty,
            'gross_weight': self.gross_weight,
            'net_weight': self.net_weight,
        }
        goods_list_text_id = sock.execute(dbname, uid, pwd, 'cus_center.customs_order', 'create', goods_list_text)

        self.update({'state': 'sented'})
        for goods_list in self:
            body = (_("清单序号：%s ：已成功发送！<br/>") % (goods_list.name))
            goods_list.message_post(body=body)

    @api.model
    def create(self, vals):
        """设置通关清单命名规则"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('code_list') or _('New')
        result = super(Custom_Goods_List, self).create(vals)
        return result