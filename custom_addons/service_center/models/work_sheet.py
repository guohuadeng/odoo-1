# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError


class WorkSheet(models.Model):
    """工作单"""

    _name = "work_sheet"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "work sheet"
    _table = "work_sheet"
    _rec_name = "name"

    # 基本信息
    name = fields.Char(string='Work Sheet ID', required=True, copy=False, state={'draft': [('readonly', False)]},
                       default=lambda self: _('New'))   # 工作单号
    business_type = fields.Many2one(comodel_name="business_type", string="Business Type")   # 业务类型
    customer = fields.Many2one(comodel_name="res.partner", string="Customer", required=True,
                               domain=[('is_company', '=', True), ('customer', '=', True)])  # 委托单位
    settlement_object = fields.Many2one(comodel_name="res.partner", string="Settlement Object",
                                        required=True, )  # 结算对象
    customer_project_no = fields.Char(string='customer project no')   # 客户项目号
    inner_protocol_no = fields.Char(string='Inner Protocal No')   # 内部协议号
    contact = fields.Many2one(comodel_name="res.partner", string="Contact")                 # 联系人
    goods_source = fields.Selection(selection=[('p', 'Pointed'), ('s', 'Seize'),
                                               ('F', 'Filiale')], string="Goods Source", default='s')     # 揽货类型
    deal_type = fields.Many2one(comodel_name="stock.incoterms", string="Deal Type",
                                required=False, )  # 贸易条款, Deal Type
    sale_order_no = fields.Many2one(comodel_name="sale.order",
                                 string="SaleOrder No", ondelete='set null')                   # 销售订单号, SaleOrder No
    contract_no = fields.Many2one(comodel_name="contract.sale_contract", string="Contract No")     # 合同号, Contract No
    company = fields.Many2one(comodel_name="res.company", string="Company", required=False,
                              default=lambda self: self.env.user.company_id.id)                 # 公司, Company
    sale_man = fields.Many2one(comodel_name='res.users', string='Saleman')   # 销售员, Saleman
    customer_service = fields.Many2one(comodel_name="res.users", string="Customer Service", required=False,
                                       default=lambda self: self.env.uid)        # Customer Service,客服
    operation_requirements = fields.Text(string="Operation Requirements",
                                         required=False, )        # 操作要求,Operation Requirements

    # 业务选项
    booking = fields.Boolean(string='Booking', default=True)   # 订舱
    fumigation = fields.Boolean(string='Fumigation')             # 熏蒸
    inspection = fields.Boolean(string="Inspection")             # 报检
    land_trans = fields.Boolean(string="Land Transportation")      # 陆运
    warehouse = fields.Boolean(string="Warehouse")           # 仓储
    custom = fields.Boolean(string="Custom")                 # 报关
    # deliver_order = fields.Boolean(string='Deliver Order')            # 换单
    switch_bill = fields.Boolean(string='Switch Bill')            # 换单

    # 发运信息
    consignor = fields.Many2one(comodel_name='res.partner', string='Consignor')  # 发货人
    input_company = fields.Many2one(comodel_name='res.partner',string='Input Company')   # 通知人
    consignee = fields.Many2one(comodel_name='res.partner', string='Consignee')   # 收货人
    overseas_agent = fields.Many2one(comodel_name='res.partner',string='Overseas Agent',
                                     domain=[('is_company', '=', True)])   # 海外代理
    Notifier = fields.Many2one(comodel_name="res.partner",string="Notifier",
                               domain=[('is_company', '=', True)])
    OverseaAgent = fields.Many2one(comodel_name="res.partner",
                                   string="OverseaAgent",
                                   domain=[('is_company', '=', True)])  # 海外代理
    # start_port = fields.Many2one(comodel_name='delegate_port', string='LoadingPort')  # 起运港
    # transit_port = fields.Many2one(comodel_name='delegate_port', string='TransshipmentPort')      # 中转港
    # final_port = fields.Many2one(comodel_name='delegate_port', string='DestinationPort')        # 目的港
    loading_port = fields.Many2one(comodel_name='basedata.internation_port', string='LoadingPort')  # 起运港
    transition_port = fields.Many2one(comodel_name='basedata.internation_port', string='TransshipmentPort')      # 中转港
    destination_port = fields.Many2one(comodel_name='basedata.internation_port', string='DestinationPort')        # 目的港
    destination = fields.Char(string='Final Destination')           # 最终目的地
    route = fields.Many2one(comodel_name="route", string="Route")      # 航线
    mbl_no = fields.Char(string='MBL No')   # 海运主单
    hbl_no = fields.Char(string='HBL No')   # 海运分单
    mawb = fields.Char(string='MAWB ')      # 空运主单号
    hawb = fields.Char(string='HAWB')       # 空运分单号
    master_no = fields.Char(string="Master NO", compute='_compute_master_house_no')     # 主单号
    house_no = fields.Char(string="House NO", compute='_compute_master_house_no')       # 分单号

    transport_item = fields.Many2one(comodel_name="transportation_term",
                                     string="Transportation Term", required=False, )   # Transport Item， 运输条款
    freight_clause = fields.Many2one(comodel_name="freight_clause", string="Freight Clause", required=False, )  # 运费条款

    # 订舱信息
    book_agent = fields.Many2one(comodel_name="res.partner", string="Booking Agent", required=False,
                                   domain=[('is_company', '=', True), ('customer', '=', True)])         # 订舱代理
    air_company = fields.Many2one(comodel_name="res.partner", string="AirlineCompany", required=False,
                                  domain=[('is_company', '=', True), ('customer', '=', True), ('supplier', '=', True)])   # 航空公司
    flight = fields.Char(string='Flight')                       # 航班
    cabin_space = fields.Char(string='FreightSpace')                  #舱位
    ship_company = fields.Many2one(comodel_name="res.partner", string="ShippingCompany")    # 船公司
    ship_name = fields.Char(string='Vessel')                    # 船名
    ship_count = fields.Char(string='Voyage')                       # 航次
    start_date = fields.Datetime(string='SailingDate')             # 开航日期
    arrive_date = fields.Datetime(string='Arrival Port Date')                # 到港日期
    leave_date = fields.Datetime(string='Departure Port Date')                 # 离港日期
    open_date = fields.Datetime(string='Open Port Date')                      # 开港日期
    customer_contract_no = fields.Char(string="Customer Contract NO")       # 客户合同号
    trade_mode_id = fields.Many2one(comodel_name='delegate_trade_mode', string='Trade Mode')  # 监管方式
    goodsValue = fields.Monetary(string='Goods Value', currency_field='goods_currency_id')    # 货值
    goods_currency_id = fields.Many2one(comodel_name="res.currency", string="Goods Currency")   # 货值币种
    goods_size_ids = fields.One2many(comodel_name="service_center.goods_size", inverse_name="work_sheet_id", string="Goods Size")     # 货物尺寸

    # 箱货信息
    packing_mode = fields.Selection(string="Container Load Type",
                                    selection=[('fcl', 'FCL'), ('lcl', 'LCL')],
                                    required=False, )  # 装箱方式
    packing_description = fields.Text(string="Container Load Note", required=False, )   # 装箱说明
    containers_size = fields.One2many(comodel_name="container_type_and_qty", inverse_name="work_order_id",
                                      string="Containers Size", required=False, )   # 箱型箱量
    cn_name = fields.Text(string="Chinese Name")  # 中文名称
    hs_code = fields.Char(string='Hs Code', size=10)   # 税号
    en_name = fields.Text(string="English Name")  # 英文名称
    marks = fields.Text(string='Marks')

    qty = fields.Integer(string='Qty')  # 委托件数
    gross_weight = fields.Float(string='GrossWeight', digits=dp.get_precision('charge weight'))  # 委托毛重
    volume = fields.Float(string='Volume', digits=dp.get_precision('Stock Weight'))  # 委托体积
    charge_weight = fields.Float(string='Charge Weight', store=True, digits=dp.get_precision('charge weight'))  # 委托计费重量

    book_cargo_qty = fields.Integer(string='Qty')  # 订舱件数
    book_cargo_gross_weight = fields.Float(string='GrossWeight', digits=dp.get_precision('Stock Weight'))  # 订舱毛重
    book_cargo_volume = fields.Float(string='Volume', digits=dp.get_precision('Stock Weight'))  # 订舱体积
    book_cargo_charge_weight = fields.Float(string='Charge Weight', digits=dp.get_precision('Stock Weight'))  # 订舱计费重量

    actual_qty = fields.Integer(string='Qty')  # 实际件数
    actual_gross_weight = fields.Float(string='GrossWeight', digits=dp.get_precision('Stock Weight'))  # 实际毛重
    actual_volume = fields.Float(string='Volume', digits=dp.get_precision('Stock Weight'))  # 实际体积
    actual_charge_weight = fields.Float(string='Charge Weight', digits=dp.get_precision('Stock Weight'))  # 实际计费重量
    wrap_type = fields.Many2one(comodel_name='delegate_packing', string='Wrap Type')  # 包装类型
    goods_attribute = fields.Many2one(comodel_name='goods_attribute', string='attribute name')  # 货物属性

    # 换单信息
    switch_bill_company = fields.Many2one(comodel_name="res.partner", string="Switch Bill Company")  # 换单公司， sheet_company
    # switch_bill_address = fields.Char(string="Switch Bill Address", required=False, )   # 换单地址
    # switch_bill_contact = fields.Char(string="Switch Bill Contact", required=False, )  # 换单联系方式
    switch_bill_address = fields.Char(string="Switch Bill Address", store=True,)   # 换单地址  获取当前换单公司信息 联系人录入的其他地址
    switch_bill_contact = fields.Char(string="Switch Bill Contact", store=True,)   # 换单联系方式
    switch_bill_estimated_date = fields.Date(string="Switch Bill Estimated Date", required=False, )  # 预计换单时间,Estimated  Date
    switch_bill_real_date = fields.Date(string="Switch Bill Real Date", required=False, )  # 实际换单日期, Real Date

    # 操作信息
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed'),
                                        ('done', 'Done'),
                                        ('cancel', 'Cancel')], string='status', readonly=True, default='draft')

    # 其它相关字段
    in_out = fields.Selection(string='InOut', related='business_type.in_out', readonly=True)    # related='business_type.in_out'
    trans_mode_code = fields.Many2one(related='business_type.transport_mode', string="Transport Mode", readonly=True)
    business_type_code = fields.Char(string="Business Type Code", related='business_type.code', readonly=True)
    # business_stage = fields.One2many(comodel_name="service_center.business_stage", inverse_name="work_sheet",
    #                                  string="Business Stage", required=False, )
    current_state = fields.One2many(comodel_name="service_center.current_state", inverse_name="work_sheet_id",
                                    string="Current State")

    # 增加附件上传功能
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')

    @api.multi
    def _compute_attachment_number(self):
        """附件上传"""
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'work_sheet'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)

    @api.multi
    def action_get_attachment_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'work_sheet'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'work_sheet', 'default_res_id': self.id}
        return res

    @api.multi
    @api.constrains('hs_code')
    def _check_hs_code(self):
        """ 增加hs_code字段的 录入限制条件 字符长度不能少于6位置 """
        for obj in self:
            len_hs_code = obj.hs_code
            if len_hs_code and len(len_hs_code) < 6:
                raise Exception(_('The length of HS code cannot be less than six！'))


    @api.multi
    @api.onchange('switch_bill_company')
    def _compute_switch_bill_address(self):
        """可以获取 联系人下的地址"""
        for company_info in self:
            company_name = company_info.switch_bill_company
            if company_name.city and company_name.street:
                company_address = '%s %s' % (company_name.city, company_name.street)
                company_contact = company_name.phone
                company_info.switch_bill_address = company_address
                company_info.switch_bill_contact = company_contact
            else:
                company_info.switch_bill_address = ''
                company_info.switch_bill_contact = ''


    # @api.multi
    # @api.onchange('switch_bill_company')
    # def _compute_switch_bill_address(self):
    #     for company_info in self:
    #         company_name = company_info.type
    #         if company_name.type:
    #             if company_name.type == 'other':
    #                 company_address = company_name.child_ids
    #                 company_contact = company_name.phone
    #                 print("**********6666666666**********")
    #                 print(company_address)
    #                 print(company_contact)
    #                 company_info.switch_bill_address = company_address
    #                 company_info.switch_bill_contact = company_contact
    #         else:
    #             company_info.switch_bill_address = ''
    #             company_info.switch_bill_contact = ''


    @api.multi
    @api.onchange('customer')
    def _get_sale_man(self):
        for sheet in self:
            sheet.sale_man = sheet.customer.user_id
            sheet.settlement_object = sheet.customer
            sheet.goods_source = sheet.customer.seize_goods_type
            sheet.contact = False    # (sheet.customer.child_ids[0] if sheet.customer.child_ids else False)
            sheet.contract_no = False
            sheet.sale_order_no = False
            if sheet.business_type.in_out == 'e':
                sheet.consignor = sheet.customer
            elif sheet.business_type.in_out == 'i':
                sheet.consignee = sheet.customer

    @api.multi
    def alert_current_state(self):
        """弹出业务状态窗口"""
        for sheet in self:
            return {
                'name': "Business Stage",
                'type': "ir.actions.act_window",
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'service_center.current_state',
                'src_model': 'service_center.current_state',
                'views': [[False, 'tree'], [False, 'form']],
                'domain': [['work_sheet_id', '=', sheet.id]],
                'target': 'new'
            }

    @api.multi
    @api.onchange('goods_size_ids')
    def _compute_qty(self):
        """根据货物尺寸计算工作单的总件数、体积、计费重量"""
        for obj in self:
            qty = obj.goods_size_ids.mapped('qty')
            obj.qty = sum(qty)

            volume = obj.goods_size_ids.mapped(lambda v: v.length * v.width * v.height * v.qty)
            obj.volume = sum(volume)/1000000.0

            # 计费重量=货物尺寸/6000(即体积重)与毛重之间，取较大值
            volume_weight = sum(obj.goods_size_ids.mapped(lambda v: v.length * v.width * v.height * v.qty))/6000.0
            print(type(volume_weight))

            float_charge_weight = round(max(volume_weight, obj.gross_weight),1)

            if (float_charge_weight - int(float_charge_weight)) == 0 or (
                float_charge_weight - int(float_charge_weight)) == 0.5:
                obj.charge_weight = float_charge_weight
            elif (float_charge_weight - int(float_charge_weight)) > 0.5:
                obj.charge_weight = round(int(float_charge_weight) + 1, 1)
            elif (float_charge_weight - int(float_charge_weight)) > 0 and (
                float_charge_weight - int(float_charge_weight)) < 0.5:
                obj.charge_weight = round(int(float_charge_weight) + 0.5, 1)

    @api.multi
    @api.onchange('gross_weight')
    def _compute_charge_weight(self):
        self.ensure_one()
        obj = self[0]
        # 计费重量=货物尺寸/6000(即体积重)与毛重之间，取较大值
        volume_weight = sum(obj.goods_size_ids.mapped(lambda v: v.length * v.width * v.height * v.qty))/6000.0
        # print(type(volume_weight))
        float_charge_weight = round(max(volume_weight, obj.gross_weight), 1)

        if (float_charge_weight - int(float_charge_weight)) == 0 or (float_charge_weight-int(float_charge_weight)) == 0.5:
            obj.charge_weight = float_charge_weight
        elif (float_charge_weight - int(float_charge_weight)) > 0.5:
            obj.charge_weight = round(int(float_charge_weight) + 1, 1)
        elif (float_charge_weight - int(float_charge_weight)) > 0 and (float_charge_weight-int(float_charge_weight))< 0.5:
            obj.charge_weight = round(int(float_charge_weight) + 0.5, 1)


    # 计算公式，需求变更，注释代码
    #
    # @api.multi
    # @api.onchange('book_cargo_gross_weight', 'book_cargo_volume')
    # def _compute_book_cargo_charge_weight(self):
    #     self.ensure_one()
    #     obj = self[0]
    #     obj.book_cargo_charge_weight = max(obj.book_cargo_gross_weight, obj.book_cargo_volume/0.006)
    #
    # @api.multi
    # @api.onchange('actual_gross_weight', 'actual_volume')
    # def _compute_actual_charge_weight(self):
    #     self.ensure_one()
    #     obj = self[0]
    #     obj.actual_charge_weight = max(obj.actual_gross_weight, obj.actual_volume/0.006)

    @api.multi
    def custom_book(self):
        """订舱"""
        pass

    @api.multi
    def confirm(self):
        """确认"""
        self.write({
            'state': 'confirmed'
        })

    @api.multi
    def complete(self):
        self.write({
            'state': 'done'
        })
        return True

    @api.multi
    def canceld(self):
        self.write({
            'state': 'cancel'
        })

        return True

    @api.multi
    def recover(self):
        self.write({
            'state': 'draft'
        })

        return True

    @api.model
    def create(self, vals):
        """设置命名和业务类型"""

        if vals.get('name', _('New')) == _('New'):
            business_type_id = self._context.get('default_business_type')
            # print(business_type_id)
            if business_type_id:
                business_type_obj = self.env['business_type'].browse(int(business_type_id))
                business_type_code = business_type_obj.code

                import pytz
                tz = pytz.timezone('Asia/Shanghai')
                local_time = fields.datetime.now(tz).strftime('%y%m')
                name = business_type_code + local_time
                qsets = self.search([('name', 'like', name + '%')])

                if len(qsets) == 0:
                    num = 1
                else:
                    name_sets = []
                    for i in qsets:
                        s = i.name[-4:]
                        try:
                            name_sets.append(int(s))
                        except ValueError:
                            raise ValidationError(
                                _('The last four num of order occur wrong, please make sure it is numbers'))
                    num = max(name_sets) + 1
                vals['name'] = (name + '%04d') % num
            else:
                raise ValidationError(_('business type context occur error!'))


            # vals['name'] = self.env['ir.sequence'].next_by_code('work_sheet') or _('New')
        result = super(WorkSheet, self).create(vals)

        # 当工作单创建时，关联所有业务阶段对象
        business_stage = self.env['service_center.business_stage'].search([('business_type', '=', vals['business_type'])])
        for stage in business_stage:
            status = stage.business_status_id.sorted(key=lambda r:r.sequence)
            self.env['service_center.current_state'].create({
                'work_sheet_id': result.id,
                'business_stage_id': stage.id,
                'business_status_id': status[0].id
            })

        return result

    @api.multi
    def action_work_sheet_send(self):
        """发送邮件"""
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        print("start send email")
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'work_sheet',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "sale.mail_template_data_notification_email_sale_order"
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def print_work_sheet(self):
        """打印各自的报表"""
        self.ensure_one()
        obj = self[0]
        xml_id_dict = obj.business_type.get_xml_id()
        xml_id = xml_id_dict.get(obj.business_type.id)
        report = {
            'basedata.business_type_for_sea_import': 'service_center.report_work_sheet_sea_import_template',
            'basedata.business_type_for_sea_export': 'service_center.report_work_sheet_sea_export_template',
            'basedata.business_type_for_air_import': 'service_center.report_work_sheet_air_import_template',
            'basedata.business_type_for_air_export': 'service_center.report_work_sheet_air_export_template',
        }
        return self.env['report'].get_action(self, report.get(xml_id))

    @api.multi
    @api.depends('business_type', 'mbl_no', 'hbl_no', 'mawb', 'hawb')
    def _compute_master_house_no(self):
        """根据业务类型计算主分单号"""
        for obj in self:
            trans_code = obj.business_type.transport_mode.code
            if trans_code == '2':
                obj.master_no = obj.mbl_no
                obj.house_no = obj.hbl_no
            elif trans_code == '5':
                obj.master_no = obj.mawb
                obj.house_no = obj.hawb
            else:
                raise UserWarning(_('transport type error!'))

    @api.onchange("business_type")
    def onchange_business_type(self):
        """当业务状态改变时，改变港口字段的domain"""
        result = {}
        if self.business_type.code in ['SI', 'SE']:
            result = {
                'domain': {
                    'loading_port': [('port_type', '=', 'seaport')],
                    'transition_port': [('port_type', '=', 'seaport')],
                    'destination_port': [('port_type', '=', 'seaport')],
                }
            }
        elif self.business_type.code in ['AI', 'AE']:
            result = {
                'domain': {
                    'loading_port': [('port_type', '=', 'airport')],
                    'transition_port': [('port_type', '=', 'airport')],
                    'destination_port': [('port_type', '=', 'airport')],
                }
            }

        return result



