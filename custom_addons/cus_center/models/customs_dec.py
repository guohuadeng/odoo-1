# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta

import odoo.addons.decimal_precision as dp

from odoo import models, fields, api, _
from ..utils.to_generate_customs_xml_and_send_to_ex import send_customs_dec_edoc_xml_to_ex
from ..utils.to_generate_customs_xml_and_send_to_ex import send_customs_dec_xml_to_ex
from ..utils.to_parse_customer_xml_from_cus import parse_customs_dec_edoc_xml
from ..utils.to_parse_customer_xml_from_cus import parse_customs_dec_xml
from ..utils.to_parse_receipt_xml_from_ex import parse_receipt_xml

_logger = logging.getLogger(__name__)


class CustomsDeclaration(models.Model):
    """ 报关单 """
    _name = 'cus_center.customs_dec'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Customs Declaration'

    name = fields.Char(string="Name", copy=False)  # 报关单流水号   # copy=False 防止服务器动作复制报关单信息时复制
    client_seq_no = fields.Char(string="client seq No")  # 报关单客户端编号
    synergism_seq_no = fields.Char(string="Synergism seq No")  # 客户协同单号

    # customs_customer_id 委托报关客户（与customer_id区分开,customer_id指的是委托单位，即与该笔业务进行结算的单位(可能不是实际的报关单位，例如富士康委托中外运做运输，中外运委托运通安达做报关，则中外运是委托单位，富士康是委托报关单位)）
    customs_customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")

    # 关联工作单
    work_sheet_id = fields.Many2one(comodel_name="work_sheet", string="Work Sheet")  # 工作单ID

    # 关联通关清单 多对一
    customs_order_id = fields.Many2one(comodel_name="cus_center.customs_order", string="customs Order")

    cus_ciq_No = fields.Char(string="us Ciq No")  # 关检关联号
    custom_master_id = fields.Many2one(comodel_name="cus_args.customs", string="Dec Custom")  # 申报口岸 / 申报地海关

    entry_type_id = fields.Many2one(comodel_name="cus_args.entry_type", string="Entry Type")  # 报关单类型 关联报关单类型字典表，待新增
    bill_type_id = fields.Many2one(comodel_name="cus_args.filing_bill_type", string="bill Type")  # 备案清单 待新建，备案清单类型表
    inout = fields.Selection(string="InOut", selection=[('I', u'进口'), ('E', u'出口'), ],
                             track_visibility='always', )  # 进出口类型
    dec_seq_no = fields.Char(string="DecSeqNo")  # 统一编号
    pre_entry_id = fields.Char(string="PreEntryId")  # 预录入编号
    entry_id = fields.Char(string="EntryId")  # 海关编号
    manual_no = fields.Char(string="Manual No", track_visibility='always', )  # 备案号
    customer_contract_no = fields.Char(string="Customer Contract No", track_visibility='onchange', )  # 合同协议号
    in_out_date = fields.Datetime(string="InoutDate")  # 进出口日期
    dec_date = fields.Datetime(string="DecDate")  # 申报日期
    customs_id = fields.Many2one(comodel_name="cus_args.customs", string="Customs")  # 进出口岸

    transport_mode_id = fields.Many2one(comodel_name="cus_args.transport_mode",
                                        string="Transport Mode")  # 运输方式
    native_ship_name = fields.Char(string="Native Ship Name")  # 运输工具名称
    voyage_no = fields.Char(string="Voyage No")  # 航次号

    bill_no = fields.Char(string="Bill No")  # 提运单号
    trade_mode_id = fields.Many2one(comodel_name="cus_args.trade_mode", string="Trade Mode")  # 监管方式
    cut_mode_id = fields.Many2one(comodel_name="cus_args.cut_mode", string="CutMode id")  # 征免性质   征免性质表待新建
    in_ratio = fields.Integer(string="In ratio")  # 征免比例
    license_no = fields.Char(string="Bill No")  # 许可证号

    origin_arrival_country_id = fields.Many2one(comodel_name="cus_args.country",
                                                string="Origin Arrival Country")  # 启运/抵达国
    port_id = fields.Many2one(comodel_name="cus_args.port", string="Port", )  # 装货/指运港
    internal_district_id = fields.Many2one(comodel_name="cus_args.internal_district", string="Region")  # 境内目的/货源地
    trade_terms_id = fields.Many2one(comodel_name="cus_args.trade_terms", string="Trade Term")  # 成交方式

    # 关联 纳税单位标识类型
    payment_mark = fields.Many2one(comodel_name="cus_center.pay_mark_type", string="payment mark")  # 纳税单位

    # 关联 费用标识类型
    fee_mark = fields.Many2one(comodel_name="cus_center.exp_mark_type", string="FeeMark")  # 运费标记
    insurance_mark = fields.Many2one(comodel_name="cus_center.exp_mark_type", string="insurance_mark")  # 保险费标记
    other_mark = fields.Many2one(comodel_name="cus_center.exp_mark_type", string="other_mark")  # 杂费标记

    # 关联 是否标识类型
    promise1 = fields.Many2one(comodel_name="cus_center.whet_mark_type", string="promise1")  # 特殊关系确认
    promise2 = fields.Many2one(comodel_name="cus_center.whet_mark_type", string="promise2")  # 价格影响确认
    promise3 = fields.Many2one(comodel_name="cus_center.whet_mark_type", string="promise3")  # 支付特许权使用费确认

    fee_rate = fields.Float(string="FeeRate", digits=dp.get_precision('Product Price'), )  # 运费/率
    fee_currency_id = fields.Many2one(comodel_name="cus_args.currency", string="FeeCurrency")  # 运费币制

    insurance_rate = fields.Float(string="InsurRate", digits=dp.get_precision('Product Price'), )  # 保险费/率
    insurance_currency_id = fields.Many2one(comodel_name="cus_args.currency", string="InsurCurrency_id")  # 保险费币制

    other_rate = fields.Float(string="OtherRate", digits=dp.get_precision('Product Price'), )  # 杂费/率
    other_currency_id = fields.Many2one(comodel_name="cus_args.currency", string="OtherCurrency_id")  # 杂费币制

    qty = fields.Integer(string="Qty")  # 件数
    gross_weight = fields.Float(string="Gross Weight")  # 毛重
    net_weight = fields.Float(string="Net Weight")  # 净重
    remarks = fields.Text(string="Marks")  # 备注
    wrap_type_id = fields.Many2one(comodel_name="cus_args.wrap_type", string="Wrap Type")  # 包装种类
    trade_country_id = fields.Many2one(comodel_name="cus_args.country",
                                       string="Trade Country")  # 贸易国别

    # 报关单关联信息
    rel_dec_No = fields.Char(string="RelDec No")  # 关联报关单
    rel_man_No = fields.Char(string="License No")  # 关联 备案
    bonded_No = fields.Char(string="Bonded No")  # 监管场所
    customs_field = fields.Char(string="CustomsField")  # 货场代码

    declare_company_id = fields.Many2one(comodel_name="cus_args.register_company",
                                         string="declare company name")  # 申报单位
    input_company_id = fields.Many2one(comodel_name="cus_args.register_company",
                                       string="input company id")  # 货主单位 消费使用单位
    business_company_id = fields.Many2one(comodel_name="cus_args.register_company",
                                          string="business company name")  # 经营单位 收发货人

    @api.onchange('business_company_id')
    def _compute_input_company(self):
        """根据当前选中的收发货人 改变 消费使用单位"""
        for customs_dec in self:
            if customs_dec.business_company_id != 0:
                customs_dec.input_company_id = customs_dec.business_company_id

    cop_code = fields.Char(string="cop code")  # 录入单位企业组织机构代码
    cop_name = fields.Char(string="cop name")  # 录入单位企业名称
    cop_code_scc = fields.Char(string="cop Social credit uniform coding")  # 录入单位社会信用统一编码
    inputer_name = fields.Char(string="inputer name")  # 录入员姓名
    oper_name = fields.Char(string="oper name")  # 操作员姓名
    certificate = fields.Char(string="oper card certificate")  # 操作员卡的证书号
    ic_code = fields.Char(string="IC number")  # 操作员IC卡号/录入员IC卡号
    dec_company_customs_code = fields.Char(string="declare company path")  # 申报单位海关编号/ 报文存放路径

    # cop_code_scc = fields.Char(string="cop Social credit uniform coding")  # 录入单位社会信用统一编码
    # owner_code_scc = fields.Char(string="owner Social credit uniform coding")   # 货主单位/生产消费单位 社会信用统一编码
    # trade_code_scc = fields.Char(string="owner Social credit uniform coding")   # 经营单位 / 收发货人 统一编码

    decl_trn_rel = fields.Selection(string="DeclTrnRel", selection=[('0', u'一般报关单'), ('1', u'转关提前报关单')])  # 报关/转关关系标志
    ediId = fields.Selection(string="ediId", selection=[('1', u'普通报关'), ('3', u'北方转关提前'),
                                                        ('5', u'南方转关提前'), ('6', u'普通报关')], )  # 报关标志

    # 关联报关单商品列表 1对多关系
    dec_goods_list = fields.One2many(comodel_name="cus_center.dec_goods_list",
                                     inverse_name="customs_dec_id", string="dec goods name")
    #
    # 集装箱信息 报关单 关联集装箱模型 一对多
    dec_container_ids = fields.One2many(comodel_name="cus_center.dec_container",
                                        inverse_name="customs_dec_id", string="container info")

    # 随附单证，一对多
    dec_lic_doc_list = fields.One2many(comodel_name="cus_center.dec_lic_doc",
                                       inverse_name="customs_dec_id", string="Dec Lic Doc")

    # 报关单状态
    customs_declaration_state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                                            ('succeed', 'Success'),
                                                                            ('cancel', 'Cancel'),
                                                                            ('failure', 'Failure')],
                                                 default='draft')
    # 回执状态
    receipt_list = fields.One2many(comodel_name="cus_center.dec_result", inverse_name="customs_dec_id",
                                   string="Recipts", required=False, )

    # 报关单发送状态
    cus_dec_sent_state = fields.Selection(string="Sent State", selection=[('draft', 'Draft'),
                                                                          ('succeed', 'Success'),
                                                                          ('cancel', 'Cancel'),
                                                                          ('failure', 'Failure')],
                                          default='draft')
    # 报关单回执状态    注：这里设置store=True 否则仪表板 加载搜索展示没有回执的数据 后台会报错
    cus_dec_rec_state = fields.Char(string="dec receive status", compute='_get_current_rec_state',
                                    store=True)

    # 报关单发送通道选择
    cus_dec_sent_way = fields.Selection(string="Sent way",
                                        selection=[('single', 'single windows'), ('QP', 'quick pass')])

    # 附件拖拽上传
    information_attachment_ids = fields.Many2many('ir.attachment')

    #############################################################################################

    @api.multi
    @api.depends('receipt_list')
    def _get_current_rec_state(self):
        # 获取最新回执状态

        for record in self:
            state_sequence = 0
            state_name = False

            for receipt in record.receipt_list:
                if receipt.status_id:
                    if receipt.status_id.sequence >= state_sequence:
                        state_sequence = receipt.status_id.sequence
                        state_name = receipt.status_id.name

            record.cus_dec_rec_state = state_name

    # 服务器动作 复制当前报关单表头数据
    @api.multi
    def duplicate_current_title_data(self):
        """ 复制当前报关单表头数据 """
        self.ensure_one()
        customs_declaration_obj_copy = self.copy()
        customs_declaration_obj_copy.update(
            {'cus_dec_sent_way': '', 'cus_dec_sent_state': ''})  # 将发送通道字段修改为空，否则复制全部的时候，会导致复制的新报关单无法再次发送

        if customs_declaration_obj_copy:
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'cus_center.customs_dec',
                'res_id': customs_declaration_obj_copy.id,
                'context': self.env.context,
                'flags': {'initial_mode': 'edit'},
            }

    # 服务器动作 复制当前报关单全部数据
    @api.multi
    def duplicate_current_all_data(self):
        """ 复制当前报关单全部数据 """
        self.ensure_one()
        customs_declaration_obj_copy = self.copy()
        customs_declaration_obj_copy.update(
            {'cus_dec_sent_way': '', 'cus_dec_sent_state': ''})  # 将发送通道字段修改为空，否则复制全部的时候，会导致复制的新报关单无法再次发送

        # cus_goods_list_ids_list = []
        for line in self:
            if line.dec_goods_list:
                cus_goods_list_ids_list = [goods.copy().id for goods in line.dec_goods_list]
                customs_declaration_obj_copy.dec_goods_list |= self.env['cus_center.dec_goods_list'].search(
                    [('id', 'in', cus_goods_list_ids_list)])
        if customs_declaration_obj_copy:
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'cus_center.customs_dec',
                'res_id': customs_declaration_obj_copy.id,
                'context': self.env.context,
                'flags': {'initial_mode': 'edit'},
            }

    ##############################################################################################
    # 报关单列表视图 回执状态 查看历史回执按钮
    @api.multi
    def btn_review_receipt(self):
        return {
            'name': u"回执历史状态",
            'type': "ir.actions.act_window",
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'cus_center.dec_result',
            'views': [[False, 'tree']],
            'res_id': self.ids,
            "domain": [["customs_dec_id", "=", self.id]],
            'target': 'new'
        }

    # 通关清单生成报关单
    # 通关清单视图中 通过按钮“生成报关单” 触发动作。将当前界面清单id传递过来，执行该方法创建相应报关单
    @api.onchange('customs_order_id')
    def _onchange_customs_order_id(self):
        if not self.customs_order_id:
            return
        customs_order = self.customs_order_id

        # 报关单表体
        self.work_sheet_id = customs_order.work_sheet_id.id

        self.inout = str(customs_order.inout).upper()
        self.customs_id = customs_order.customs_id.id  # 进出口岸
        self.custom_master_id = customs_order.custom_master_id.id
        self.manual_no = customs_order.manual_no
        self.customer_contract_no = customs_order.customer_contract_no
        self.licenseNo = customs_order.license_no
        self.declare_company_id = customs_order.declare_company_id.id
        self.input_company_id = customs_order.input_company_id.id
        self.business_company_id = customs_order.business_company_id.id
        self.transport_mode_id = customs_order.transport_mode_id.id
        self.transport_name = customs_order.transport_name
        self.voyage_no = customs_order.voyage_no
        self.trade_terms_id = customs_order.trade_terms_id.id
        self.wrap_type_id = customs_order.wrap_type_id.id
        self.trade_country_id = customs_order.trade_country_id.id
        self.origin_arrival_country_id = customs_order.origin_arrival_country_id.id
        self.port_id = customs_order.port_id.id
        self.internal_district_id = customs_order.internal_district_id.id
        self.qty = customs_order.qty
        self.gross_weight = customs_order.gross_weight
        self.net_weight = customs_order.net_weight
        self.remarks = customs_order.marks

        # 报关单商品列表
        goods_list = []
        for line in customs_order.order_goods_list:
            goods_list.append((0, 0, {
                'goods_classification_id': line.goods_classification_id.id,  # 客户料号
                'goods_tariff_id': line.goods_tariff_id.id,  # 商品编号
                'goods_name': line.goods_name,  # 商品名称
                'goods_model': line.goods_model,  # 规格型号
                'deal_qty': line.deal_qty,  # 规格型号
                'deal_unit_price': line.deal_unit_price,  # 成交单价
                'deal_unit_id': line.deal_unit_id.id,  # 成交单位
                'deal_total_price': line.deal_total_price,  # 成交总价
                'currency_id': line.currency_id.id,  # 币制
                'first_qty': line.first_qty,  # 第一数量
                'first_unit_id': line.first_unit_id.id,  # 第一单位
                'second_qty': line.second_qty,  # 第一单位
                'second_unit_id': line.second_unit_id.id,  # 第二单位
                'origin_country_id': line.origin_country_id.id,  # 原产国
                'destination_country_id': line.destination_country_id.id,  # 目的国
                'duty_mode_id': line.duty_mode_id.id,  # 征免方式
                'manual_sn': line.manual_sn,  # 备案序号
                'version_no': line.version_no,  # 版本号
                'product_no': line.product_no,  # 货号
            }))
        self.dec_goods_list = goods_list

    ###################################################################

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
                vals['client_seq_no'] = str((datetime.now() + timedelta(hours=8)).strftime('%y%m%d%H%M%S%f'))
        result = super(CustomsDeclaration, self).create(vals)

        return result

    @api.multi
    def generate_single_customer_xml(self):
        """ 生成报关单报文+随附单据报文,存放到指定目录,发送单一窗口  """
        self.update({'cus_dec_sent_way': 'single'})  # 前端点击发送通道按钮之后 确定发送通道 隐藏另一条通道

        for line in self:
            # 判断当前报关单的随附单据中是否有数据
            attach_list = []
            for attach in self.information_attachment_ids:
                attach_data = attach.datas
                attach_list.append(attach_data)

            # 发送报关单xml报文到交换云（单一窗口或QP）
            send_customs_dec_xml_to_ex(line)

            if attach_list:
                # 发送报关单随附单据xml报文到交换云（单一窗口或QP）
                send_customs_dec_edoc_xml_to_ex(line)

            self.update({'cus_dec_sent_state': 'succeed'})

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

            # 发送报关单xml报文到交换云（单一窗口或QP）
            send_customs_dec_xml_to_ex(line)

            if attach_list:
                # 发送报关单随附单据xml报文到交换云（单一窗口或QP）
                send_customs_dec_edoc_xml_to_ex(line)

            self.update({'cus_dec_sent_state': 'succeed'})

    # @api.model
    # @q_job.job
    @api.multi
    def parse_cus_message_xml(self):
        """从客户给物流云发送的报关单报文文件夹中，解析报关单报文（解析入库后生成报关单和随附单据（空附件））"""
        parse_customs_dec_xml(self)

    # @api.model
    # @q_job.job
    @api.multi
    def auto_parse_attach_message_xml(self):
        """从客户给物流云发送的随附单据文件夹中，解析随附单据报文（解析入库后，给相应的附件模型data赋值）"""
        parse_customs_dec_edoc_xml(self)
        pass

    @api.multi
    def generate_single_customer_xml_after(self):
        """报文已发送至单一窗口"""
        pass

    @api.multi
    def generate_qp_customer_xml_after(self):
        """报文已发送至QP"""
        pass

    # @api.model
    # @q_job.job
    @api.multi
    def parse_receipt_xml(self):
        # 解析回执报文
        parse_receipt_xml(self)

    def create_classify_goods(self, dec_sheet):
        print('create_classify_goods')

        if not self.business_company_id:
            return False

        """ 报关单状态为放行后调用该方法 自动归类"""
        for goods_item in self.dec_goods_list:
            # print('goods_item.goods_classification_id', goods_item.goods_classification_id)
            if goods_item.cust_goods_code:
                break

            business_company_id = self.business_company_id.id  # 收发貨人
            cust_goods_code = goods_item.cust_goods_code  # 客户料号
            goods_tariff_no = goods_item.goods_tariff_id.id  # 商品编号
            goods_name = goods_item.goods_name  # 商品名称
            goods_model = goods_item.goods_model  # 规格型号

            # 多条件搜索:收发货人+商品编号+商品名称+规格型号
            history_good_classify_info = self.env['cus_center.goods_classify'].search([
                ('business_company_id', '=', business_company_id),
                ('goods_tariff_id', '=', goods_tariff_no),
                ('goods_name', '=', goods_name),
                ('goods_model', '=', goods_model)
            ])

            # 为真：调用次数字段 加1, 最新调用时间为当前时间
            if history_good_classify_info:
                new_call_count = history_good_classify_info.call_count + 1
                history_good_classify_info.update({'call_count': new_call_count,
                                                   'new_call_date': fields.Datetime.now()})

            # 创建一条新的归类记录
            else:
                classify_goods_dic = {
                    'cust_goods_code': cust_goods_code,  # 客户料号
                    'business_company_id': business_company_id,  # 收发货人
                    'manual_no': self.manual_no,  # 备案号
                    'manual_sn': goods_item.manual_sn,  # 备案序号
                    'goods_tariff_id': goods_tariff_no,  # 商品编号
                    'goods_name': goods_name,  # 商品名称
                    'goods_model': goods_model,  # 规格型号
                    'deal_unit_price': goods_item.deal_unit_price,  # 申报单价
                    'currency_id': goods_item.currency_id.id,  # 币制
                    'deal_unit_id': goods_item.deal_unit_id.id,  # 成交单位
                    'origin_country_id': goods_item.origin_country_id.id,  # 原产国
                    'destination_country_id': goods_item.destination_country_id.id,  # 目的国
                    'duty_mode_id': goods_item.duty_mode_id.id,  # 征免方式
                    'call_count': 1,
                    'new_call_date': fields.Datetime.now(),  # 最近调用时间用当前时间，不是很严谨,需要改进（取商品行新建的时间？）
                    'state': 'approve'
                }

                classify_goods_dic = {item: classify_goods_dic[item]
                                      for item in classify_goods_dic if classify_goods_dic[item]}  # 清除False

                cus_goods_classify_obj = self.env['cus_center.goods_classify'].create(classify_goods_dic)
