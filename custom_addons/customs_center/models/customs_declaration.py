# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import odoo.addons.decimal_precision as dp
import odoo.addons.queue_job.job as q_job
from odoo.tools import config
import logging, os, shutil
from lxml import etree
from collections import OrderedDict
import uuid
from datetime import datetime, timedelta
from odoo.exceptions import UserError

# from custom_addons.customs_center.utils.to_xml_message import delegate_to_xml
from ..utils.to_xml_message import delegate_to_xml
from ..utils.to_attach_xml_message import generate_attach_xml_to_single
_logger = logging.getLogger(__name__)


# 本地测试环境路径
# pre_ex_client 前置交换客户端路径
# PARSE_CUS_TO_WLY_PATH = config.options.get('parse_cus_to_wly_path','/mnt/odooshare/about_wly_xml_data/pre_ex_client/cus_to_wly')
# PARSE_CUS_TO_WLY_ATTACH_PATH = config.options.get('parse_cus_to_wly_attach_path','/mnt/odooshare/about_wly_xml_data/pre_ex_client/cus_to_wly_attach_send')
# PARSE_SEND_ERROR_XML_PATH = config.options.get('parse_send_error_xml_path','/mnt/odooshare/about_wly_xml_data/pre_ex_client/send_error_xml_message')
# GENERATE_REC_WLY_TO_XG_PATH = config.options.get('generate_rec_wly_to_cus_path', '/mnt/odooshare/about_wly_xml_data/pre_ex_client/rec_wly_to_cus')
# GENERATE_REC_WLY_TO_XG_ATTACH_PATH = config.options.get('generate_rec_wly_to_cus_attach_path', '/mnt/odooshare/about_wly_xml_data/pre_ex_client/rec_wly_to_cus_attach')
# BACKUP_SEND_XML_PATH = config.options.get('backup_send_xml_path', '/mnt/odooshare/about_wly_xml_data/pre_ex_client/send_backup_xml')   # 新光原始报文备份目录
# BACKUP_SEND_ATTACH_XML_PATH = config.options.get('backup_attach_send_xml_path', '/mnt/odooshare/about_wly_xml_data/pre_ex_client/send_backup_xml_attach')   # 新光原始报文备份目录
#
# # post_ex_client 后置交换客户端路径
# RECV_XML_BASE_PATH = config.options.get('parse_rec_ex_to_wly', '/mnt/odooshare/about_wly_xml_data/post_ex_client/rec_ex_to_wly')
# RECV_XML_ATTACH_BASE_PATH = config.options.get('parse_rec_ex_to_wly_attach', '/mnt/odooshare/about_wly_xml_data/post_ex_client/rec_ex_to_wly_attach')
# ERROR_XML_BASE_PATH = config.options.get('parse_rec_error_xml_path','/mnt/odooshare/about_wly_xml_data/post_ex_client/error_xml_message')
# BAKUP_XML_BASE_PATH = config.options.get('backup_rec_xml_path','/mnt/odooshare/about_wly_xml_data/post_ex_client/backup_rec_xml')



# # # 118测试环境路径
# # pre_ex_client 前置交换客户端路径
# PARSE_CUS_TO_WLY_PATH = config.options.get('parse_cus_to_wly_path','/home/odootest/about_wly_xml_data/pre_ex_client/cus_to_wly')
# PARSE_CUS_TO_WLY_ATTACH_PATH = config.options.get('parse_cus_to_wly_attach_path','/home/odootest/about_wly_xml_data/pre_ex_client/cus_to_wly_attach_send')
# PARSE_SEND_ERROR_XML_PATH = config.options.get('parse_send_error_xml_path','/home/odootest/about_wly_xml_data/pre_ex_client/send_error_xml_message')
# GENERATE_REC_WLY_TO_XG_PATH = config.options.get('generate_rec_wly_to_cus_path', '/home/odootest/about_wly_xml_data/pre_ex_client/rec_wly_to_cus')
# GENERATE_REC_WLY_TO_XG_ATTACH_PATH = config.options.get('generate_rec_wly_to_cus_attach_path', '/home/odootest/about_wly_xml_data/pre_ex_client/rec_wly_to_cus_attach')
# BACKUP_SEND_XML_PATH = config.options.get('backup_send_xml_path', '/home/odootest/about_wly_xml_data/pre_ex_client/send_backup_xml')   # 新光原始报文备份目录
# BACKUP_SEND_ATTACH_XML_PATH = config.options.get('backup_attach_send_xml_path', '/home/odootest/about_wly_xml_data/pre_ex_client/send_backup_xml_attach')   # 新光原始报文备份目录
#
# # post_ex_client 后置交换客户端路径
# RECV_XML_BASE_PATH = config.options.get('parse_rec_ex_to_wly', '/home/odootest/about_wly_xml_data/post_ex_client/rec_ex_to_wly')
# RECV_XML_ATTACH_BASE_PATH = config.options.get('parse_rec_ex_to_wly_attach', '/home/odootest/about_wly_xml_data/post_ex_client/rec_ex_to_wly_attach')
# ERROR_XML_BASE_PATH = config.options.get('parse_rec_error_xml_path','/home/odootest/about_wly_xml_data/post_ex_client/error_xml_message')
# BAKUP_XML_BASE_PATH = config.options.get('backup_rec_xml_path','/home/odootest/about_wly_xml_data/post_ex_client/backup_rec_xml')



# # 应用服务器 测试环境路径
# pre_ex_client 前置交换客户端路径
PARSE_CUS_TO_WLY_PATH = config.options.get('parse_cus_to_wly_path','/mnt/xml_data/about_wly_xml_data/pre_ex_client/cus_to_wly')
PARSE_CUS_TO_WLY_ATTACH_PATH = config.options.get('parse_cus_to_wly_attach_path','/mnt/xml_data/about_wly_xml_data/pre_ex_client/cus_to_wly_attach_send')
PARSE_SEND_ERROR_XML_PATH = config.options.get('parse_send_error_xml_path','/mnt/xml_data/about_wly_xml_data/pre_ex_client/send_error_xml_message')
GENERATE_REC_WLY_TO_XG_PATH = config.options.get('generate_rec_wly_to_cus_path', '/mnt/xml_data/about_wly_xml_data/pre_ex_client/rec_wly_to_cus')
GENERATE_REC_WLY_TO_XG_ATTACH_PATH = config.options.get('generate_rec_wly_to_cus_attach_path', '/mnt/xml_data/about_wly_xml_data/pre_ex_client/rec_wly_to_cus_attach')
BACKUP_SEND_XML_PATH = config.options.get('backup_send_xml_path', '/mnt/xml_data/about_wly_xml_data/pre_ex_client/send_backup_xml')   # 新光原始报文备份目录
BACKUP_SEND_ATTACH_XML_PATH = config.options.get('backup_attach_send_xml_path', '/mnt/xml_data/about_wly_xml_data/pre_ex_client/send_backup_xml_attach')   # 新光原始报文备份目录

# post_ex_client 后置交换客户端路径
RECV_XML_BASE_PATH = config.options.get('parse_rec_ex_to_wly', '/mnt/xml_data/about_wly_xml_data/post_ex_client/rec_ex_to_wly')
RECV_XML_ATTACH_BASE_PATH = config.options.get('parse_rec_ex_to_wly_attach', '/mnt/xml_data/about_wly_xml_data/post_ex_client/rec_ex_to_wly_attach')
ERROR_XML_BASE_PATH = config.options.get('parse_rec_error_xml_path','/mnt/xml_data/about_wly_xml_data/post_ex_client/error_xml_message')
BAKUP_XML_BASE_PATH = config.options.get('backup_rec_xml_path','/mnt/xml_data/about_wly_xml_data/post_ex_client/backup_rec_xml')





def check_and_mkdir(*path):
    for p in path:
        if not os.path.exists(p):
            os.mkdir(p)



