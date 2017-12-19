# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Customer(models.Model):
    """ 客户信息字段添加 """

    _inherit = 'res.partner'
    _description = 'add partner fields model'

    @api.multi
    def _count_contract(self):
        for partner in self:
            partner.contract_num = len(partner.contract)

    # 基本信息
    short_name = fields.Char(string='Short Name')
    en_name = fields.Char(string='English Name')
    company_code = fields.Char(string='Code', copy=False,
                       default=lambda self: _(''))
    business_type = fields.Many2many(comodel_name='business_type', string='Business Type')

    # 销售栏加入的信息
    department = fields.Many2many(comodel_name="hr.department", string="Department", required=False)
    seize_goods_type = fields.Selection(string="Goods Source",
                                        selection=[('p', 'Pointed'), ('s', 'Seize'), ('F', 'Filiale')], default='s',
                                        required=False, )     # 揽货类型

    # 关联合同
    contract = fields.One2many(comodel_name="contract.sale_contract", inverse_name="customer", string="Contract", required=False, )
    contract_num = fields.Integer(string="Contract Count", compute='_count_contract', required=False, )
    # 合规认证
    unify_social_credit_code = fields.Char(string='USCI', help='Unified Social Credit Identifier')   # 统一社会信用代码
    HS_Code = fields.Char(string='HS Code', help='Harmonized System Code')     # 海关编码
    CIQ_register_code = fields.Char(string='CIQ Code', help='CIQ register code')      # 检验检疫注册编码

    birthday = fields.Datetime(string='Birthday')
    special_requirement = fields.One2many(comodel_name="special_requirement", inverse_name="customer",
                                          string="Special Requirement" )

    certificate_manager = fields.One2many(comodel_name="certificate_management", inverse_name="customer",
                                          string="Certificate Manager", required=False, )
    certificate_count = fields.Integer(string="Certificate Count", compute='_count_certificate_manager', required=False, )

    is_company = fields.Boolean(string='Is a Company', default=True,
                                help="Check if the contact is a company, otherwise it is a person")
    customer_service_ids = fields.Many2many(comodel_name="res.users", string="Customer Service", )  # 客服

    # 增加注册地址
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ('register', 'Register address'),
         ('other', 'Other address')], string='Address Type',
        default='contact',
        help="Used to select automatically the right address according to the context in sales and purchases documents.")

    display_name = fields.Char(compute='_compute_display_name', store=True, index=True)

    # @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name')
    # def _compute_display_name(self):
    #     diff = dict(show_address=None, show_address_only=None, show_email=None)
    #     names = dict(self.with_context(**diff).name_get())
    #
    #     for partner in self:
    #         old_str_info = names.get(partner.id)
    #         new_str_info = old_str_info.split(' ')[1]+old_str_info.split(' ')[0]
    #         partner.display_name = new_str_info
    #         print(new_str_info.encode('utf-8'))

    @api.depends('certificate_manager')
    @api.multi
    def _count_certificate_manager(self):
        for person in self:
            person.certificate_count = len(person.certificate_manager)

    def jump_certificate_manager(self):

        self.ensure_one()
        form_id = self.env.ref('customer_fields_extend.view_certificate_management_form').id
        # print(form_id)
        dic = {
            'type': 'ir.actions.act_window',
            'res_model': self.env['certificate_management']._name,  # this model
            'view_type': 'form',
            'view_mode': 'tree, form',
            'view_ids': [(form_id, 'form')],
            'domain': [('id', 'in', self.certificate_manager.ids)],
            'context': {'default_customer': self.id}
        }
        return dic

    # 结算和收付信息
    s_date_type = fields.Selection(string="Settlement Date Type",
                                   selection=[('0', 'ETD'), ('1', 'ETA'), ('2', 'Business Date'), ('3', 'Invoice Date')],
                                   required=False )        # 结算日期类型 2:业务日期 3:发票日期
    s_period = fields.Selection(string="Settlement Period",
                                selection=[('0', 'Depend Month'),
                                    ('1', 'Depend Week'),
                                    ('2', 'Specify Date'), ( '3', 'Invoice Date')],
                                required=False, )       # 结算周期 0:按月结算 1:按周结算 2:每月指定日期 3:发票日期
    s_date = fields.Integer(string="Settlement Date", required=False,
                            help='settlement date for every date')    # 每月__号为结算日期
    s_account_period = fields.Integer(string="Account Period", required=False, )    # 帐期
    s_account_period_type = fields.Selection(string="Account Period Type",
                                             selection=[('0', 'Day'), ('1', 'Week'), ('2', 'Month')],
                                     required=False, )      # 账期类型 0:day 1:天 2:周 3:月
    # s_use_agent = fields.Boolean(string="结算代理")
    # s_agent_inverse = fields.Many2one(comodel_name='res.partner', string='代理客户', index=True)
    # s_agent = fields.One2many(comodel_name="res.partner", inverse_name="s_agent_inverse",
    #                           string="结算代理", required=False, )
    s_credit_limit = fields.Monetary(string="Credit", required=False, currency_field='s_currency')      # 额度
    s_currency = fields.Many2one(comodel_name="res.currency", string="Credit Currency", required=False, )     # 额度币种
    r_receipt_payment_type = fields.Selection(selection=[('0', 'Receipt'),('1', 'Payment'),('2', 'Receipt And Payment')],
                                              string='Receipt Payment Type', default='1')   #  收付类型 0：收款 1：付款 2：收付款
    r_receipt_payment_date = fields.Datetime(string='Receipt Payment Date')     # 收付日期
    r_receipt_payment_way = fields.Selection(
        selection=[('0', 'Cash'), ('1', 'Check'), ('2', 'Transfer'),
                   ('3', 'Promissory'), ('4', 'Collection And Payment'), ('5', 'Bank Credit'), ('6', 'Telegraphic Transfer')],
        string='Receipt Payment Mode',
        default='1'
    )       # 收付方式 0:现金 1:支票 2:转账 3:本票 4:代收代付 5:银行授信
    r_note = fields.Text(string='Note')     # 附加说明

    @api.multi
    def name_get(self):
        res = []
        for partner in self:
            name = partner.name or ''

            if partner.company_name or partner.parent_id:
                if not name and partner.type in ['invoice', 'delivery', 'other']:
                    name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
                if not partner.is_company:
                    name = "%s" % (name)
            if self._context.get('show_address_only'):
                name = partner._display_address(without_company=True)
            if self._context.get('show_address'):
                name = name + "\n" + partner._display_address(without_company=True)
            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')
            if self._context.get('show_email') and partner.email:
                name = "%s <%s>" % (name, partner.email)
            if self._context.get('html_format'):
                name = name.replace('\n', '<br/>')
            res.append((partner.id, name))
        return res

    ################################################
    # 获取公司汉字拼音的首字母 并且大写
    # def multi_get_letter(self, str_input):
    #     if isinstance(str_input, unicode):
    #         unicode_str = str_input
    #     else:
    #         try:
    #             unicode_str = str_input.decode('utf8')
    #         except:
    #             try:
    #                 unicode_str = str_input.decode('gbk')
    #             except:
    #                 print 'unknown coding'
    #                 return
    #     return_list = []
    #     for one_unicode in unicode_str:
    #         return_list.append(self.single_get_first(one_unicode))
    #     return return_list
    #
    # def single_get_first(self, unicode1):
    #     str1 = unicode1.encode('gbk')
    #     try:
    #         ord(str1)
    #         return str1
    #     except:
    #         asc = ord(str1[0]) * 256 + ord(str1[1]) - 65536
    #         if asc >= -20319 and asc <= -20284:
    #             return 'a'
    #         if asc >= -20283 and asc <= -19776:
    #             return 'b'
    #         if asc >= -19775 and asc <= -19219:
    #             return 'c'
    #         if asc >= -19218 and asc <= -18711:
    #             return 'd'
    #         if asc >= -18710 and asc <= -18527:
    #             return 'e'
    #         if asc >= -18526 and asc <= -18240:
    #             return 'f'
    #         if asc >= -18239 and asc <= -17923:
    #             return 'g'
    #         if asc >= -17922 and asc <= -17418:
    #             return 'h'
    #         if asc >= -17417 and asc <= -16475:
    #             return 'j'
    #         if asc >= -16474 and asc <= -16213:
    #             return 'k'
    #         if asc >= -16212 and asc <= -15641:
    #             return 'l'
    #         if asc >= -15640 and asc <= -15166:
    #             return 'm'
    #         if asc >= -15165 and asc <= -14923:
    #             return 'n'
    #         if asc >= -14922 and asc <= -14915:
    #             return 'o'
    #         if asc >= -14914 and asc <= -14631:
    #             return 'p'
    #         if asc >= -14630 and asc <= -14150:
    #             return 'q'
    #         if asc >= -14149 and asc <= -14091:
    #             return 'r'
    #         if asc >= -14090 and asc <= -13119:
    #             return 's'
    #         if asc >= -13118 and asc <= -12839:
    #             return 't'
    #         if asc >= -12838 and asc <= -12557:
    #             return 'w'
    #         if asc >= -12556 and asc <= -11848:
    #             return 'x'
    #         if asc >= -11847 and asc <= -11056:
    #             return 'y'
    #         if asc >= -11055 and asc <= -10247:
    #             return 'z'
    #         return ''
    #
    # def transform(self, str_input):
    #     a = self.multi_get_letter(str_input)
    #     b = ''
    #     if not a:
    #         return ''
    #
    #     for i in a:
    #         b = b + i.capitalize()
    #     return b
    #
    # @api.model
    # def create(self, vals):
    #     """提取客户企业名称拼音首字母 """
    #     if vals.get('company_code', _('New')) == _('New'):
    #         company_name = vals.get('name')
    #         vals['company_code'] = self.transform(company_name)
    #
    #     result = super(Customer, self).create(vals)
    #     return result
    ####################################################################


class SpecialRequirement(models.Model):
    """ 特殊要求 """
    _name = 'special_requirement'
    _description = 'special requirement'
    _rec_name = 'name'

    customer = fields.Many2one(comodel_name='res.partner', string='Customer')     # 客户
    name = fields.Char(string='Special Requirement Name')         # 特殊要求名称
    business_type = fields.Many2many(comodel_name='business_type', string='Business Type')   # 业务类型
    remark = fields.Text(string='Remark')   # 备注