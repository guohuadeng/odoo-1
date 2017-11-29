# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import odoo.addons.decimal_precision as dp
import odoo.addons.queue_job.job as q_job
from odoo.tools import config
import logging, os, shutil
from lxml import etree
# from custom_addons.customs_center.utils.to_xml_message import delegate_to_xml
from ..utils.to_xml_message import delegate_to_xml
_logger = logging.getLogger(__name__)

RECV_XML_BASE_PATH = config.options['recv_xml_message_path']
ERROR_XML_BASE_PATH = config.options['error_xml_message_path']
BAKUP_XML_BASE_PATH = config.options['bakup_xml_message_path']


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

    name = fields.Char(string="Name")  # 报关单流水号
    client_seq_No = fields.Char(string="client seq No")  # 报关单客户端编号
    # 关联工作单
    work_sheet_id = fields.Many2one(comodel_name="work_sheet", string="Work Sheet")  # 工作单ID
    # 关联企业报关单 目录配置模型 多对一
    et_dec_catalog_ids = fields.Many2one(comodel_name="customs_center.dec_settings", string="Setting Dec catalog")  # 企业报关单ID
    et_dec_catalog_name = fields.Char(related='et_dec_catalog_ids.et_dec_catalog_name', string="enterprise path")
    # 关联通关清单 多对一
    customs_order_id = fields.Many2one(comodel_name="customs_center.customs_order", string="customs Order")
    cus_ciq_No = fields.Char(string="cus Ciq No")  # 关检关联号
    custom_master_id = fields.Many2one(comodel_name="delegate_customs", string="Dec Custom")  # 申报口岸 / 申报地海关

    entry_type_id = fields.Many2one(comodel_name="basedata.cus_entry_type", string="Entry Type")  # 报关单类型 关联报关单类型字典表，待新增
    bill_type_id = fields.Many2one(comodel_name="basedata.cus_filing_bill_type", string="bill Type")    # 备案清单 待新建，备案清单类型表
    inout = fields.Selection(string="InOut", selection=[('I', 'Import'), ('E', 'Export'), ], required=True)  # 进出口类型
    dec_seq_no = fields.Char(string="DecSeqNo")  # 统一编号
    pre_entry_id = fields.Char(string="PreEntryId")  # 预录入编号
    entry_id = fields.Char(string="EntryId")  # 海关编号
    ManualNo = fields.Char(string="Manual No")  # 备案号
    customer_contract_no = fields.Char(string="Customer Contract No")  # 合同协议号
    in_out_date = fields.Datetime(string="InoutDate", required=True)   # 进出口日期
    dec_date = fields.Datetime(string="DecDate", required=True)   # 申报日期
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
    licenseNo_id = fields.One2many(comodel_name="customs_center.dec_lic_doc",
                                inverse_name="customs_declaration_id", string="License No")  # 许可证号    一对多 关联随附单证模型

    payment_mark = fields.Selection(string="payment mark", selection=[('1', u'经营单位'),
                                                        ('2', u'收货单位'),
                                                        ('3', u'申报单位')], )  # 纳税单位

    origin_arrival_country_id = fields.Many2one(comodel_name="delegate_country",
                                                string="Origin Arrival Country")  # 启运/抵达国
    port_id = fields.Many2one(comodel_name="delegate_port", string="Port", )  # 装货/指运港
    region_id = fields.Many2one(comodel_name="delegate_region", string="Region")  # 境内目的/货源地
    trade_terms_id = fields.Many2one(comodel_name="delegate_trade_terms", string="Trade Term")  # 成交方式 or 贸易条款

    fee_mark = fields.Selection(string="FeeMark", selection=[('1', u'1-率'),
                                                        ('2', u'2-单价'),
                                                        ('3', u'3-总价')], )  # 运费标记
    fee_rate = fields.Float(string="FeeRate", digits=dp.get_precision('Product Price'),)  # 运费/率
    fee_currency_id = fields.Many2one(comodel_name="basedata.cus_currency", string="FeeCurrency", required=False, )  # 运费币制

    insurance_mark = fields.Selection(string="InsurMark", selection=[('1', '1-率'),
                                                        ('3', '3-总价')], )  # 保险费标记
    insurance_rate = fields.Float(string="InsurRate", digits=dp.get_precision('Product Price'),)  # 保险费/率
    insurance_currency_id = fields.Many2one(comodel_name="basedata.cus_currency", string="InsurCurrency_id", required=False, )  # 保险费币制

    other_mark = fields.Selection(string="OtherMark", selection=[('1', u'1-率'),
                                                        ('3', u'3-总价')], )  # 杂费标记
    other_rate = fields.Float(string="OtherRate", digits=dp.get_precision('Product Price'),)  # 杂费/率
    other_currency_id = fields.Many2one(comodel_name="basedata.cus_currency", string="OtherCurrency_id", required=False, )  # 杂费币制

    qty = fields.Integer(string="Qty")  # 件数
    gross_weight = fields.Float(string="Gross Weight")  # 毛重
    net_weight = fields.Float(string="Net Weight")  # 净重
    remarks = fields.Text(string="Marks")  # 备注
    packing_id = fields.Many2one(comodel_name="delegate_packing", string="Package Type")  # 包装种类、方式
    trade_country_id = fields.Many2one(comodel_name="delegate_country",
                                       string="Trade Country")  # 贸易国别

    promise1 = fields.Selection(string="promise1", selection=[('0', u'0-否'),
                                                        ('1', u'1-是'),
                                                        ('9', u'9-空')], )  # 特殊关系确认
    promise2 = fields.Selection(string="promise2", selection=[('0', u'0-否'),
                                                        ('1', u'1-是'),
                                                        ('9', u'9-空')], )  # 价格影响确认
    promise3 = fields.Selection(string="promise3", selection=[('0', u'0-否'),
                                                        ('1', u'1-是'),
                                                        ('9', u'9-空')], )  # 支付特许权使用费确认

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
    input_company_id = fields.Many2one(comodel_name="basedata.cus_register_company", string="input company id")  # 消费使用单位 新建企业库表
    business_company_id = fields.Many2one(comodel_name="basedata.cus_register_company", string="business company name")    # 收发货人 新建企业库表

    cop_code = fields.Char(string="cop code")  # 录入单位企业组织机构代码
    cop_name = fields.Char(string="cop name")  # 录入单位企业名称
    cop_code_scc = fields.Char(string="cop Social credit uniform coding")  # 录入单位社会信用统一编码
    inputer_name = fields.Char(string="inputer name")  # 录入员姓名
    oper_name = fields.Char(string="oper name")     # 操作员姓名
    certificate = fields.Char(string="oper card certificate")   # 操作员卡的证书号
    ic_code = fields.Char(string="IC number")  # 操作员IC卡号/录入员IC卡号

    # cop_code_scc = fields.Char(string="cop Social credit uniform coding")  # 录入单位社会信用统一编码
    # owner_code_scc = fields.Char(string="owner Social credit uniform coding")  # 货主单位/生产消费单位 社会信用统一编码
    # trade_code_scc = fields.Char(string="owner Social credit uniform coding")  # 经营单位 / 收发货人 统一编码

    decl_trn_rel = fields.Selection(string="DeclTrnRel", selection=[('0', u'一般报关单'), ('1', u'转关提前报关单')])   # 报关/转关关系标志
    ediId = fields.Selection(string="ediId", selection=[('1', u'普通报关'), ('3', u'北方转关提前'),
                                                        ('5', u'南方转关提前'), ('6', u'普通报关')], )  # 报关标志
    # trade_code = fields.Char(string="Trade Code", required=True, )  # 经营单位编号

    # 关联报关单商品列表 1对多关系
    dec_goods_list_ids = fields.One2many(comodel_name="customs_center.dec_goods_list",
                                         inverse_name="customs_declaration_id", string="dec goods name")

    customs_declaration_state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], default='draft')  # 报关单状态
    receipt_ids = fields.One2many(comodel_name="customs_center.dec_result", inverse_name="customs_declaration_id",
                                  string="Recipts", required=False, )

    @api.model
    def create(self, vals):
        """设置报关单命名规则"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('code_customs_declaration') or _('New')
        result = super(CustomsDeclaration, self).create(vals)

        return result

    @api.multi
    def customs_delegate_to_xml(self):
        """ 根据报关单生成xml报文 存放到指定目录 """
        for line in self:
            delegate_to_xml(line)
        return True

    # @api.model
    # def parse_receipt_xml(self):
    #     pass

    @api.model
    @q_job.job
    def parse_receipt_xml(self):
        """解析回执报文"""

        # 设置文件路径path
        company_name = self.env.user.company_id.name
        recv_path = os.path.join(RECV_XML_BASE_PATH, company_name.encode('utf-8'))
        error_path = os.path.join(ERROR_XML_BASE_PATH, company_name.encode('utf-8'))
        bakup_path = os.path.join(BAKUP_XML_BASE_PATH, company_name.encode('utf-8'))
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
                [('name', '=', rep_client_no or bus_client_no)])
            if not dec_sheets:
                _logger.error(
                    u'{} Can\'t find related declaration sheet according to ClientSeqNo {}'
                        .format(xml_message.decode('utf-8'), rep_client_no or bus_client_no))
                shutil.move(xml_message, error_path)
                continue
            dec_sheet = dec_sheets[0]
            if not dec_sheet.dec_seq_no:
                dec_sheet.dec_seq_no = response_dic.get('SeqNo') or business_dic.get('SEQ_NO')
            if response_dic:
                resp_code = response_dic.get('ResponseCode')
                status = self.env['customs_center.dec_res_status'].search([('code', '=', resp_code)])
                print(response_dic)
                message = response_dic['ErrorMessage']
            else:
                resp_code = business_dic['DEC_RESULT']['CHANNEL']
                status = self.env['customs_center.dec_res_status'].search([('code', '=', resp_code)])
                message = business_dic['RESULT_INFO']

            if not status:
                _logger.error(
                    u'%s Can\'t find related statu obj according to response code' % xml_message.decode('utf-8'))
                shutil.move(xml_message, error_path)
                continue
            receipt_dic = {
                'status_id': status[0].id,
                'message': message,
                'customs_declaration_id': dec_sheet.id
            }
            try:
                self.env['customs_center.dec_result'].create(receipt_dic)
            except Exception, error_info:
                _logger.error(u'{} {}'.format(xml_message.decode('utf-8'), str(error_info).decode('utf-8')))
                shutil.move(xml_message, error_path)
                continue
            else:
                shutil.move(xml_message, bakup_path)
                _logger.info(u'Had parsed the xml message %s' % xml_message.decode('utf-8'))


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