class CustomsDeclaration(models.Model):
    """ 报关单 """
    _name = 'customs_center.customs_dec'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Customs Declaration'

    name = fields.Char(string="Name", copy=False)   # 报关单流水号   # copy=False 防止服务器动作复制报关单信息时复制
    client_seq_no = fields.Char(string="client seq No")  # 报关单客户端编号
    synergism_seq_no = fields.Char(string="Synergism seq No")  # 客户协同单号

    # 关联工作单
    work_sheet_id = fields.Many2one(comodel_name="work_sheet", string="Work Sheet")  # 工作单ID

    # 关联通关清单 多对一
    customs_order_id = fields.Many2one(comodel_name="customs_center.customs_order", string="customs Order")
    cus_ciq_No = fields.Char(string="cus Ciq No")  # 关检关联号
    custom_master_id = fields.Many2one(comodel_name="delegate_customs", string="Dec Custom")  # 申报口岸 / 申报地海关

    entry_type_id = fields.Many2one(comodel_name="basedata.cus_entry_type", string="Entry Type")  # 报关单类型 关联报关单类型字典表，待新增
    bill_type_id = fields.Many2one(comodel_name="basedata.cus_filing_bill_type", string="bill Type")    # 备案清单 待新建，备案清单类型表
    inout = fields.Selection(string="InOut", selection=[('I', u'进口'), ('E', u'出口'), ], track_visibility='always',)  # 进出口类型
    dec_seq_no = fields.Char(string="DecSeqNo")  # 统一编号
    pre_entry_id = fields.Char(string="PreEntryId")  # 预录入编号
    entry_id = fields.Char(string="EntryId")  # 海关编号
    ManualNo = fields.Char(string="Manual No", track_visibility='always',)  # 备案号
    customer_contract_no = fields.Char(string="Customer Contract No", track_visibility='onchange',)  # 合同协议号
    in_out_date = fields.Datetime(string="InoutDate")   # 进出口日期
    dec_date = fields.Datetime(string="DecDate")   # 申报日期
    customs_id = fields.Many2one(comodel_name="delegate_customs", string="Customs")  # 进出口岸

    transport_mode_id = fields.Many2one(comodel_name="delegate_transport_mode",
                                        string="Transport Mode")  # 运输方式
    NativeShipName = fields.Char(string="Native Ship Name")  # 运输工具名称
    VoyageNo = fields.Char(string="Voyage No")           # 航次号

    bill_no = fields.Char(string="Bill No")           # 提运单号
    trade_mode_id = fields.Many2one(comodel_name="delegate_trade_mode", string="Trade Mode")  # 监管方式
    CutMode_id = fields.Many2one(comodel_name="basedata.cus_cut_mode", string="CutMode id")  # 征免性质   征免性质表待新建
    in_ratio = fields.Integer(string="In ratio")  # 征免比例
    licenseNo = fields.Char(string="Bill No")  # 许可证号
    licenseNo_ids = fields.One2many(comodel_name="customs_center.dec_lic_doc",
                                inverse_name="customs_declaration_id", string="License No")  # 许可证号    一对多 关联随附单证模型

    origin_arrival_country_id = fields.Many2one(comodel_name="delegate_country",
                                                string="Origin Arrival Country")  # 启运/抵达国
    port_id = fields.Many2one(comodel_name="delegate_port", string="Port", )  # 装货/指运港
    region_id = fields.Many2one(comodel_name="delegate_region", string="Region")  # 境内目的/货源地
    trade_terms_id = fields.Many2one(comodel_name="delegate_trade_terms", string="Trade Term")  # 成交方式 or 贸易条款


    # payment_mark = fields.Selection(string="payment mark", selection=[('1', u'经营单位'),
    #                                                     ('2', u'收货单位'),
    #                                                     ('3', u'申报单位')], )  # 纳税单位

    # 关联 纳税单位标识类型 替换 上边注释
    payment_mark = fields.Many2one(comodel_name="customs_center.pay_mark_type", string="payment mark")   # 纳税单位

    # fee_mark = fields.Selection(string="FeeMark", selection=[('1', u'1-率'),
    #                                                     ('2', u'2-单价'),
    #                                                     ('3', u'3-总价')], )  # 运费标记
    # insurance_mark = fields.Selection(string="InsurMark", selection=[('1', '1-率'),
    #                                                     ('3', '3-总价')], )  # 保险费标记
    # other_mark = fields.Selection(string="OtherMark", selection=[('1', u'1-率'),
    #                                                     ('3', u'3-总价')], )  # 杂费标记

    # 关联 费用标识类型 替换 上边注释
    fee_mark = fields.Many2one(comodel_name="customs_center.exp_mark_type", string="FeeMark")  # 运费标记
    insurance_mark = fields.Many2one(comodel_name="customs_center.exp_mark_type", string="insurance_mark") # 保险费标记
    other_mark = fields.Many2one(comodel_name="customs_center.exp_mark_type", string="other_mark") # 杂费标记

    # promise1 = fields.Selection(string="promise1", selection=[('0', u'0-否'),
    #                                                     ('1', u'1-是'),
    #                                                     ('9', u'9-空')], )  # 特殊关系确认
    # promise2 = fields.Selection(string="promise2", selection=[('0', u'0-否'),
    #                                                     ('1', u'1-是'),
    #                                                     ('9', u'9-空')], )  # 价格影响确认
    # promise3 = fields.Selection(string="promise3", selection=[('0', u'0-否'),
    #                                                     ('1', u'1-是'),
    #                                                     ('9', u'9-空')], )  # 支付特许权使用费确认

    # 关联 是否标识类型 替换 上边注释
    promise1 = fields.Many2one(comodel_name="customs_center.whet_mark_type", string="promise1") # 特殊关系确认
    promise2 = fields.Many2one(comodel_name="customs_center.whet_mark_type", string="promise2") # 价格影响确认
    promise3 = fields.Many2one(comodel_name="customs_center.whet_mark_type", string="promise3") # 支付特许权使用费确认

    fee_rate = fields.Float(string="FeeRate", digits=dp.get_precision('Product Price'),)  # 运费/率
    fee_currency_id = fields.Many2one(comodel_name="basedata.cus_currency", string="FeeCurrency")  # 运费币制

    insurance_rate = fields.Float(string="InsurRate", digits=dp.get_precision('Product Price'),)  # 保险费/率
    insurance_currency_id = fields.Many2one(comodel_name="basedata.cus_currency", string="InsurCurrency_id")  # 保险费币制

    other_rate = fields.Float(string="OtherRate", digits=dp.get_precision('Product Price'),)  # 杂费/率
    other_currency_id = fields.Many2one(comodel_name="basedata.cus_currency", string="OtherCurrency_id")  # 杂费币制

    qty = fields.Integer(string="Qty")  # 件数
    gross_weight = fields.Float(string="Gross Weight")  # 毛重
    net_weight = fields.Float(string="Net Weight")  # 净重
    remarks = fields.Text(string="Marks")  # 备注
    packing_id = fields.Many2one(comodel_name="delegate_packing", string="Package Type")  # 包装种类、方式
    trade_country_id = fields.Many2one(comodel_name="delegate_country",
                                       string="Trade Country")  # 贸易国别


    # 报关单关联信息
    rel_dec_No = fields.Char(string="RelDec No")  # 关联报关单
    rel_man_No = fields.Char(string="License No")  # 关联 备案
    bonded_No = fields.Char(string="Bonded No")  # 监管场所
    customs_field = fields.Char(string="CustomsField")  # 货场代码

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")  # 客户

    # # 集成通3.0 XML报文相关字段
    # agent_code = fields.Char(string="Agent Code", required=True, )  # 申报单位代码
    # cop_code = fields.Char(string="Cop Code", required=True, )      # 录入单位代码
    # cop_name = fields.Char(string="Cop Name", required=True, )      # 录入单位名称
    # custom_master = fields.Char(string="Custom Master", required=True, )  # 申报地海关代码

    declare_company_id = fields.Many2one(comodel_name="basedata.cus_register_company", string="declare company name")  # 申报单位 新建企业库表
    input_company_id = fields.Many2one(comodel_name="basedata.cus_register_company", string="input company id")  # 货主单位 消费使用单位 新建企业库表
    business_company_id = fields.Many2one(comodel_name="basedata.cus_register_company", string="business company name")    # 收发货人 新建企业库表

    @api.onchange('business_company_id')
    def _compute_input_company(self):
        """根据当前选中的收发货人 改变 消费使用单位"""
        for customs_dec in self:
            if customs_dec.business_company_id != 0:
                customs_dec.input_company_id = customs_dec.business_company_id

    cop_code = fields.Char(string="cop code")  # 录入单位企业组织机构代码
    cop_name = fields.Char(string="cop name")  # 录入单位企业名称
    # dec_company = fields.Char(string="dec company name")  # 申报单位企业名称

    # 模糊查询 从当前登录的用户所在的公司 模糊匹配海关企业表中的公司
    dec_company = fields.Many2one(comodel_name="basedata.cus_register_company", string="dec company name",
                                  default = lambda self: self.env['basedata.cus_register_company'].search([('register_name_cn', 'like', self.env.user.company_id.name[:4]+'%')])[0]) # 申报单位企业名称
    cop_code_scc = fields.Char(string="cop Social credit uniform coding")  # 录入单位社会信用统一编码
    inputer_name = fields.Char(string="inputer name")  # 录入员姓名
    oper_name = fields.Char(string="oper name")     # 操作员姓名
    certificate = fields.Char(string="oper card certificate")   # 操作员卡的证书号
    ic_code = fields.Char(string="IC number")  # 操作员IC卡号/录入员IC卡号
    # cus_dec_dir = fields.Char(string="customs dec path")  # 企业报文服务器存放路径
    dec_company_customs_code = fields.Char(string="declare company path")  # 申报单位海关编号/ 报文存放路径

    # cop_code_scc = fields.Char(string="cop Social credit uniform coding")  # 录入单位社会信用统一编码
    # owner_code_scc = fields.Char(string="owner Social credit uniform coding")   # 货主单位/生产消费单位 社会信用统一编码
    # trade_code_scc = fields.Char(string="owner Social credit uniform coding")   # 经营单位 / 收发货人 统一编码

    decl_trn_rel = fields.Selection(string="DeclTrnRel", selection=[('0', u'一般报关单'), ('1', u'转关提前报关单')])   # 报关/转关关系标志
    ediId = fields.Selection(string="ediId", selection=[('1', u'普通报关'), ('3', u'北方转关提前'),
                                                        ('5', u'南方转关提前'), ('6', u'普通报关')], )  # 报关标志
    # trade_code = fields.Char(string="Trade Code", required=True, )  # 经营单位编号

    # 关联报关单商品列表 1对多关系
    # dec_goods_list_ids = fields.One2many(comodel_name="customs_center.dec_goods_list",
    #                                     inverse_name="customs_declaration_id", string="dec goods name")
    # 通关清单 和报关单共用一张商品表的时候 下方的写法
    dec_goods_list_ids = fields.One2many(comodel_name="customs_center.cus_goods_list",
                                         inverse_name="customs_declaration_id", string="dec goods name")
    # 报关单 关联合规模型 一对多 冗余字段 用于修改历史商品列表 通过关联报关单 确认是否已归类
    dec_goods_classified_ids = fields.One2many(comodel_name="customs_center.goods_classify",
                                         inverse_name="customs_declaration_id", string="goods classified")

    # 集装箱信息 报关单 关联集装箱模型 一对多
    dec_container_ids = fields.One2many(comodel_name="customs_center.dec_container",
                                         inverse_name="customs_declaration_id", string="container info")

    customs_declaration_state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], default='draft')  # 报关单状态
    # 回执状态
    receipt_ids = fields.One2many(comodel_name="customs_center.dec_result", inverse_name="customs_declaration_id",
                                  string="Recipts", required=False, )

    cus_dec_sent_state = fields.Selection(string="Sent State", selection=[('draft', 'Draft'),
                                                                      ('succeed', 'Success'),
                                                                      ('cancel', 'Cancel'),
                                                                      ('failure', 'Failure')],default='draft')  # 报关单发送状态
    cus_dec_rec_state = fields.Char(string="dec receive status")  # 报关单回执状态

    cus_dec_sent_way = fields.Selection(string="Sent way", selection=[('single', 'single windows'),('QP', 'quick pass')])  # 报关单发送通道选择

    # 附件拖拽上传
    information_attachment_ids = fields.Many2many('ir.attachment')


    #####################################################################################################
    # 报关单关联的附件 该字段生成报文发送单一窗口QP的时候需要   继承原附件模型写法
    # information_attachment_ids = fields.Many2many('ir.attachment', compute='_get_attachment_ids', string='attach')
    # @api.multi
    # def _get_attachment_ids(self):
    #     att_model = self.env['ir.attachment']  # 获取附件模型
    #     for obj in self:
    #         query = [('res_model', '=', 'customs_center.customs_dec'), ('res_id', '=', obj.id)]  # 根据res_model和res_id查询附件
    #         obj.information_attachment_ids = att_model.search(query)  # 取得附件list

    ###############################################################################################################
    # 随附单据上传功能   继承原附件模型写法
    # attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')
    # @api.multi
    # def _compute_attachment_number(self):
    #     """附件上传 计算附件数量"""
    #     attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'customs_center.customs_dec'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
    #     attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
    #     for expense in self:
    #         expense.attachment_number = attachment.get(expense.id, 0)

    @api.multi
    def action_get_dec_attachment_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('customs_center', 'dec_action_attachment')
        res['domain'] = [('res_model', '=', 'customs_center.customs_dec'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'customs_center.customs_dec', 'default_res_id': self.id}
        return res
    #############################################################################################

    # 服务器动作 复制当前报关单全部数据
    @api.multi
    def duplicate_current_all_data(self):
        """ 复制当前报关单全部数据 """
        self.ensure_one()
        customs_declaration_obj_copy = self.copy()
        # cus_goods_list_ids_list = []
        for line in self:
            if line.dec_goods_list_ids:
                cus_goods_list_ids_list = [goods.copy().id for goods in line.dec_goods_list_ids]
                customs_declaration_obj_copy.dec_goods_list_ids |= self.env['customs_center.cus_goods_list'].search([('id', 'in', cus_goods_list_ids_list)])
        if customs_declaration_obj_copy:
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'customs_center.customs_dec',
                'res_id': customs_declaration_obj_copy.id,
                'context': self.env.context,
                'flags': {'initial_mode': 'edit'},
            }

        # 自己实现方式2
        # ref_id = self._context.get('active_id')
        # customs_declaration_obj = self.env['customs_center.customs_dec'].browse(ref_id).copy()
        #
        # cus_goods_list_ids_list = []
        # for line in self:
        #     if line.dec_goods_list_ids:
        #         cus_goods_list_ids_list = [goods.copy().id for goods in line.dec_goods_list_ids]
        # customs_declaration_obj.dec_goods_list_ids |= self.env['customs_center.cus_goods_list'].search([('id', 'in', cus_goods_list_ids_list)])
        #
        # return {
        #     'name': "Customs Center Clearance",
        #     'type': "ir.actions.act_window",
        #     'view_type': 'form',
        #     'view_mode': 'form, tree',
        #     'res_model': 'customs_center.customs_dec',
        #     'views': [[False, 'form']],
        #     'res_id': customs_declaration_obj.id,
        #     'target': 'current',
        #     'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}}
        #     # 'target': 'main'
        # }



    ##############################################################################################
    # 报关单列表视图 回执状态 查看历史回执按钮
    @api.multi
    def btn_review_receipt(self):
        """ 查看历史回执按钮 """
        # for line in self:
        #     cus_goods_list_ids = []
        #     if line.cus_goods_list_ids:
        #         cus_goods_list_ids = [goods.copy().id for goods in line.cus_goods_list_ids]

        return {
            'name': u"回执历史状态",
            'type': "ir.actions.act_window",
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'customs_center.dec_result',
            'views': [[False, 'tree']],
            'res_id': self.ids,
            "domain": [["customs_declaration_id", "=", self.id]],
            'target': 'new'
        }

    @api.model
    def create(self, vals):
        """设置报关单命名规则"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('code_customs_declaration') or _('New')
            # vals['client_seq_no'] = str(uuid.uuid1())
            # 生成报关单的时候 如果客户协同单号存在 那么客户端编号唯一ID就用客户的 如果没有就用物流云自己生成的
            if vals.get('synergism_seq_no'):
                vals['client_seq_no'] = vals.get('synergism_seq_no')
            else:
                vals['client_seq_no'] = str((datetime.now()+timedelta(hours=8)).strftime('%y%m%d%H%M%S%f'))
        result = super(CustomsDeclaration, self).create(vals)

        return result


    # @api.model
    # @q_job.job
    @api.multi
    def parse_cus_message_xml(self):
        """解析报文 + 空随附单据入库"""
        # company_xml_parse_path = '0000016165'  # 做成前端界面可配置
        # company_xml_parse_path = self.dec_company_customs_code  # 获取配置信息中的 申报单位海关编码 作为解析路径

        customs_dec_model_dic = self.env['customs_center.customs_dec'].default_get(['dec_company_customs_code']) # 获取报关单模型对象
        company_xml_parse_path = customs_dec_model_dic.get('dec_company_customs_code')  # 获取配置信息中的 申报单位海关编码 作为解析路径

        # print("**************************77777777777777***********************")
        # print(company_xml_parse_path)
        parse_xml_path = os.path.join(PARSE_CUS_TO_WLY_PATH, company_xml_parse_path.encode('utf-8'))  # 原始报文解析目录
        parse_attach_path = os.path.join(PARSE_CUS_TO_WLY_ATTACH_PATH,
                                         company_xml_parse_path.encode('utf-8'))  # 随附单据解析目录
        parse_error_xml_path = os.path.join(PARSE_SEND_ERROR_XML_PATH, company_xml_parse_path.encode('utf-8'))
        backup_xml_path = os.path.join(BACKUP_SEND_XML_PATH, company_xml_parse_path.encode('utf-8'))  # 原始报文备份目录
        backup_attach_xml_path = os.path.join(BACKUP_SEND_ATTACH_XML_PATH, company_xml_parse_path.encode('utf-8'))  # 随附单据报文备份目录

        # 检查并生成相应的目录
        check_and_mkdir(parse_xml_path, parse_attach_path, parse_error_xml_path, backup_xml_path, backup_attach_xml_path)

        files = os.listdir(parse_xml_path)
        files = [filename for filename in files if filename.endswith('.xml')]
        if not files:
            return True
        files = [os.path.join(parse_xml_path, i) for i in files]

        # 读文件，用lxml解析报文
        for xml_message in files:

            with open(xml_message, 'r') as f:
                xml_str = str(f.read())
                xml_str = xml_str.replace('xmlns="http://www.chinaport.gov.cn/dec"', '')
                root = etree.fromstring(xml_str)  # 打开xml文档

                customs_dec_dic = {}
                root_name = etree.QName(root).localname
                print(root_name)  # DecMessage
                if root_name == u'DecMessage':
                    head_node = root.find('DecHead')
                    body_list = root.find('DecLists')
                    body_containers_list = root.find('DecContainers')
                    body_license_docus_list = root.find('DecLicenseDocus')
                    body_free_test_list = root.find('DecFreeTxt')
                    body_dec_sign = root.find('DecSign')
                    trn_head_info = root.find('TrnHead')
                    trn_list_info = root.find('TrnList')
                    trn_containers_info = root.find('TrnContainers')
                    trn_conta_goods_list = root.find('TrnContaGoodsList')
                    e_doc_realation_info = root.findall('EdocRealation')  # 随附单据标签

                    customs_dec_dic['DecHead'] = {}
                    if head_node:
                        for child in head_node:
                            if child.text:
                                customs_dec_dic['DecHead'][child.tag] = child.text
                    # 报文中的商品列表
                    customs_dec_dic['DecLists'] = {}
                    d_list = 0
                    for child in body_list:
                        customs_dec_dic['DecLists'][d_list] = {}
                        for child_son in child:
                            if child_son.text:
                                customs_dec_dic['DecLists'][d_list][child_son.tag] = child_son.text
                        d_list += 1
                    dec_goods_list_dic = customs_dec_dic['DecLists']

                    customs_dec_dic['DecContainers'] = {}
                    if body_containers_list:
                        for child in body_containers_list:
                            if child.text:
                                customs_dec_dic['DecContainers'][child.tag] = child.text

                    customs_dec_dic['DecLicenseDocus'] = {}
                    if body_license_docus_list:
                        for child in body_license_docus_list:
                            if child.text:
                                customs_dec_dic['DecLicenseDocus'][child.tag] = child.text

                    customs_dec_dic['DecFreeTxt'] = {}
                    if body_free_test_list:
                        for child in body_free_test_list:
                            if child.text:
                                customs_dec_dic['DecFreeTxt'][child.tag] = child.text

                    customs_dec_dic['DecFreeTxt'] = {}
                    if body_free_test_list:
                        for child in body_free_test_list:
                            if child.text:
                                customs_dec_dic['DecFreeTxt'][child.tag] = child.text

                    customs_dec_dic['DecSign'] = {}
                    if body_dec_sign:
                        for child in body_dec_sign:
                            if child.text:
                                customs_dec_dic['DecSign'][child.tag] = child.text

                    customs_dec_dic['TrnHead'] = {}
                    if trn_head_info:
                        for child in trn_head_info:
                            if child.text:
                                customs_dec_dic['TrnHead'][child.tag] = child.text

                    customs_dec_dic['TrnList'] = {}
                    if trn_list_info:
                        for child in trn_list_info:
                            if child.text:
                                customs_dec_dic['TrnList'][child.tag] = child.text

                    customs_dec_dic['TrnContainers'] = {}
                    if trn_containers_info:
                        for child in trn_containers_info:
                            if child.text:
                                customs_dec_dic['TrnContainers'][child.tag] = child.text

                    customs_dec_dic['TrnContaGoodsList'] = {}
                    if trn_conta_goods_list:
                        for child in trn_conta_goods_list:
                            if child.text:
                                customs_dec_dic['TrnContaGoodsList'][child.tag] = child.text

                    # 随附单据
                    customs_dec_dic['EdocRealation'] = {}
                    if e_doc_realation_info:
                        d_list = 0
                        for child in e_doc_realation_info:
                            customs_dec_dic['EdocRealation'][d_list] = {}
                            for child_son in child:
                                if child_son.text:
                                    customs_dec_dic['EdocRealation'][d_list][child_son.tag] = child_son.text
                            d_list += 1
                    attach_list_dic = customs_dec_dic['EdocRealation']   # # 随附单据字典
                else:
                    _logger.error(u'Find error format xml message: %s' % xml_message.decode('utf-8'))
                    shutil.move(xml_message, parse_error_xml_path)
                    continue

            if customs_dec_dic:
                client_seq_no = customs_dec_dic['DecSign'].get('ClientSeqNo', None)  # 报关单客户端编号
                inout = customs_dec_dic['DecHead'].get('IEFlag', None)  # u'进出口标志'

                custom_master_code = customs_dec_dic['DecHead'].get('CustomMaster', None)  # u'申报地海关'
                custom_master_id = self.env['delegate_customs'].search([('Code', '=', custom_master_code)])

                dec_seq_no = customs_dec_dic['DecHead'].get('AgentCodeScc', None)  # u'统一编号'  申报单位统一编码
                pre_entry_id = customs_dec_dic['DecHead'].get('PreEntryId', None)  # u'预录入编号'

                # customs_code = customs_dec_dic.get('DecHead')['IEPort']  # u'进出口岸'
                customs_code = customs_dec_dic['DecHead'].get('IEPort', None)  # u'进出口岸'
                customs_id = self.env['delegate_customs'].search([('Code', '=', customs_code)])

                ManualNo = customs_dec_dic['DecHead'].get('ManualNo', None)  # u'备案号'
                customer_contract_no = customs_dec_dic['DecHead'].get('ContrNo', None)  # u'合同编号'

                in_out_date = customs_dec_dic['DecHead'].get('IEDate', None)  # u'进出口日期'

                business_company_register_code = customs_dec_dic['DecHead'].get('TradeCode', None)  # 收发货人
                business_company_id = self.env['basedata.cus_register_company'].search(
                    [('register_code', '=', business_company_register_code)])

                input_company_unified_code = customs_dec_dic['DecHead'].get('OwnerCodeScc', None)  # 消费使用单位 货主单位
                input_company_id = self.env['basedata.cus_register_company'].search(
                    [('unified_social_credit_code', '=', input_company_unified_code)])

                # declare_company_register_code = customs_dec_dic['DecHead'].get('AgentCode', None)  # 申报单位
                # declare_company_id = self.env['basedata.cus_register_company'].search(
                #     [('register_code', '=', declare_company_register_code)])

                transport_mode_code = customs_dec_dic['DecHead'].get('TrafMode', None)  # u'运输方式'
                transport_mode_id = self.env['delegate_transport_mode'].search([('code', '=', transport_mode_code)])

                NativeShipName = customs_dec_dic['DecHead'].get('TrafName', None)  # u'运输工具名称'
                VoyageNo = customs_dec_dic['TrnList'].get('VoyageNo', None)  # u'航次号'
                bill_no = customs_dec_dic['DecHead'].get('BillNo', None)  # u'提运单号'

                trade_mode_code = customs_dec_dic['DecHead'].get('TradeMode', None)  # u'监管方式'
                trade_mode_id = self.env['delegate_trade_mode'].search([('Code', '=', trade_mode_code)])

                CutMode_code = customs_dec_dic['DecHead'].get('CutMode', None)  # u'征免性质'
                CutMode_id = self.env['basedata.cus_cut_mode'].search([('Code', '=', CutMode_code)])

                payment_mark_code = customs_dec_dic['DecHead'].get('PaymentMark', None)  # u'纳税单位'
                payment_mark = self.env['customs_center.pay_mark_type'].search([('Code', '=', payment_mark_code)])

                licenseNo = customs_dec_dic['DecHead'].get('LicenseNo', None)  # u'许可证编号'

                origin_arrival_country_code = customs_dec_dic['DecHead'].get('TradeCountry', None)  # u'启运国/抵达国'
                origin_arrival_country_id = self.env['delegate_country'].search(
                    [('Code', '=', origin_arrival_country_code)])

                port_code = customs_dec_dic['DecHead'].get('DistinatePort', None)  # u'装货/指运港'
                port_id = self.env['delegate_port'].search([('Code', '=', port_code)])

                region_code = customs_dec_dic['DecHead'].get('DistrictCode', None)  # u'境内目的/货源地'
                region_id = self.env['delegate_region'].search([('Code', '=', region_code)])

                trade_terms_code = customs_dec_dic['DecHead'].get('TransMode', None)  # u'成交方式 or 贸易条款'
                trade_terms_id = self.env['delegate_trade_terms'].search([('Code', '=', trade_terms_code)])

                fee_mark_code = customs_dec_dic['DecHead'].get('FeeMark', None)  # u'运费标记'
                fee_mark = self.env['customs_center.exp_mark_type'].search([('Code', '=', fee_mark_code)])
                fee_rate = customs_dec_dic['DecHead'].get('FeeRate', None)  # u'运费／率'

                fee_currency_code = customs_dec_dic['DecHead'].get('FeeCurr', None)  # u'运费币制'
                fee_currency_id = self.env['basedata.cus_currency'].search([('Code', '=', fee_currency_code)])

                insurance_mark_code = customs_dec_dic['DecHead'].get('InsurMark', None)  # u'保险费标记'
                insurance_mark = self.env['customs_center.exp_mark_type'].search([('Code', '=', insurance_mark_code)])
                insurance_rate = customs_dec_dic['DecHead'].get('InsurRate', None)  # u'保险费／率'

                insurance_currency_code = customs_dec_dic['DecHead'].get('InsurCurr', None)  # u'保险费币制'
                insurance_currency_id = self.env['basedata.cus_currency'].search(
                    [('Code', '=', insurance_currency_code)])

                other_mark_code = customs_dec_dic['DecHead'].get('OtherMark', None)  # u'杂费标记'
                other_mark = self.env['customs_center.exp_mark_type'].search([('Code', '=', other_mark_code)])
                other_rate = customs_dec_dic['DecHead'].get('OtherRate', None)  # u'杂费／率'

                other_currency_code = customs_dec_dic['DecHead'].get('OtherCurr', None)  # u'杂费币制'
                other_currency_id = self.env['basedata.cus_currency'].search([('Code', '=', other_currency_code)])

                qty = customs_dec_dic['DecHead'].get('PackNo', None)  # u'件数'

                packing_code = customs_dec_dic['DecHead'].get('WrapType', None)  # u'包装种类'
                packing_id = self.env['delegate_packing'].search([('Code', '=', packing_code)])

                gross_weight = customs_dec_dic['DecHead'].get('GrossWet', None)  # u'毛重'
                net_weight = customs_dec_dic['DecHead'].get('NetWt', None)  # u'净重'

                trade_country_code = customs_dec_dic['DecHead'].get('TradeAreaCode', None)  # u'贸易国别'
                trade_country_id = self.env['delegate_country'].search([('Code', '=', trade_country_code)])

                in_ratio = customs_dec_dic['DecHead'].get('PayWay', None)  # u'征税比例' in_ratio  报文PayWay

                promise1_promise2_promise3_code = customs_dec_dic['DecHead'].get('PromiseItmes', None)  # u'承诺事项'  字符串拼接

                promise1_code = str(promise1_promise2_promise3_code)[0] if promise1_promise2_promise3_code else None
                promise2_code = str(promise1_promise2_promise3_code)[1] if promise1_promise2_promise3_code else None
                promise3_code = str(promise1_promise2_promise3_code)[2] if promise1_promise2_promise3_code else None
                promise1 = self.env['customs_center.whet_mark_type'].search([('Code', '=', promise1_code)])  # 特殊关系确认
                promise2 = self.env['customs_center.whet_mark_type'].search([('Code', '=', promise2_code)])  # 价格影响确认
                promise3 = self.env['customs_center.whet_mark_type'].search(
                    [('Code', '=', promise3_code)])  # 支付特许权使用费确认

                entry_type_code = customs_dec_dic['DecHead'].get('EntryType', None)  # u'报关单类型'
                entry_type_id = self.env['basedata.cus_entry_type'].search([('Code', '=', entry_type_code)])

                remarks = customs_dec_dic['DecHead'].get('NoteS', None)  # u'备注'

                cop_code = customs_dec_dic['DecHead'].get('CopCode', None)  # u'录入单位企业组织机构代码'
                cop_name = customs_dec_dic['DecHead'].get('CopName', None)  # u'录入单位名称'
                cop_code_scc = customs_dec_dic['DecHead'].get('CopCodeScc', None)  # u'录入单位社会信用统一编码'
                inputer_name = customs_dec_dic['DecHead'].get('InputerName', None)  # u'录入员姓名'
                oper_name = customs_dec_dic['DecSign'].get('OperName', None)  # u'操作员姓名'
                certificate = customs_dec_dic['DecSign'].get('Certificate', None)  # u'操作员卡的证书号'
                ic_code = customs_dec_dic['DecHead'].get('TypistNo', None)  # u'操作员IC卡号/录入员IC卡号'

                customs_dec_dic = {
                    'synergism_seq_no': client_seq_no,  # 报关单客户端编号
                    'client_seq_no': client_seq_no,  # 报关单客户端编号
                    'inout': inout,  # u'进出口标志'
                    'custom_master_id': custom_master_id[0].id if len(custom_master_id) else None,  # 申报口岸 / 申报地海关
                    'dec_seq_no': dec_seq_no,  # u'统一编号'
                    'pre_entry_id': pre_entry_id,  # u'预录入编号'
                    'customs_id': customs_id[0].id if len(customs_id) else None,  # u'进出口岸'
                    'ManualNo': ManualNo,  # u'备案号'
                    'customer_contract_no': customer_contract_no,  # u'合同协议号'
                    'in_out_date': in_out_date,  # u'进出口日期'
                    'business_company_id': business_company_id[0].id if len(business_company_id) else None,  # 收发货人
                    'input_company_id': input_company_id[0].id if len(input_company_id) else None,  # 消费使用单位 货主单位
                    #'declare_company_id': declare_company_id[0].id if len(declare_company_id) else None,  # 申报单位
                    'transport_mode_id': transport_mode_id[0].id if len(transport_mode_id) else None,  # u'运输方式'
                    'NativeShipName': NativeShipName,  # u'运输工具名称'
                    'VoyageNo': VoyageNo,  # u'航次号'
                    'bill_no': bill_no,  # u'提运单号'
                    'trade_mode_id': trade_mode_id[0].id if len(trade_mode_id) else None,  # u'监管方式'
                    'CutMode_id': CutMode_id[0].id if len(CutMode_id) else None,  # u'征免性质'
                    'payment_mark': payment_mark[0].id if len(payment_mark) else None,  # 纳税单位 id
                    'licenseNo': licenseNo,  # u'许可证编号'
                    'origin_arrival_country_id': origin_arrival_country_id[0].id if len(
                        origin_arrival_country_id) else None,  # 启运国/抵达国
                    'port_id': port_id[0].id if len(port_id) else None,  # 装货/指运港 id
                    'region_id': region_id[0].id if len(region_id) else None,  # 境内目的/货源地 id
                    'trade_terms_id': trade_terms_id[0].id if len(trade_terms_id) else None,  # 成交方式 or 贸易条款 id
                    'fee_mark': fee_mark[0].id if len(fee_mark) else None,  # # 运费标记 id
                    'fee_rate': fee_rate,  # 运费/率
                    'fee_currency_id': fee_currency_id[0].id if len(fee_currency_id) else None,  # 运费币制
                    'insurance_mark': insurance_mark[0].id if len(insurance_mark) else None,  # 保险费标记
                    'insurance_rate': insurance_rate,  # 保险费/率
                    'insurance_currency_id': insurance_currency_id[0].id if len(insurance_currency_id) else None,
                # 保险费币制
                    'other_mark': other_mark[0].id if len(other_mark) else None,  # 杂费标记
                    'other_rate': other_rate,  # 杂费/率
                    'other_currency_id': other_currency_id[0].id if len(other_currency_id) else None,  # 杂费币制
                    'qty': qty,  # 件数
                    'packing_id': packing_id[0].id if len(packing_id) else None,  # 包装种类、方式 id
                    'gross_weight': gross_weight,  # 毛重
                    'net_weight': net_weight,  # 净重
                    'trade_country_id': trade_country_id[0].id if len(trade_country_id) else None,  # 贸易国别
                    'in_ratio': in_ratio,  # u'征税比例' in_ratio  报文PayWay
                    'promise1': promise1[0].id if len(promise1) else None,  # 特殊关系确认
                    'promise2': promise2[0].id if len(promise2) else None,  # 价格影响确认
                    'promise3': promise3[0].id if len(promise3) else None,  # 支付特许权使用费确认
                    'entry_type_id': entry_type_id[0].id if len(entry_type_id) else None,  # 报关单类型 关联报关单类型字典表
                    'remarks': remarks,  # 备注
                    'cop_code': cop_code,  # 录入单位企业组织机构代码
                    'cop_name': cop_name,  # 录入单位名称
                    'cop_code_scc': cop_code_scc,  # 录入单位社会信用统一编码
                    'inputer_name': inputer_name,  # 录入员姓名
                    'oper_name': oper_name,  # 操作员姓名
                    'certificate': certificate,  # 操作员卡的证书号
                    'ic_code': ic_code,  # 操作员IC卡号/录入员IC卡号
                }
                customs_dec_dic = {item: customs_dec_dic[item] for item in customs_dec_dic if customs_dec_dic[item]}
            else:
                _logger.error(u'Find error format xml message: %s' % xml_message.decode('utf-8'))
                shutil.move(xml_message, parse_error_xml_path)
                continue

            try:
                customs_declaration_obj = self.env['customs_center.customs_dec'].create(customs_dec_dic)
                # 创建报关单后 同时创建 空的 随附单据
                # 首先解析随附单据目录的文件  可能多个附件
                # attach_files = os.listdir(parse_attach_path)
                # attach_files_list = [attach_filename for attach_filename in attach_files if attach_filename.endswith('.xml')]
                #
                # if not attach_files_list:
                #     return True
                # attach_files = [os.path.join(parse_attach_path, i) for i in attach_files_list]

                # # 读文件，用lxml解析报文
                # xml_attach_message_list = []
                # for xml_attach_message in attach_files:
                #     with open(xml_attach_message, 'r') as f:
                #         attach_xml_str = str(f.read())
                #         attach_xml_str1 = attach_xml_str.replace('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"', '')
                #         attach_xml_str = attach_xml_str1.replace('xsi:nil="true"', '')
                #         # print xml_str
                #         root = etree.fromstring(attach_xml_str)  # 打开xml文档
                #
                #         root_name = etree.QName(root).localname
                #         print(root_name)  # Data
                #         xml_attach_message_dic = {}  # 随附单据报文中的数据
                #         if root_name == u'Data':
                #             attach_data_node = root.xpath('.//TcsData')
                #             for child in attach_data_node[0]:
                #                 xml_attach_message_dic[child.tag] = child.text
                #             xml_attach_message_list.append(xml_attach_message_dic)

                # 生成附件
                if attach_list_dic:  # 报关单中的随附单据数据 attach_list_dic
                    for keys, values_dic in attach_list_dic.items():
                        if values_dic:
                            genarate_attach_list_dic = {}
                            for k, values in values_dic.items():
                                if k == 'EdocID':
                                    attach_id = values  # u'随附单据编号'
                                    genarate_attach_list_dic['name'] = attach_id
                                    genarate_attach_list_dic['datas_fname'] = attach_id

                                    # # 查询和文件名匹配的二进制数据
                                    # if xml_attach_message_list:
                                    #     for attach_dic in xml_attach_message_list:
                                    #         if attach_dic.get('FILE_NAME') == attach_id:
                                    #             binary_data = attach_dic.get('BINARY_DATA', None)
                                    #             genarate_attach_list_dic['datas'] = binary_data
                                if k == 'EdocCode':
                                    edoc_code = values  # u'随附单据类别'
                                    # genarate_attach_list_dic['description'] = edoc_code # 原先第一次实现 用的附件模型字段自带的description字段 临时存放了
                                    # genarate_attach_list_dic['attach_type'] = edoc_code   # 第二种方案 关务中心附件上传 扩展了附件模型 增加单据类型字段attach_type
                                    genarate_attach_list_dic['dec_edoc_type'] = edoc_code   # 第三种方案 附件拖拽上传 扩展了附件字段

                            # 如果报关单对象为真 并且随附单据字典数据不为空 才会创建随附单据空附件
                            if customs_declaration_obj.id and genarate_attach_list_dic:
                                genarate_attach_list_dic['res_model'] = "customs_center.customs_dec"
                                genarate_attach_list_dic['res_id'] = customs_declaration_obj.id
                                genarate_attach_list_dic = {item: genarate_attach_list_dic[item] for item in
                                                            genarate_attach_list_dic if
                                                            genarate_attach_list_dic[item]}

                                new_attachment = self.env['ir.attachment'].create(genarate_attach_list_dic)

                                #if not attach_files_list or not new_attachment:
                                if not new_attachment:
                                    return True
                                # for xml_attach_message in attach_files_list:  # xml_attach_message是单据名
                                #     if xml_attach_message:
                                #         strlist = xml_attach_message.split('$')
                                #         filename = strlist[0]
                                #         if genarate_attach_list_dic.get('name' , None) == filename:  # 如果解析出的随附单据名 和 生成的随附单据名相同 就把报文移动到附件报文备份目录
                                #             # 这里 其实物流云不必放到备份目录再生成一遍随附单据报文 可以直接丢到 wly_to_ex_atach目录
                                #             xml_attach_message_path = os.path.join(parse_attach_path, xml_attach_message)
                                #             shutil.move(xml_attach_message_path, backup_attach_xml_path)
                                #             _logger.info(u'Had parsed the attach xml message %s' % xml_attach_message.decode('utf-8'))

                # 商品列表 字典
                # dec_goods_list_dic = customs_dec_dic['DecLists']
                if dec_goods_list_dic:
                    for keys, values_dic in dec_goods_list_dic.items():
                        if values_dic:
                            dec_goods_list = {}
                            for k, values in values_dic.items():
                                if k == 'CodeTS':
                                    cus_goods_tariff_code_ts = values  # u'商品编号'
                                    cus_goods_tariff_id = self.env['basedata.cus_goods_tariff'].search(
                                        [('Code_ts', '=', cus_goods_tariff_code_ts)])
                                    dec_goods_list['cus_goods_tariff_id'] = cus_goods_tariff_id[0].id if len(
                                        cus_goods_tariff_id) else None
                                elif k == 'GName':
                                    goods_name = values  # u'商品名称'
                                    dec_goods_list['goods_name'] = goods_name
                                elif k == 'GModel':
                                    goods_model = values  # u'商品规格、型号'
                                    dec_goods_list['goods_model'] = goods_model
                                elif k == 'GQty':
                                    deal_qty = values  # u'申报数量  成交数量'
                                    dec_goods_list['deal_qty'] = deal_qty
                                elif k == 'DeclPrice':
                                    deal_unit_price = values  # u'申报单价 成交单价'
                                    dec_goods_list['deal_unit_price'] = deal_unit_price
                                elif k == 'GUnit':
                                    deal_unit_code = values  # u'申报/成交计量单位'
                                    deal_unit_id = self.env['basedata.cus_unit'].search([('Code', '=', deal_unit_code)])
                                    dec_goods_list['deal_unit'] = deal_unit_id[0].id if len(deal_unit_id) else None
                                elif k == 'DeclTotal':
                                    deal_total_price = values  # u'申报总价 成交总价'
                                    dec_goods_list['deal_total_price'] = deal_total_price
                                elif k == 'TradeCurr':
                                    currency_code = values  # u'成交币制'
                                    currency_id = self.env['basedata.cus_currency'].search([('Code', '=', currency_code)])
                                    dec_goods_list['currency_id'] = currency_id[0].id if len(currency_id) else None
                                elif k == 'FirstQty':
                                    first_qty = values  # u'第一法定数量'
                                    dec_goods_list['first_qty'] = first_qty
                                elif k == 'FirstUnit':
                                    first_unit_code = values  # u'第一计量单位'
                                    first_unit_id = self.env['basedata.cus_unit'].search([('Code', '=', first_unit_code)])
                                    dec_goods_list['first_unit'] = first_unit_id[0].id if len(first_unit_id) else None
                                elif k == 'SecondQty':
                                    second_qty = values  # u'第二法定数量'
                                    dec_goods_list['second_qty'] = second_qty
                                elif k == 'SecondUnit':
                                    second_unit_code = values  # u'第二计量单位'
                                    second_unit_id = self.env['basedata.cus_unit'].search([('Code', '=', second_unit_code)])
                                    dec_goods_list['second_unit'] = second_unit_id[0].id if len(second_unit_id) else None
                                elif k == 'DutyMode':
                                    duty_mode_code = values  # u'征减免税方式'
                                    duty_mode_id = self.env['basedata.cus_duty_mode'].search(
                                        [('Code', '=', duty_mode_code)])
                                    dec_goods_list['duty_mode_id'] = duty_mode_id[0].id if len(duty_mode_id) else None
                                elif k == 'OriginCountry':
                                    origin_country_code = values  # u'原产地'
                                    origin_country_id = self.env['delegate_country'].search(
                                        [('Code', '=', origin_country_code)])
                                    dec_goods_list['origin_country_id'] = origin_country_id[0].id if len(
                                        origin_country_id) else None
                                elif k == 'DestinationCountry':
                                    destination_country_code = values  # u'最终目的国'
                                    destination_country_id = self.env['delegate_country'].search(
                                        [('Code', '=', destination_country_code)])
                                    dec_goods_list['destination_country_id'] = destination_country_id[0].id if len(
                                        destination_country_id) else None

                                # dec_goods_list = {item: dec_goods_list[item] for item in dec_goods_list if
                                #                   dec_goods_list[item]}

                            try:
                                customs_declaration_id = customs_declaration_obj.id
                                dec_goods_list['customs_declaration_id'] = customs_declaration_id
                                dec_goods_list = {item: dec_goods_list[item] for item in dec_goods_list if
                                                  dec_goods_list[item]}

                                cus_goods_list_obj = self.env['customs_center.cus_goods_list'].create(dec_goods_list)
                            except Exception, error_info:
                                _logger.error(
                                    u'{} {}'.format(xml_message.decode('utf-8'), str(error_info).decode('utf-8')))
                                shutil.move(xml_message, parse_error_xml_path)
                                continue
            except Exception, error_info:
                _logger.error(u'{} {}'.format(xml_message.decode('utf-8'), str(error_info).decode('utf-8')))
                shutil.move(xml_message, parse_error_xml_path)
                continue
            else:
                shutil.move(xml_message, backup_xml_path)
                _logger.info(u'Had parsed the xml message %s' % xml_message.decode('utf-8'))



    # @api.multi
    # # @api.model
    # # @q_job.job
    # def parse_attach_message_xml(self):
    #     """ 手动 解析随附单据入库 从报关单到随附单据报文 正向查找  可用 """
    #     company_xml_parse_path = '0000016165'  # 做成前端界面可配置
    #     parse_xml_path = os.path.join(PARSE_CUS_TO_WLY_PATH, company_xml_parse_path.encode('utf-8'))  # 新光原始报文解析目录
    #     parse_attach_path = os.path.join(PARSE_CUS_TO_WLY_ATTACH_PATH,
    #                                      company_xml_parse_path.encode('utf-8'))  # 新光随附单据解析目录
    #     parse_error_xml_path = os.path.join(PARSE_SEND_ERROR_XML_PATH, company_xml_parse_path.encode('utf-8'))
    #     backup_xml_path = os.path.join(BACKUP_SEND_XML_PATH, company_xml_parse_path.encode('utf-8'))  # 新光原始报文备份目录
    #     backup_attach_xml_path = os.path.join(BACKUP_SEND_ATTACH_XML_PATH,
    #                                           company_xml_parse_path.encode('utf-8'))  # 新光随附单据报文备份目录
    #
    #     # 检查并生成相应的目录
    #     check_and_mkdir(parse_xml_path, parse_attach_path, parse_error_xml_path, backup_xml_path,
    #                     backup_attach_xml_path)
    #
    #     # 首先解析随附单据目录的文件  可能多个附件
    #     attach_files = os.listdir(parse_attach_path)
    #     attach_files_list = [attach_filename for attach_filename in attach_files if attach_filename.endswith('.xml')]
    #
    #     if not attach_files_list:
    #         return True
    #     attach_files = [os.path.join(parse_attach_path, i) for i in attach_files_list]
    #
    #     # 读文件，用lxml解析报文
    #     xml_attach_message_list = []
    #     attach_name_list = []
    #     for xml_attach_message in attach_files:
    #         with open(xml_attach_message, 'r') as f:
    #             attach_xml_str = str(f.read())
    #             attach_xml_str1 = attach_xml_str.replace('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"', '')
    #             attach_xml_str = attach_xml_str1.replace('xsi:nil="true"', '')
    #             # print xml_str
    #             root = etree.fromstring(attach_xml_str)  # 打开xml文档
    #
    #             root_name = etree.QName(root).localname
    #             print(root_name)  # 根标签 Data
    #             xml_attach_message_dic = {}  # 随附单据报文中的数据  即将xml随附单据TcsData标签部分 转换为字典形式
    #             if root_name == u'Data':
    #                 attach_data_node = root.xpath('.//TcsData')
    #                 for child in attach_data_node[0]:
    #                     xml_attach_message_dic[child.tag] = child.text
    #                 xml_attach_message_list.append(xml_attach_message_dic)
    #
    #             genarate_attach_list_dic = {}
    #             for obj in self:
    #                 # 获取附件模型 根据res_model和res_id查询附件
    #                 information_attachment_ids = self.env['ir.attachment'].search([('res_model', '=', 'customs_center.customs_dec'),('res_id', '=', obj.id)])  # 取得附件list
    #                 print(information_attachment_ids)    # ir.attachment(2738, 2737, 2736, 2735)
    #                 for i in information_attachment_ids:
    #                     attach_name = i.name
    #                     attach_id = i.id
    #                     attach_name_list.append(attach_name)
    #                     if xml_attach_message_list:
    #                         for attach_dic in xml_attach_message_list:    # 这里循环出的每一个attach_dic 相当于上边的 xml_attach_message_dic
    #                             if attach_dic.get('FILE_NAME') == attach_name:
    #                                 binary_data = attach_dic.get('BINARY_DATA', None)
    #                                 genarate_attach_list_dic['datas'] = binary_data
    #                                 genarate_attach_list_dic['res_id'] = attach_id
    #                                 if genarate_attach_list_dic:
    #                                     new_attachment = self.env['ir.attachment'].search([('res_model', '=', 'customs_center.customs_dec'),('res_id', '=',obj.id),('name', '=',attach_name)]).update({'datas': binary_data})
    #
    #     # 将解析成功的随附单据报文 移动到随附单据备份目录
    #     for xml_attach_message in attach_files_list:  # xml_attach_message是单据名
    #         if xml_attach_message:
    #             strlist = xml_attach_message.split('$')
    #             filename = strlist[0]
    #             if filename in attach_name_list:
    #                 xml_attach_message_path = os.path.join(parse_attach_path, xml_attach_message)
    #                 shutil.move(xml_attach_message_path, backup_attach_xml_path)
    #                 _logger.info(
    #                     u'Had parsed the attach xml message %s' % xml_attach_message.decode('utf-8'))


    # @api.model
    # @q_job.job
    @api.multi
    def auto_parse_attach_message_xml(self):
        """ 自动 解析随附单据入库 从随附单据报文到报关单 反向查找"""
        # company_xml_parse_path = '0000016165'  # 做成前端界面可配置
        customs_dec_model_dic = self.env['customs_center.customs_dec'].default_get(
            ['dec_company_customs_code'])  # 获取报关单模型对象
        company_xml_parse_path = customs_dec_model_dic.get(
            'dec_company_customs_code')  # 获取配置信息中的 申报单位海关编码 作为解析路径

        parse_xml_path = os.path.join(PARSE_CUS_TO_WLY_PATH, company_xml_parse_path.encode('utf-8'))  # 新光原始报文解析目录
        parse_attach_path = os.path.join(PARSE_CUS_TO_WLY_ATTACH_PATH,
                                         company_xml_parse_path.encode('utf-8'))  # 新光随附单据解析目录
        parse_error_xml_path = os.path.join(PARSE_SEND_ERROR_XML_PATH, company_xml_parse_path.encode('utf-8'))
        backup_xml_path = os.path.join(BACKUP_SEND_XML_PATH, company_xml_parse_path.encode('utf-8'))  # 新光原始报文备份目录
        backup_attach_xml_path = os.path.join(BACKUP_SEND_ATTACH_XML_PATH,
                                              company_xml_parse_path.encode('utf-8'))  # 新光随附单据报文备份目录

        # 检查并生成相应的目录
        check_and_mkdir(parse_xml_path, parse_attach_path, parse_error_xml_path, backup_xml_path,
                        backup_attach_xml_path)

        # 首先解析随附单据目录的文件 可能多个附件
        attach_files = os.listdir(parse_attach_path)
        attach_files_list = [attach_filename for attach_filename in attach_files if attach_filename.endswith('.xml')]

        if not attach_files_list:
            return True
        attach_files = [os.path.join(parse_attach_path, i) for i in attach_files_list]

        # 读文件，用lxml解析报文
        attach_name_list = []
        for xml_attach_message in attach_files:
            with open(xml_attach_message, 'r') as f:
                attach_xml_str = str(f.read())
                attach_xml_str1 = attach_xml_str.replace('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"', '')
                attach_xml_str = attach_xml_str1.replace('xsi:nil="true"', '')
                # print xml_str
                root = etree.fromstring(attach_xml_str)  # 打开xml文档

                root_name = etree.QName(root).localname
                print(root_name)  # 根标签 Data
                xml_attach_message_dic = {}  # 随附单据报文中的数据  即将xml随附单据TcsData标签部分 转换为字典形式
                if root_name == u'Data':
                    attach_data_node = root.xpath('.//TcsData')
                    for child in attach_data_node[0]:
                        xml_attach_message_dic[child.tag] = child.text
                attach_name_in_xml = xml_attach_message_dic.get('FILE_NAME')  # 获取随附单据报文中的文件名
                binary_data = xml_attach_message_dic.get('BINARY_DATA', None) # 获取随附单据报文中的二进制数据

                # 根据上述获取的附件名称 在附件模型中查找 对应的附件ID
                attach_id = self.env['ir.attachment'].search([('res_model', '=', 'customs_center.customs_dec'),('name', '=', attach_name_in_xml)])
                print("*******************^^6666666665555555555555666666666666**********************")
                print(attach_id)
                # 根据附件ID 找到对应的报关单ID
                res_id = attach_id.res_id
                print("*******************^^66666666666666666666666666666666**********************")
                print(res_id)
                # 根据上方找到的报关单ID 找到该报关单对应的附件列表
                information_attachment_ids = self.env['ir.attachment'].search(
                    [('res_model', '=', 'customs_center.customs_dec'), ('res_id', '=', res_id)])  # 取得附件list
                print(information_attachment_ids)
                for i in information_attachment_ids:
                    attach_name = i.name
                    attach_name_list.append(attach_name)

                    if attach_name == attach_name_in_xml:
                        new_attachment = self.env['ir.attachment'].search(
                            [('res_model', '=', 'customs_center.customs_dec'), ('res_id', '=', res_id),
                             ('name', '=', attach_name)]).update({'datas': binary_data})

        # 将解析成功的随附单据报文 移动到随附单据备份目录
        for xml_attach_message in attach_files_list:  # xml_attach_message是单据名
            if xml_attach_message:
                strlist = xml_attach_message.split('$')
                filename = strlist[0]
                if filename in attach_name_list:
                    xml_attach_message_path = os.path.join(parse_attach_path, xml_attach_message)
                    shutil.move(xml_attach_message_path, backup_attach_xml_path)
                    _logger.info(
                        u'Had parsed the attach xml message %s' % xml_attach_message.decode('utf-8'))

    @api.multi
    def generate_single_customer_xml_after(self):
        """报文已发送至单一窗口"""
        pass

    @api.multi
    def generate_qp_customer_xml_after(self):
        """报文已发送至QP"""
        pass


    @api.multi
    def print_check_reports(self):
        """"""
        return self.env['report'].get_action(self,'customs_center.report_dec_customs_check_template')


    @api.multi
    def print_invoice(self):
        """打印发票按钮"""
        self.env['report'].get_action(self,'customs_center.print_dec_customs_invoice_template')

        self.information_attachment_ids=(4,2902)






    @api.multi
    def generate_single_customer_xml(self):
        """ 生成报关单报文+随附单据报文 发送单一窗口 存放到指定目录 """
        self.update({'cus_dec_sent_way': 'single'})  # 前端点击发送通道按钮之后 确定发送通道 隐藏另一条通道
        for line in self:
            # 判断当前报关单的随附单据中是否有数据
            attach_list = []
            for attach in self.information_attachment_ids:
                attach_data = attach.datas
                attach_list.append(attach_data)
            # 如果第一个附件中有值，说明随附单据解析入库成功
            delegate_to_xml(line)
            # if attach_list:
            #     generate_attach_xml_to_single(line)
            #     self.update({'cus_dec_sent_state': 'succeed'})
            #     return True
            # else:
            #     raise UserError(_("该报关单关联的随附单据附件无效，请检查！"))


    @api.multi
    def generate_qp_customer_xml(self):
        """ 生成报文发送QP  存放到指定目录 """
        self.update({'cus_dec_sent_way': 'QP'})  # 前端点击发送通道按钮之后 确定发送通道 隐藏另一条通道
        for line in self:
            # 判断当前报关单的随附单据中是否有数据
            attach_list = []
            for attach in self.information_attachment_ids:
                attach_data = attach.datas
                attach_list.append(attach_data)
            delegate_to_xml(line)
            # 如果第一个附件中有值，说明随附单据解析入库成功
            if attach_list:
                generate_attach_xml_to_single(line)
                self.update({'cus_dec_sent_state': 'succeed'})
                return True
            else:
                raise UserError(_("该报关单关联的随附单据附件无效，请检查！"))

    @api.multi
    def dec_send_success(self):
        pass
        return True


    # @api.model
    # @q_job.job
    @api.multi
    def parse_receipt_xml(self):
        """解析回执报文"""
        # 设置文件路径path
        # company_name = self.env.user.company_id.name
        # company_name = '0000016165'
        customs_dec_model_dic = self.env['customs_center.customs_dec'].default_get(
            ['dec_company_customs_code'])  # 获取报关单模型对象
        company_xml_parse_path = customs_dec_model_dic.get('dec_company_customs_code')  # 获取配置信息中的 申报单位海关编码 作为解析路径

        recv_path = os.path.join(RECV_XML_BASE_PATH, company_xml_parse_path.encode('utf-8'))
        error_path = os.path.join(ERROR_XML_BASE_PATH, company_xml_parse_path.encode('utf-8'))
        bakup_path = os.path.join(BAKUP_XML_BASE_PATH, company_xml_parse_path.encode('utf-8'))
        # 检查并生成相应的目录
        check_and_mkdir(recv_path, error_path, bakup_path)

        files = os.listdir(recv_path)
        files = [filename for filename in files if filename.endswith('.xml')]
        if not files:
            return True
        files = [os.path.join(recv_path, i) for i in files]

        # 读文件，用lxml解析报文
        for xml_message in files:
            with open(xml_message, 'r') as f:
                tree = etree.parse(f)
                root = tree.getroot()
                response_dic = {}
                business_dic = {}
                root_name = etree.QName(root).localname
                if root_name == u'DecImportResponse':
                    for child in root.iterchildren():
                        key = etree.QName(child).localname
                        value = child.text
                        response_dic[key] = value
                elif root_name == u'DEC_DATA':
                    result_node = root.find('DEC_RESULT')
                    result_info_node = root.find('RESULT_INFO')
                    business_dic['DEC_RESULT'] = {}
                    for child in result_node.iterchildren():
                        if child.text:
                            business_dic['DEC_RESULT'][child.tag] = child.text
                            business_dic['RESULT_INFO'] = result_info_node.text if result_info_node.text else ''
                else:
                    _logger.error(u'Find error format xml message: %s' % xml_message.decode('utf-8'))
                    shutil.move(xml_message, error_path)
                    continue
            # 根据报文中客户端代码找到关联的报关单
            rep_client_no = response_dic.get('ClientSeqNo')
            bus_client_no = business_dic['DEC_RESULT'].get('CLIENTSEQ_NO') if business_dic.get('DEC_RESULT') else None

            dec_sheets = self.env['customs_center.customs_dec'].search(
                [('client_seq_no', '=', rep_client_no or bus_client_no)])
            # 原周杨实现方式
            # dec_sheets = self.env['customs_center.customs_dec'].search(
            #     [('name', '=', rep_client_no or bus_client_no)])
            if not dec_sheets:
                _logger.error(
                    u'{} Can\'t find related declaration sheet according to ClientSeqNo {}'
                        .format(xml_message.decode('utf-8'), rep_client_no or bus_client_no))
                shutil.move(xml_message, error_path)
                continue
            dec_sheet = dec_sheets[0]
            if not dec_sheet.dec_seq_no:
                dec_sheet.dec_seq_no = response_dic.get('SeqNo') or business_dic.get('SEQ_NO')  # 回填统一编号
            # if not dec_sheet.entry_id:
            #     dec_sheet.entry_id = business_dic.get('ENTRY_ID', None)  # 根据回执 回填海关编号
            # if not dec_sheet.dec_date:
            #     dec_date_str = business_dic.get('D_DATE', None)
            #     dec_date = datetime.strptime(dec_date_str,'%Y%m%d')  # 将字符串日期 转换为日期格式
            #     dec_sheet.dec_date = dec_date  # 回填申报日期
            if response_dic:
                resp_code = response_dic.get('ResponseCode')
                status = self.env['customs_center.dec_res_status'].search([('code', '=', resp_code)])
                print(response_dic)
                message = response_dic['ErrorMessage']
            else:
                resp_code = business_dic['DEC_RESULT']['CHANNEL']
                status = self.env['customs_center.dec_res_status'].search([('code', '=', resp_code)])
                message = business_dic['RESULT_INFO']
                dec_sheet.entry_id = business_dic['DEC_RESULT'].get('ENTRY_ID', None)
                dec_date_str = business_dic['DEC_RESULT'].get('D_DATE', None)
                if dec_date_str:
                    dec_date = datetime.strptime(dec_date_str, '%Y%m%d')  # 将字符串日期 转换为日期格式
                    dec_sheet.dec_date = dec_date  # 回填申报日期

            if not status:
                _logger.error(
                    u'%s Can\'t find related status obj according to response code' % xml_message.decode('utf-8'))
                shutil.move(xml_message, error_path)
                continue
            receipt_dic = {
                'status_id': status[0].id,
                'message': message,
                'customs_declaration_id': dec_sheet.id
            }
            try:
                self.env['customs_center.dec_result'].create(receipt_dic)
                dec_sheet.cus_dec_rec_state = status[0].name if status[0].name else None # 更新 报关单模型的回执状态字段
            except Exception, error_info:
                _logger.error(u'{} {}'.format(xml_message.decode('utf-8'), str(error_info).decode('utf-8')))
                shutil.move(xml_message, error_path)
                continue
            else:
                shutil.move(xml_message, bakup_path)
                _logger.info(u'Had parsed the xml message %s' % xml_message.decode('utf-8'))

    @api.multi
    def create_customs_declearation(self):
        """创建商品列表"""

        return True


class WorkSheet(models.Model):
    """" 工作单 """
    _inherit = 'work_sheet'

    customs_declaration_ids = fields.One2many(comodel_name="customs_center.customs_order", inverse_name="work_sheet_id",
                                        string="Customs Order")
    # 报关单状态
    customs_declaration_state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                                ('succeed', 'Success'),
                                                                ('cancel', 'Cancel'),
                                                                ('failure', 'Failure')], compute='_get_customs_state')

    @api.depends('customs_declaration_ids')
    def _get_customs_state(self):
        """ 获取当前工作单对应的通关清单 状态"""
        for sheet in self:
            if sheet.customs_declaration_ids:
                customs_obj = sheet.customs_declaration_ids[0]
                sheet.customs_declaration_state = customs_obj.customs_declaration_state


