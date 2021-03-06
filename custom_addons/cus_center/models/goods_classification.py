# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.exceptions
import logging

_logger = logging.getLogger(__name__)


class GoodsClassification(models.Model):
    """ 商品归类（合规）"""
    _name = 'cus_center.goods_classify'
    _rec_name = 'cust_goods_code'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Goods Classification'

    cust_goods_code = fields.Char(string="Customer Goods Code", index=True, copy=False)  # 客户料号

    business_company_id = fields.Many2one(comodel_name="cus_args.register_company",
                                          string="business company name", required=True)  # 收发货人 / 经营单位
    goods_tariff_id = fields.Many2one(comodel_name="cus_args.goods_tariff", string="cus goods Code TS",
                                      required=False, )  # 海关税则编码 / 商品编号 Code_ts 即 hs_code
    goods_name = fields.Char(string="goods name")  # 商品名称

    goods_model = fields.Char(string="goods model", required=False, )  # 规格型号

    first_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="First Unit",
                                    related='goods_tariff_id.first_unit_id', store=False)  # 第一计量单位
    second_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="second Unit",
                                     related='goods_tariff_id.second_unit_id', store=False)  # 第二计量单位
    supervision_condition = fields.Char(string="supervision condition", related='goods_tariff_id.supervision_condition',
                                        store=False)  # 监管标识/监管标识

    goods_tariff_hs_code = fields.Char(string="cus goods number", related='goods_tariff_id.code_ts', store=True,
                                       required=False, )  # 税则库商品编号，冗余字段 ，主要是为了在报关单添加商品界面，实现按商品编号搜索归类库

    deal_unit_price = fields.Float(string="deal unit price", )  # 成交单价
    deal_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="deal unit", required=False, )  # 成交单位
    currency_id = fields.Many2one(comodel_name="cus_args.currency", string="currency id", required=False, )  # 币制
    origin_country_id = fields.Many2one(comodel_name="cus_args.country", string="origin country", )  # 原产国
    destination_country_id = fields.Many2one(comodel_name="cus_args.country", string="destination country", )  # 目的国

    call_count = fields.Integer(string='call times', help="classify goods call times",
                                default=0)  # 归类商品调用次数(申报放行，算一次调用)
    new_call_date = fields.Datetime(string="new call date")  # 最新调用时间

    @api.onchange('goods_tariff_id')
    def _generate_about_name(self):
        """根据当前海关税则编码的变化 改变监管条件 并通过onchange装饰器，自动执行_generate_about_name方法"""
        for goods_list in self:
            if goods_list.goods_tariff_id:
                goods_list.goods_name = goods_list.goods_tariff_id.name_cn
                # goods_list.first_unit = goods_list.goods_tariff_id.first_unit
                # goods_list.second_unit = goods_list.goods_tariff_id.second_unit
                # goods_list.supervision_condition = goods_list.goods_tariff_id.supervision_condition
                # goods_list.goods_tariff_hs_code = goods_list.goods_tariff_id.code_ts

    duty_mode_id = fields.Many2one(comodel_name="cus_args.duty_mode", string="Duty Mode", )  # 征免方式
    manual_no = fields.Char(string="Manual No")  # 备案号 / 账册号
    manual_sn = fields.Char(string="Manual SN")  # 备案序号

    state = fields.Selection(selection=[('draft', 'Draft'),  # 草稿
                                        ('submitted', 'Submitted'),  # 提交 待审核
                                        ('refused', 'Refused'),  # 审核不通过
                                        ('approve', 'approved')  # 通过审核
                                        ], string='status', readonly=True, default='draft')

    # 合规商品
    @api.multi
    @api.depends('cust_goods_code', 'goods_name', 'goods_tariff_hs_code', 'goods_model')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u"%s %s %s %s" % (record.cust_goods_code if record.cust_goods_code else ''
                                              , record.goods_name if record.goods_name else ''
                                              , record.goods_tariff_hs_code if record.goods_tariff_hs_code else ''
                                              , record.goods_model if record.goods_model else ''))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', '|', ('cust_goods_code', operator, name), ('goods_name', operator, name),
                     ('goods_tariff_hs_code', operator, name)]

        return super(GoodsClassification, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )

    @api.multi
    def submit_review_btn(self):
        """ 商品归类信息提交审核 按钮"""
        self.update({'state': 'submitted'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类审核已提交, 请耐心等待管理员审核 ！<br/>") % (goods_cls_list.goods_tariff_id.code_ts))
            goods_cls_list.message_post(body=body)

    @api.multi
    def re_submit_review_btn(self):
        """ 商品归类信息 重新提交审核 按钮"""
        self.update({'state': 'submitted'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类审核已重新提交, 请耐心等待管理员审核 ！<br/>") % (goods_cls_list.goods_tariff_id.code_ts))
            goods_cls_list.message_post(body=body)

    @api.multi
    def already_reviewed_btn(self):
        """ 商品归类信息 审核通过 按钮"""
        self.update({'state': 'approve'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类，已审核通过！<br/>") % (goods_cls_list.goods_tariff_id.code_ts))
            goods_cls_list.message_post(body=body)

    @api.multi
    def refused_reviewed_btn(self):
        """ 商品归类信息 审核拒绝 按钮"""
        self.update({'state': 'refused'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类，未审核通过！<br/>") % (goods_cls_list.goods_tariff_id.code_ts))
            goods_cls_list.message_post(body=body)

    @api.multi
    def classify_batch_check_submit(self):
        """批量审核提交"""
        self.update({'state': 'submitted'})
        for goods_cls_list in self:
            body = (_("商品归类 批量审核已提交, 请耐心等待管理员审核 ！<br/>"))
            goods_cls_list.message_post(body=body)

    @api.multi
    def classify_batch_check_pass(self):
        """批量审核通过"""
        self.update({'state': 'approve'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类，已审核通过！<br/>") % (goods_cls_list.cus_goods_tariff_id.code_ts))
            goods_cls_list.message_post(body=body)

    @api.constrains('cust_goods_code', 'business_company_id')
    def _check_cus_goods_code(self):
        """ 同一收发货人，料号必须唯一 """
        if self.cust_goods_code:

            goods = self.search([('cust_goods_code', "=", self.cust_goods_code)
                                    , ('business_company_id', "=", self.business_company_id.id)])
            if len(goods) > 1:
                raise odoo.exceptions.except_orm(u'错误', u"%s 已存在料号 %s,不允许重复录入"
                                                 % (self.business_company_id.register_name_cn, self.cust_goods_code))