class ContainersSize(models.Model):
    """装箱明细"""
    _name = 'containers_list'
    _description = 'box containers list'
    _table = 'containers_list'

    container_size = fields.Many2one(comodel_name="container_type", string=u"箱型")    # 箱型, ContainerType
    container_count = fields.Char(string=u"箱号")                          # 箱号,ContainerNo
    container_weight = fields.Float(string=u"箱重",  required=False,
                                    digits=dp.get_precision('Stock Weight'))     # 箱重, ContainerWeight
    seal_no = fields.Char(string=u"封号", required=False, )                # 封号,SealNo
    pcs = fields.Integer(string=u"件数", required=False, )                 # 件数,PCS
    gross_weight = fields.Float(string="",  required=False, digits=dp.get_precision('Stock Weight'))  # 毛重,GrossWeight
    volume = fields.Float(string=u"体积",  required=False, digits=dp.get_precision('Stock Weight'))    # 体积,Volume
    goods_name = fields.Char(string=u"品名", required=False, )       # 品名,GoodsName
    soc = fields.Boolean(string=u"是否货主箱", )                      # 是否货主箱,SOC


class ContainerTypeAndQty(models.Model):
    """箱型箱量"""
    _name = 'container_type_and_qty'
    _description = 'container type and qty'
    _table = 'container_type_and_qty'
    _rec_name = 'id'

    work_order_id = fields.Many2one(comodel_name="work_sheet", string="Work Order", required=False, )   # 工作单
    container_type_id  = fields.Many2one(comodel_name="container_type", string="Container Type", required=False, )
    container_qty = fields.Integer(string="Container Qty", required=False, )
    soc = fields.Boolean(string="SOC",  )   # 是否货主箱
    container_no = fields.Char(string="ContainerNo")
    seal_no = fields.Char(string="SealNo")

    @api.constrains('container_no')
    def _check_container_no(self):
        """集装箱号规则"""
        char_code = "0123456789A?BCDEFGHIJK?LMNOPQRSTU?VWXYZ"
        for container in self:
            str_code = container.container_no
            if len(str_code) != 11:
                raise ValidationError(_('The length of container num is wrong!'))
            num = 0
            for i in range(0, 10):
                idx = char_code.find(str_code[i])
                if idx == -1 or char_code[idx] == '?':
                    raise ValidationError(_("The container num contains invalid char"))
                idx = idx * (2 ** i)
                num += idx
            num = (num % 11) % 10
            if num != int(str_code[-1]):
                raise ValidationError(_("The validate code is wrong!"))
