# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class GoodsClassification(models.Model):
    """ 商品归类（合规）"""
    _name = 'customs_center.goods_classify'
    _rec_name = 'cus_goods_code'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Goods Classification'

    cus_goods_code = fields.Char(string="Customer Goods Code", index=True)     # 客户料号
    # 关联商品列表
    dec_goods_list_ids = fields.One2many(comodel_name="customs_center.cus_goods_list",
                                         inverse_name="cus_goods_tariff_id", string="dec goods name")

    business_company_id = fields.Many2one(comodel_name="basedata.cus_register_company",
                                          string="business company name")  # 收发货人 / 经营单位
    cus_goods_tariff_id = fields.Many2one(comodel_name="basedata.cus_goods_tariff", string="cus goods Code TS", required=False, )  # 海关税则编码 / 商品编号 Code_ts 即 hs_code
    goods_name = fields.Char(string="goods name")  # 商品名称

    # @api.onchange('cus_goods_tariff_id')
    # def _generate_about_name(self):
    #     """根据当前海关税则编码的变化 改变商品名称 并通过onchange装饰器，自动执行_generate_about_name方法"""
    #     for goods_list in self:
    #         if goods_list.cus_goods_tariff_id:
    #             goods_list.goods_name = goods_list.cus_goods_tariff_id.NameCN

    cus_goods_tariff_no = fields.Char(string="cus goods number", required=False, )  # 税则库商品编号 方便前端搜索视图调用

    goods_model = fields.Char(string="goods model", required=False, )  # 规格型号
    first_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="First Unit", )  # 第一计量单位
    second_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="second Unit", )  # 第二计量单位
    supervision_condition = fields.Char (string="supervision condition")  # 监管标识/监管标识

    # first_unit = fields.Char(string="First Unit")  # 第一计量单位
    # second_unit = fields.Char(string="second Unit")  # 第二计量单位
    # supervision_condition = fields.Char(string="supervision condition", required=False, )  # 监管标识/监管标识

    deal_unit_price = fields.Monetary(string="deal unit price", )  # 成交单价/申报单价
    deal_unit = fields.Many2one(comodel_name="basedata.cus_unit", string="deal unit", required=False, )  # 成交单位
    currency_id = fields.Many2one(comodel_name="basedata.cus_currency", string="currency id", required=False, )  # 币制
    origin_country_id = fields.Many2one(comodel_name="delegate_country", string="origin country", )  # 原产国
    destination_country_id = fields.Many2one(comodel_name="delegate_country", string="destination country", )  # 目的国


    @api.onchange('cus_goods_tariff_id')
    def _generate_about_name(self):
        """根据当前海关税则编码的变化 改变监管条件 并通过onchange装饰器，自动执行_generate_about_name方法"""
        for goods_list in self:
            if goods_list.cus_goods_tariff_id:
                goods_list.goods_name = goods_list.cus_goods_tariff_id.NameCN
                goods_list.first_unit = goods_list.cus_goods_tariff_id.first_unit
                goods_list.second_unit = goods_list.cus_goods_tariff_id.second_unit
                goods_list.supervision_condition = goods_list.cus_goods_tariff_id.supervision_condition

    duty_mode_id = fields.Many2one(comodel_name="basedata.cus_duty_mode", string="Duty Mode", )  # 征免方式
    ManualNo = fields.Char(string="Manual No")  # 备案号 / 账册号
    ManualSN = fields.Char(string="Manual SN")  # 备案序号

    state = fields.Selection(selection=[('draft', 'Draft'),    # 草稿
                                        ('submitted', 'Submitted'),  # 提交 待审核
                                        ('refused', 'Refused'),  # 审核不通过
                                        ('approve', 'approved')  # 通过审核
                                        ], string='status', readonly=True, default='draft')

    customs_declaration_id = fields.Many2one(comodel_name="customs_center.customs_dec",
                                         inverse_name="cus_goods_tariff_id", string="customs declaration id")  # 冗余字段 用于判断报关历史商品是否已报关


    # 合规商品
    @api.multi
    @api.depends('cus_goods_code', 'goods_name','cus_goods_tariff_no', 'goods_model')
    def name_get(self):
        result = []
        for record in self:
            # 判断一下cus_goods_tariff_no字段是否有值
            cus_no = record.cus_goods_tariff_no if record.cus_goods_tariff_no else ''
            result.append(
                (record.id, u"%s %s %s %s" % (record.cus_goods_code, record.goods_name, cus_no, record.goods_model))
            )
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """重写模型name字段搜索方法"""
        args = args or []
        if not (name == '' and operator == 'ilike'):
            args += ['|', '|', ('cus_goods_code', operator, name), ('goods_name', operator, name),
                     ('cus_goods_tariff_no', operator, name)]

        return super(GoodsClassification, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )






    # @api.model
    # def create(self, vals):
    #     """创建归类的时候 判断该商品有无关联报关单 有则说明是历史上报商品 需要修改原商品状态 为已归类"""
    #     for goods_cls_list in self:
    #         if goods_cls_list.customs_declaration_id and goods_cls_list.state == 'approve':
    #             classify_status = self.env['customs_center.cus_goods_list'].search([('customs_declaration_id', '=', goods_cls_list.customs_declaration_id.id)]).update({'classify_status': 'yes'})
    #     result = super(GoodsClassification, self).create(vals)
    #     return result

    @api.multi
    def submit_review_btn(self):
        """ 商品归类信息提交审核 按钮"""
        self.update({'state': 'submitted'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类审核已提交, 请耐心等待管理员审核 ！<br/>") % (goods_cls_list.cus_goods_tariff_id.Code_ts))
            goods_cls_list.message_post(body=body)

    @api.multi
    def re_submit_review_btn(self):
        """ 商品归类信息 重新提交审核 按钮"""
        self.update({'state': 'submitted'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类审核已重新提交, 请耐心等待管理员审核 ！<br/>") % (goods_cls_list.cus_goods_tariff_id.Code_ts))
            goods_cls_list.message_post(body=body)


    @api.multi
    def already_submit_review_btn(self):
        """ 商品归类信息已提交审核 显示按钮"""
        pass

    @api.multi
    def already_reviewed_btn(self):
        """ 商品归类信息 审核通过 按钮"""
        self.update({'state': 'approve'})
        for goods_cls_list in self:
            if goods_cls_list.customs_declaration_id:
                classify_status = self.env['customs_center.cus_goods_list'].search(
                    [('customs_declaration_id', '=', goods_cls_list.customs_declaration_id.id)]).update(
                    {'classify_status': 'yes'})
            body = (_("商品编号：%s 归类，已审核通过！<br/>") % (goods_cls_list.cus_goods_tariff_id.Code_ts))
            goods_cls_list.message_post(body=body)

    @api.multi
    def refused_reviewed_btn(self):
        """ 商品归类信息 审核拒绝 按钮"""
        self.update({'state': 'refused'})
        for goods_cls_list in self:
            body = (_("商品编号：%s 归类，未审核通过！<br/>") % (goods_cls_list.cus_goods_tariff_id.Code_ts))
            goods_cls_list.message_post(body=body)