class DecLicenseDoc(models.Model):
    """ 随附单证 """
    _name = 'customs_center.dec_lic_doc'
    _rec_name = 'dec_license_no'
    _description = 'DecLicenseDoc'

    dec_license_no = fields.Char(string="license no")  # 单证编号
    # 多对一关联 报关单
    customs_declaration_id = fields.Many2one(comodel_name="customs_center.customs_dec",
                                       string="customs declaration")
    dec_license_doc_type_id = fields.Many2one(comodel_name="basedata.dec_license_doc_type", string="DecLicenseDoc type")   # 单证类型/单证代码

class GoodsWizard(models.TransientModel):
    _name = 'customs_center.goods_wizard'
    _description = 'Customs Goods Wizard'

    cus_goods_tariff_id = fields.Many2one(comodel_name="basedata.cus_goods_tariff", string="cus goods Code TS", required=False, )
    goods_model = fields.Char(string="goods model", required=False, )
    deal_qty = fields.Float(string="deal quantity", default=1, )
    deal_unit_price = fields.Monetary(string="deal unit price")
    deal_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="deal unit", required=False, )
    deal_total_price = fields.Monetary(string="deal total price")
    currency_id = fields.Many2one(comodel_name="basedata.cus_currency", string="currency id", required=False, )
    first_qty = fields.Float(string="first quantity", required=False, )
    first_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="First Unit", required=False, )
    second_qty = fields.Float(string="second quantity", required=False, )
    second_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="second Unit", required=False, )
    origin_country_id = fields.Many2one(comodel_name="delegate_country", string="origin country", required=False, )
    destination_country_id = fields.Many2one(comodel_name="delegate_country", string="destination country", required=False, )
    duty_mode_id = fields.Many2one(comodel_name="basedata.cus_duty_mode", string="Duty Mode", required=False, )
    goods_classification_id = fields.Many2one(comodel_name="customs_center.goods_classify", string="Goods Classification", required=False, )    # 客户料号
    supervision_condition = fields.Char(string="supervision condition", required=False, )


    @api.onchange('deal_qty', 'deal_unit_price')
    def _compute_total_goods_price(self):
        """根据当前商品列表的成交单价 X 成交数量数量 计算出商品单行总价"""
        if self.deal_qty != 0:
            self.deal_total_price = self.deal_qty * self.deal_unit_price


    @api.onchange('cus_goods_tariff_id')
    def _generate_about_name(self):
        """根据当前海关税则编码的变化 改变商品名称 并通过onchange装饰器，自动执行_generate_about_name方法"""
        if self.cus_goods_tariff_id:
            self.goods_name = self.cus_goods_tariff_id.NameCN
            self.first_unit = self.cus_goods_tariff_id.first_unit
            self.second_unit = self.cus_goods_tariff_id.second_unit
            self.supervision_condition = self.cus_goods_tariff_id.supervision_condition

    @api.onchange('goods_classification_id')
    def _generate_about_goods_info(self):
        """根据当前合规客户料号的变化 改变商品名称 商品编码等信息 并通过onchange装饰器，自动执行_generate_about_name方法"""
        if self.goods_classification_id:
            self.cus_goods_tariff_id = self.goods_classification_id.cus_goods_tariff_id
            self.goods_name = self.goods_classification_id.goods_name
            self.goods_model = self.goods_classification_id.goods_model
            self.first_unit = self.goods_classification_id.first_unit
            self.second_unit = self.goods_classification_id.second_unit
            self.origin_country_id = self.goods_classification_id.origin_country_id
            self.destination_country_id = self.goods_classification_id.destination_country_id
            self.duty_mode_id = self.goods_classification_id.duty_mode_id
            self.ManualSN = self.goods_classification_id.ManualSN
            self.supervision_condition = self.goods_classification_id.supervision_condition


    @api.multi
    def create_goods_list(self):
        """创建报关单商品列表"""

        return True
