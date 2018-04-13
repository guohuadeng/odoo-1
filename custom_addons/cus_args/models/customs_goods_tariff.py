# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CusGoodsTariff(models.Model):
    """ 海关商品税则 """
    _name = 'cus_args.goods_tariff'
    _description = 'Goods Tariff Table'
    _rec_name = 'code_ts'

    code_t = fields.Char(string='Tax Regulations Code', )  # 税号
    code_s = fields.Char(string='Attach Code', )  # 附加编码
    code_ts = fields.Char(string='HS Code', required=True)  # 商品编号

    name_cn = fields.Char(string='Goods Chinese Name', size=50, required=True)  # 中文名称


    # 该商品对应的申报要素，仅用于界面显示，方便用户查询商品申报要素，不做存储
    # 例如 2916140090对应的申报要素, '0:品牌类型;1:出口享惠情况;2:成分含量;3:用途;4:丙烯酸、丙烯酸盐或酯应报明包装;5:GTIN;6:CAS;'
    # TODO(ouyubin) 考虑到性能原因，_get_declare_elements可能需要改善
    declare_elements = fields.Char(string='Goods Declare Element', compute='_get_declare_elements', store=False)  # 中文名称

    @api.multi
    def _get_declare_elements(self):
        for goods in self:
            goods.declare_elements = ''
            elements = self.env['cus_args.goods_declare_element'].search([('goods_tariff_hs_code', '=', goods.code_ts)])
            for e in elements:
                s = '%s:%s;' % (str(e.sequence), e.name_cn)
                goods.declare_elements += s

    first_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="First Unit", )  # 第一计量单位
    second_unit_id = fields.Many2one(comodel_name="cus_args.unit", string="Second Unit", )  # 第二计量单位

    # 最惠国进口税率（也叫做进口关税率_低)
    import_rate_most_favoured = fields.Float(string="Import Rate Most Favoured")

    # 普通进口税率(也叫做进口关税率_普)
    import_rate_general = fields.Float(string="Import Rate General")

    # 消费税率
    tax_rate = fields.Float(string="Tax Rate")

    # 出口关税率(也叫做出口从价税税率)
    export_rate = fields.Float(string="Export Rate")

    # 增值税率
    vat_rate = fields.Float(string="Vat Rate")

    # 监管条件
    supervision_condition = fields.Char(string="Supervision Condition")

    # 商品描述
    goods_description = fields.Char(string="Goods Description")


class DeclareElement(models.Model):
    """商品申报要素"""
    _name = 'cus_args.goods_declare_element'
    _description = 'Goods Declare Element'
    _rec_name = 'name_cn'

    # goods_tariff_id = fields.Many2one(comodel_name="cus_args.goods_tariff", string="HS Code", required=True, ) 不使用id的方式关联，不便于数据维护

    goods_tariff_hs_code = fields.Char(string='HS Code', required=True)
    name_cn = fields.Char('Element Name', size=50, required=True)  # 要素名
    sequence = fields.Integer('Num', required=True)  # 序号
