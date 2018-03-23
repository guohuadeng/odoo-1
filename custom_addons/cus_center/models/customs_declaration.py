# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
import logging
from ..utils.to_parse_receipt_xml import parse_receipt_message_xml

_logger = logging.getLogger(__name__)


class CustomsDeclaration(models.Model):
    """ 报关单 """
    _name = 'cus_center.cus_dec'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Customs Declaration'

    name = fields.Char(string="Name", copy=False, default=_('New'))   # 报关单流水号
    client_seq_no = fields.Char(string="client seq No")  # 报关单客户端编号
    synergism_seq_no = fields.Char(string="Synergism seq No")  # 客户协同单号
    # 关联通关清单 多对一
    customs_order_id = fields.Many2one(comodel_name="cus_center.cus_order", string="customs Order")
    cus_ciq_No = fields.Char(string="cus Ciq No")  # 关检关联号
    custom_master_id = fields.Many2one(comodel_name="cus_args.customs", string="Dec Custom")  # 申报口岸 / 申报地海关

    entry_type_id = fields.Many2one(comodel_name="cus_args.entry_type", string="Entry Type")  # 报关单类型 关联报关单类型字典表，待新增
    bill_type_id = fields.Many2one(comodel_name="cus_args.filing_bill_type", string="Bill Type")    # 备案清单 待新建，备案清单类型表
    inout = fields.Selection(string="InOut", selection=[('I', u'进口'), ('E', u'出口'), ], track_visibility='always',)  # 进出口类型
    dec_seq_no = fields.Char(string="DecSeqNo")  # 统一编号
    pre_entry_id = fields.Char(string="PreEntryId")  # 预录入编号
    entry_id = fields.Char(string="EntryId")  # 海关编号
    ManualNo = fields.Char(string="Manual No", track_visibility='always',)  # 备案号
    customer_contract_no = fields.Char(string="Customer Contract No", track_visibility='onchange',)  # 合同协议号
    in_out_date = fields.Datetime(string="InoutDate")   # 进出口日期
    dec_date = fields.Datetime(string="DecDate")   # 申报日期
    customs_id = fields.Many2one(comodel_name="cus_args.customs", string="Customs")  # 进出口岸
    transport_mode_id = fields.Many2one(comodel_name="cus_args.transport_mode", string="Transport Mode")  # 运输方式
    NativeShipName = fields.Char(string="Native Ship Name")  # 运输工具名称
    VoyageNo = fields.Char(string="Voyage No")           # 航次号

    bill_no = fields.Char(string="Bill No")           # 提运单号
    trade_mode_id = fields.Many2one(comodel_name="cus_args.trade_mode", string="Trade Mode")  # 监管方式
    CutMode_id = fields.Many2one(comodel_name="cus_args.cut_mode", string="CutMode id")  # 征免性质   征免性质表待新建
    in_ratio = fields.Integer(string="In Ratio")  # 征免比例
    licenseNo = fields.Char(string="Bill No")  # 许可证号
    licenseNo_ids = fields.One2many(comodel_name="customs_center.dec_lic_doc",
                                inverse_name="customs_declaration_id", string="License No")  # 许可证号    一对多 关联随附单证模型

    origin_arrival_country_id = fields.Many2one(comodel_name="cus_args.country",
                                                string="Origin Arrival Country")  # 启运/抵达国
    port_id = fields.Many2one(comodel_name="cus_args.port", string="Port", )  # 装货/指运港
    region_id = fields.Many2one(comodel_name="cus_args.region", string="Region")  # 境内目的/货源地
    trade_terms_id = fields.Many2one(comodel_name="cus_args.trade_terms", string="Trade Term")  # 成交方式 or 贸易条款
    # 关联 纳税单位标识类型 替换 上边注释
    payment_mark = fields.Many2one(comodel_name="cus_center.pay_mark_type", string="payment mark")   # 纳税单位
    # 关联 费用标识类型 替换 上边注释
    fee_mark = fields.Many2one(comodel_name="cus_center.exp_mark_type", string="FeeMark")  # 运费标记
    insurance_mark = fields.Many2one(comodel_name="cus_center.exp_mark_type", string="insurance_mark") # 保险费标记
    other_mark = fields.Many2one(comodel_name="cus_center.exp_mark_type", string="other_mark") # 杂费标记

    # 关联 是否标识类型 替换 上边注释
    promise1 = fields.Many2one(comodel_name="cus_center.whet_mark_type", string="promise1") # 特殊关系确认
    promise2 = fields.Many2one(comodel_name="cus_center.whet_mark_type", string="promise2") # 价格影响确认
    promise3 = fields.Many2one(comodel_name="cus_center.whet_mark_type", string="promise3") # 支付特许权使用费确认

    fee_rate = fields.Float(string="FeeRate", digits=dp.get_precision('Product Price'),)  # 运费/率
    fee_currency_id = fields.Many2one(comodel_name="cus_args.cus_currency", string="FeeCurrency")  # 运费币制

    insurance_rate = fields.Float(string="InsurRate", digits=dp.get_precision('Product Price'),)  # 保险费/率
    insurance_currency_id = fields.Many2one(comodel_name="cus_args.cus_currency", string="InsurCurrency_id")  # 保险费币制

    other_rate = fields.Float(string="OtherRate", digits=dp.get_precision('Product Price'),)  # 杂费/率
    other_currency_id = fields.Many2one(comodel_name="cus_args.cus_currency", string="OtherCurrency_id")  # 杂费币制

    qty = fields.Integer(string="Qty")  # 件数
    gross_weight = fields.Float(string="Gross Weight")  # 毛重
    net_weight = fields.Float(string="Net Weight")  # 净重
    remarks = fields.Text(string="Marks")  # 备注
    packing_id = fields.Many2one(comodel_name="cus_args.packing", string="Package Type")  # 包装种类、方式
    trade_country_id = fields.Many2one(comodel_name="cus_args.country", string="Trade Country")  # 贸易国别
    # 报关单关联信息
    rel_dec_No = fields.Char(string="RelDec No")  # 关联报关单
    rel_man_No = fields.Char(string="License No")  # 关联 备案
    bonded_No = fields.Char(string="Bonded No")  # 监管场所
    customs_field = fields.Char(string="CustomsField")  # 货场代码

    declare_company_id = fields.Many2one(comodel_name="cus_args.register_company", string="declare company name")  # 申报单位
    input_company_id = fields.Many2one(comodel_name="cus_args.register_company", string="input company id")  # 货主单位 消费使用单位
    business_company_id = fields.Many2one(comodel_name="cus_args.register_company", string="business company name")    # 收发货人

    cop_code = fields.Char(string="cop code")  # 录入单位企业组织机构代码
    cop_name = fields.Char(string="cop name")  # 录入单位企业名称

    # 模糊查询 从当前登录的用户所在的公司 模糊匹配海关企业表中的公司
    cop_code_scc = fields.Char(string="cop Social credit uniform coding")  # 录入单位社会信用统一编码
    inputer_name = fields.Char(string="inputer name")  # 录入员姓名
    oper_name = fields.Char(string="oper name")     # 操作员姓名
    certificate = fields.Char(string="oper card certificate")   # 操作员卡的证书号
    ic_code = fields.Char(string="IC number")  # 操作员IC卡号/录入员IC卡号
    dec_company_customs_code = fields.Char(string="declare company path")  # 申报单位海关编号/ 报文存放路径

    decl_trn_rel = fields.Selection(string="DeclTrnRel", selection=[('0', u'一般报关单'), ('1', u'转关提前报关单')])   # 报关/转关关系标志
    ediId = fields.Selection(string="ediId", selection=[('1', u'普通报关'), ('3', u'北方转关提前'),
                                                        ('5', u'南方转关提前'), ('6', u'普通报关')], )  # 报关标志

    # 通关清单
    dec_goods_list_ids = fields.One2many(comodel_name="cus_center.goods_list",
                                         inverse_name="customs_declaration_id", string="dec goods name")

    # 报关单 关联合规模型 一对多 冗余字段 用于修改历史商品列表 通过关联报关单 确认是否已归类
    # dec_goods_classified_ids = fields.One2many(comodel_name="customs_center.goods_classify",
    #                                      inverse_name="customs_declaration_id", string="goods classified")

    # 集装箱信息 报关单 关联集装箱模型 一对多
    dec_container_ids = fields.One2many(comodel_name="customs_center.dec_container",
                                         inverse_name="customs_declaration_id", string="container info")

    state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], default='draft')  # 报关单状态
    # 回执
    receipt_ids = fields.One2many(comodel_name="cus_center.dec_result", inverse_name="customs_declaration_id",
                                  string="Recipts", required=False, )
    cus_dec_rec_state = fields.Char(string="dec receive status")  # 报关单回执状态
    cus_dec_sent_way = fields.Selection(string="Sent way", selection=[('single', 'single windows'),('QP', 'quick pass')])  # 报关单发送通道选择

    # 附件拖拽上传
    information_attachment_ids = fields.Many2many('ir.attachment')


    @api.onchange('business_company_id')
    def _compute_input_company(self):
        """根据当前选中的收发货人 改变 消费使用单位"""
        for customs_dec in self:
            if not customs_dec.business_company_id:
                customs_dec.input_company_id = customs_dec.business_company_id


    @api.multi
    def action_get_dec_attachment_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('customs_center', 'dec_action_attachment')
        res['domain'] = [('res_model', '=', 'customs_center.customs_dec'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'customs_center.customs_dec', 'default_res_id': self.id}
        return res


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


    # 报关单列表视图 回执状态 查看历史回执按钮
    @api.multi
    def btn_review_receipt(self):
        """ 查看历史回执按钮 """

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

        result = super(CustomsDeclaration, self).create(vals)

        return result



    # @api.model
    # @q_job.job
    @api.multi
    def parse_receipt_xml(self):
        """解析回执报文"""
        # 设置文件路径path
        customs_dec_model_dic = self.env['customs_center.customs_dec'].default_get(
            ['dec_company_customs_code'])  # 获取报关单模型对象
        company_xml_parse_path = customs_dec_model_dic.get('dec_company_customs_code')  # 获取配置信息中的 申报单位海关编码 作为解析路径
        # 解析报文
        parse_receipt_message_xml(self, company_xml_parse_path, _logger)
