# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json, requests, base64, logging
from collections import OrderedDict
_logger = logging.getLogger(__name__)


class ClearanceDraft(models.Model):
    """报关原始清单"""
    _name = 'customs_clearance.clearance_draft'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = 'Customs Clearance Draft'

    name = fields.Char(string="Name")
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")     # 客户
    work_sheet_id = fields.Many2one(comodel_name="work_sheet", string="Work Sheet")                 # 工作单
    inout = fields.Selection(string="InOut", selection=[('i', 'Import'), ('e', 'Export'), ])     # 进出口
    customs_id = fields.Many2one(comodel_name="delegate_customs", string="Customs")                             # 进出口岸
    business_company_id = fields.Many2one(comodel_name="res.partner", string="Business Company")  # 收发货人
    input_company_id = fields.Many2one(comodel_name="res.partner", string="InputCompany")        # 生产消费单位
    declare_company = fields.Many2one(comodel_name="res.partner", string="DeclareCompany", required=True, )
    customer_contract_no = fields.Char(string="CustomerContractNo")                                             # 合同号
    trade_terms_id = fields.Many2one(comodel_name="delegate_trade_terms", string="Trade Term")                  # 贸易条款
    trade_mode_id = fields.Many2one(comodel_name="delegate_trade_mode", string="Trade Mode")   # 监管方式
    transport_mode_id = fields.Many2one(comodel_name="delegate_transport_mode",
                                        string="Transport Mode")                               # 运输方式
    trade_country_id = fields.Many2one(comodel_name="delegate_country",
                                       string="Trade Country")                                 # 贸易国别
    origin_arrival_country_id = fields.Many2one(comodel_name="delegate_country",
                                                string="Origin Arrival Country")               # 启运/抵达国
    port_id = fields.Many2one(comodel_name="delegate_port", string="Port", )                                    # 装货/指运港
    region_id = fields.Many2one(comodel_name="delegate_region", string="Region")            # 境内目的/货源地
    qty = fields.Integer(string="Qty")                      # 件数
    pack_id = fields.Many2one(comodel_name="delegate_packing", string="Package Type")           # 包装方式
    gross_weight = fields.Float(string="Groos Weight")      # 毛重
    net_weight = fields.Float(string="Net Weight")          # 净重
    marks = fields.Text(string="Marks")                     # 标记唛码及备注
    declaration_record_ids = fields.One2many(comodel_name="customs_clearance.declaration_record",
                                    inverse_name="declaration_draft_id", string="Declarantion Records")
    state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], default='draft')

    @api.multi
    def send_message(self):
        """发送json格式报关单报文"""
        obj = self[0]
        business_company_address = [obj.business_company_id.country_id.name, obj.business_company_id.state_id.name,
                                    obj.business_company_id.city,obj.business_company_id.street,
                                    obj.business_company_id.street2]
        business_company_address = [i for i in business_company_address if i]
        business_company_address = ''.join(business_company_address)              # 生成收发货人地址

        input_company_address = [obj.input_company_id.country_id.name, obj.input_company_id.state_id.name,
                                 obj.input_company_id.city, obj.input_company_id.street, obj.input_company_id.street2]
        input_company_address = [i for i in input_company_address if i]
        input_company_address = ''.join(input_company_address)              # 生成生产消费单位地址

        MessageHead = OrderedDict()
        T_DHL_Inventory = OrderedDict()
        T_DHL_Inventory_Goods = OrderedDict()

        MessageHead['CustomerCode'] = u'1111980068'
        MessageHead['CustomerName'] = u'北京运通安达报关有限公司'

        T_DHL_Inventory['CustomerInnerCode'] = obj.work_sheet_id.name if obj.work_sheet_id else u'N/A'
        T_DHL_Inventory['Remittance'] = u''
        T_DHL_Inventory['InOutID'] = obj.inout.upper()
        T_DHL_Inventory['PortCO'] = obj.customs_id.Code                     # 进出口岸
        T_DHL_Inventory['PortCN'] = obj.customs_id.NameCN
        T_DHL_Inventory['DealTypeID'] = obj.trade_terms_id.Code             # 成交方 式
        T_DHL_Inventory['DealTypeCN'] = obj.trade_terms_id.NameCN
        T_DHL_Inventory['TransportTypeID'] = obj.transport_mode_id.code     # 运输方式
        T_DHL_Inventory['TransportTypeCN'] = obj.transport_mode_id.name_cn
        T_DHL_Inventory['Qty'] = int(obj.qty)
        T_DHL_Inventory['PackageTypeID'] = obj.pack_id.Code                 # 包装方式
        T_DHL_Inventory['PackageTypeCN'] = obj.pack_id.NameCN
        T_DHL_Inventory['NationCO'] = obj.origin_arrival_country_id.Code    # 启运抵达国
        T_DHL_Inventory['NationCN'] = obj.origin_arrival_country_id.NameCN
        T_DHL_Inventory['TradeModeID'] = obj.trade_mode_id.Code             # 监管方式
        T_DHL_Inventory['TradeModeName'] = obj.trade_mode_id.NameCN
        T_DHL_Inventory['HavenCO'] = obj.port_id.Code                       # 装货/指运港,
        T_DHL_Inventory['HavenCN'] = obj.port_id.NameCN
        T_DHL_Inventory['RegionCO'] = obj.region_id.Code                    # 境内目的/货源地
        T_DHL_Inventory['RegionCN'] = obj.region_id.NameCN
        T_DHL_Inventory['TradeCountryCO'] = obj.trade_country_id.Code       # 贸易国别
        T_DHL_Inventory['TradeCountryCN'] = obj.trade_country_id.NameCN
        T_DHL_Inventory['ContractNo'] = obj.customer_contract_no
        T_DHL_Inventory['Remark'] = obj.marks
        T_DHL_Inventory['DeclareCompanyId'] = obj.declare_company.HS_Code
        T_DHL_Inventory['DeclareCompany'] = obj.declare_company.name
        T_DHL_Inventory['BusinessCompanyId'] = obj.business_company_id.HS_Code  # 收发货人
        T_DHL_Inventory['BusinessCompany'] = obj.business_company_id.name
        T_DHL_Inventory['BusinessCompanyAddress'] = business_company_address
        T_DHL_Inventory['BusinessCompanyTel'] = obj.business_company_id.phone
        T_DHL_Inventory['BusinessCompanyMail'] = obj.business_company_id.email
        T_DHL_Inventory['InputCompanyId'] = obj.input_company_id.HS_Code        # 生产消费单位
        T_DHL_Inventory['InputCompanyOrganizationCode'] = u''
        T_DHL_Inventory['InputCompany'] = obj.input_company_id.name
        T_DHL_Inventory['InputCompanyAddress'] = input_company_address
        T_DHL_Inventory['InputCompanyTel'] = obj.input_company_id.phone
        T_DHL_Inventory['InputCompanyMail'] = obj.input_company_id.email

        _T_DHL_Inventory = set()            # 清除无效字段的数据
        for item in T_DHL_Inventory:
            if not T_DHL_Inventory[item]:
                _T_DHL_Inventory.add(item)
        for item in _T_DHL_Inventory:
            del T_DHL_Inventory[item]

        T_DHL_Inventory_Goods['CustomerPartNo'] = u'T001'
        T_DHL_Inventory_Goods['MaxPackingQty'] = u'10'
        T_DHL_Inventory_Goods['NetWeight'] = u'10'
        T_DHL_Inventory_Goods['GrossWeight'] = u'10'
        T_DHL_Inventory_Goods['DealQty'] = u'10'
        T_DHL_Inventory_Goods['DealUnitID'] = u'001'
        T_DHL_Inventory_Goods['DealUnit'] = u'台'
        T_DHL_Inventory_Goods['DealUnitPrice'] = u'10'
        T_DHL_Inventory_Goods['DealAmount'] = u'100'
        T_DHL_Inventory_Goods['CurrencyID'] = u'142'
        T_DHL_Inventory_Goods['Currency'] = u'人民币'
        T_DHL_Inventory_Goods['CN_Name'] = u'用植物性材料制作的人体模型'
        T_DHL_Inventory_Goods['HSCode_TS'] = u'9618000010'
        T_DHL_Inventory_Goods['Model'] = u'用途|材质|其他'
        T_DHL_Inventory_Goods['PalletsNum'] = u'ZZZ0001'

        dic = {
            'MessageHead': [MessageHead],
            'T_DHL_Inventory': [T_DHL_Inventory],
            # 'T_DHL_Inventory_Goods': [T_DHL_Inventory_Goods],
            'Attachment': []
        }

        data = json.dumps(dic, encoding='utf-8')
        _logger.info(u'发送报文： ' + data)
        data = base64.b64encode(data)
        reponse = requests.post('http://www.aeotrade.com:7009/T_DHL_Inventory_Unified', data=data)
        message = reponse.text
        status = json.loads(message, encoding='utf-8')
        if status['IsOk'] == '1':
            obj.write({'state': 'succeed'})
        else:
            obj.write({'state': 'failure'})
        obj.message_post(body=status['ReturnData'], subject='Returned Message', subtype="mt_note")
        _logger.info(message)

        return True
    #
    # @api.multi
    # def generate_and_sent_xml(self):
    #     """ 生成并发送xml报文 """
    #     pass

    @api.model
    def create(self, vals):
        """设置原始清单命名规则"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('declaration_draft') or _('New')
        result = super(ClearanceDraft, self).create(vals)

        return result


class DeclarationRecord(models.Model):
    _name = 'customs_clearance.declaration_record'
    _rec_name = 'name'
    _description = 'Declaration Record'

    name = fields.Char(string="Customs Declaration No", required=True)                      # 报关单号
    declaration_date = fields.Datetime(string="Customs Declaration Date", required=True)    # 报关日期
    pages = fields.Integer(string="PageCount", required=True, )                             # 页数
    declaration_draft_id = fields.Many2one(comodel_name="customs_clearance.clearance_draft",
                                           string="Declaration Draft")


class WorkSheet(models.Model):
    _inherit = 'work_sheet'

    clearance_draft_ids = fields.One2many(comodel_name="customs_clearance.clearance_draft", inverse_name="work_sheet_id",
                                          string="Clearance Draft")
    custom_count = fields.Integer(string='Custom Declaration', compute='_get_custom_count')
    customs_state = fields.Selection(string="State",selection=[('draft', 'Draft'),
                                                        ('succeed', 'Success'),
                                                        ('cancel', 'Cancel'),
                                                        ('failure', 'Failure')], compute='_get_customs_state')


    @api.depends('clearance_draft_ids')
    def _get_custom_count(self):
        for sheet in self:
            sheet.custom_count = len(sheet.clearance_draft_ids)

    @api.depends('clearance_draft_ids')
    def _get_customs_state(self):
        for sheet in self:
            if sheet.clearance_draft_ids:
                customs_obj = sheet.clearance_draft_ids[0]
                sheet.customs_state = customs_obj.state

    @api.constrains('clearance_draft_ids')
    def _check_clearance_one2one(self):
        for item in self:
                if len(item.clearance_draft_ids) > 1:
                    raise ValidationError(_('work sheet must relate only one clearance draft'))

    @api.model
    def create(self, vals):
        """当创建工作单时，如果报关选项被选上则创建原始清单"""
        obj = super(WorkSheet, self).create(vals)
        if vals.get('custom'):
            dic = {
                'customer_id': obj.customer,
                'work_sheet_id': obj.id,
                'inout': obj.business_type.in_out,
                'business_company_id': obj.consignee if obj.in_out == 'i' else obj.consignor,
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
                if item in {'customer_id', 'business_company_id', 'trade_terms_id', 'trade_mode_id',
                            'transport_mode_id', 'customs_id', 'trade_country_id', 'port_id', 'region_id'}:
                    _dic[item] = dic[item].id
            dic.update(_dic)
            self.env['customs_clearance.clearance_draft'].create(dic)
        return obj

    @api.multi
    def write(self, vals):
        """重写修改方法，使改变报关布尔值时创建报关单"""
        # obj = self[0]
        for obj in self:
            if 'custom' in vals:
                if not obj.custom and not obj.clearance_draft_ids:  # 如果报关选项没有勾选且没有关联的原始清单
                    dic = {
                        'customer_id': obj.customer,
                        'work_sheet_id': obj.id,
                        'inout': obj.business_type.in_out,
                        'business_company_id': obj.consignee if obj.in_out == 'i' else obj.consignor,
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

                    dic = {item: dic[item] for item in dic if dic[item]}    # 清除False
                    _dic = {}                                               # 把object转换为id
                    for item in dic:
                        if item in {'customer_id', 'business_company_id','trade_terms_id', 'trade_mode_id',
                                    'transport_mode_id', 'customs_id', 'trade_country_id', 'port_id', 'region_id'}:
                            _dic[item] = dic[item].id
                    dic.update(_dic)
                    # print(dic)

                    self.env['customs_clearance.clearance_draft'].create(dic)

                elif obj.custom and obj.clearance_draft_ids:
                    if obj.clearance_draft_ids[0].state != 'succeed':
                        obj.clearance_draft_ids.write({'state': 'cancel'})

            if obj.clearance_draft_ids and obj.clearance_draft_ids[0].state != 'succeed':
                dic = {
                    'customer_contract_no': vals.get('customer_contract_no'),
                    # 'trade_terms_id': vals.get('trade_terms_id'),
                    'trade_mode_id': vals.get('trade_mode_id'),
                    'qty': vals.get('qty'),
                    'gross_weight': vals.get('gross_weight'),
                    'pack_id': vals.get('wrap_type')
                }
                dic = {item: dic[item] for item in dic if dic[item]}  # 清除False
                obj.clearance_draft_ids.write(dic)


            # if obj.clearance_draft_ids:
            #     if obj.clearance_draft_ids[0].state != 'succeed':
            #         if obj.custom:
            #             obj.clearance_draft_ids.write({'state': 'cancel'})
            #         else:
            #             obj.clearance_draft_ids.write({'state': 'draft'})
            #         dic = {
            #             'customer_contract_no': vals.get('customer_contract_no'),
            #             # 'trade_terms_id': vals.get('trade_terms_id'),
            #             'trade_mode_id': vals.get('trade_mode_id'),
            #             'qty': vals.get('qty'),
            #             'gross_weight': vals.get('gross_weight'),
            #             'wrap_type': vals.get('wrap_type')
            #         }
            #         dic = {item: dic[item] for item in dic if dic[item]}  # 清除False
            #         obj.clearance_draft_ids.write(dic)


        return super(WorkSheet, self).write(vals)

    @api.multi
    def canceld(self):
        """当工作单取消时，关联的原始清单也同时取消"""
        for sheet in self:
            if sheet.customs_state != 'succeed':
                sheet.clearance_draft_ids.write({'state': 'cancle'})

        return super(WorkSheet, self).canceld()

    @api.multi
    def recover(self):
        """当工作单还原时，被取消的关联的原始清单也同时还原"""
        for sheet in self:
            if sheet.customs_state != 'succeed':
                sheet.clearance_draft_ids.write({'state': 'draft'})

        return super(WorkSheet, self).recover()

    @api.multi
    def customs_clearance(self):
        """跳转到相关报关单界面"""
        for obj in self:
            if not obj.clearance_draft_ids:
                return
            customs_clearance_obj = obj.clearance_draft_ids[0]
            return {
                'name': "Customs Clearance",
                'type': "ir.actions.act_window",
                'view_type': 'form',
                'view_mode': 'form, tree',
                'res_model': 'customs_clearance.clearance_draft',
                'views': [[False, 'form']],
                'res_id': customs_clearance_obj.id,
                'target': 'current'
            }

    @api.multi
    def canceld(self):
        """工作单取消后同时把原始清单取消"""
        obj = self[0]
        if obj.clearance_draft_ids:
            obj.clearance_draft_ids[0].write({'state': 'cancel'})
        return super(WorkSheet, self).canceld()

    @api.multi
    def recover(self):
        """工作单还原后把原始清单也还原"""
        obj = self[0]
        if obj.clearance_draft_ids:
            obj.clearance_draft_ids[0].write({'state': 'draft'})
        return super(WorkSheet, self).recover()

