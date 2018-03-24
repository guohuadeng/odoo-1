# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import Warning
import binascii,logging
import tempfile
from tempfile import TemporaryFile
from odoo.exceptions import UserError, ValidationError

try:
    import xlrd
except ImportError:
    _logger = logging.getLogger(__name__)
    _logger.error('Cannot `import xlrd`.')


class import_customs_dec_goods_list_wizard(models.TransientModel):
    _name = 'import.customs_dec.goods_list.wizard'

    goods_list_file = fields.Binary(string="Select File")

    @api.multi
    def import_goods_list(self):
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.goods_list_file))
        fp.seek(0)
        values = {}
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        for row_no in range(sheet.nrows):
            val = {}
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(
                    map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                        sheet.row(row_no)))
                values.update({
                    'cust_goods_code': str(line[0]),  # 客户料号
                    'ManualSN': line[1],  # 备案序号
                    'cus_goods_tariff': line[2],  # 商品编号
                    'goods_name': line[3],  # 商品名称
                    'goods_model': line[4],  # 规格型号
                    'deal_qty': line[5],  # 成交数量
                    'deal_unit_price': line[6],  # 成交单价
                    'deal_unit': line[7],  # 成交单位
                    'currency': line[8],  # 币制
                    'first_qty': line[9],  # 法定数量
                    'second_qty': line[10],  # 第二数量
                    'origin_country': line[11],  # 原产国
                    'destination_country': line[12],  # 目的国
                    'duty_mode': line[13],  # 征免方式
                    'version_num': line[14],  # 版本号
                    'product_code': line[15],  # 货号
                })
                res = self.create_goods_list(values)
        return res

    @api.multi
    def create_goods_list(self, values):

        customs_dec_brw = self.env['customs_center.customs_dec'].browse(self._context.get('active_id'))

        goods_classification_exist_obj = self.env['customs_center.goods_classify'].search(
                 [('cust_goods_code', '=', values.get('cust_goods_code')),
                  ('business_company_id', "=", customs_dec_brw.business_company_id.id)])  #

        # 如果根据收发货人、客户料号，能从商品归类库中找到已存在的记录，则直接从归类库中调取商品名称、规格型号等信息，无需从Excel中读取
        if goods_classification_exist_obj:
            goods_classification_id = goods_classification_exist_obj.id
            ManualSN = goods_classification_exist_obj.ManualSN
            goods_name = goods_classification_exist_obj.goods_name
            goods_model = goods_classification_exist_obj.goods_model
            deal_unit_price = goods_classification_exist_obj.deal_unit_price
            deal_unit_id = goods_classification_exist_obj.deal_unit_id.id
            currency_id = goods_classification_exist_obj.currency_id.id
            origin_country_id = goods_classification_exist_obj.origin_country_id.id
            destination_country_id = goods_classification_exist_obj.destination_country_id.id
            duty_mode_id = goods_classification_exist_obj.duty_mode_id.id
        else:
            goods_classification_id=''
            ManualSN = values.get('ManualSN')
            goods_name = values.get('goods_name')
            goods_model = values.get('goods_model')
            deal_unit_price = values.get('deal_unit_price')

            deal_unit_obj = self.env['basedata.cus_unit'].search(["|",('Code', '=', values.get('deal_unit')),('NameCN', '=', values.get('deal_unit'))])

            if deal_unit_obj:
                deal_unit_id = deal_unit_obj.id
            else:
                deal_unit_id=''

            currency_obj = self.env['basedata.cus_currency'].search(["|",('Code', '=', values.get('currency')),('NameCN', '=', values.get('currency'))])
            if currency_obj:
                currency_id = currency_obj.id
            else:
                currency_id=''

            origin_country_obj = self.env['delegate_country'].search(["|",('Code', '=', values.get('origin_country')),('NameCN', '=', values.get('origin_country'))])
            if origin_country_obj:
                origin_country_id = origin_country_obj.id
            else:
                origin_country_id=''

            destination_country_obj = self.env['delegate_country'].search(["|",('Code', '=', values.get('destination_country')),('NameCN', '=', values.get('destination_country'))])
            if origin_country_obj:
                destination_country_id = destination_country_obj.id
            else:
                destination_country_id=''

            duty_mode_obj = self.env['basedata.cus_duty_mode'].search(["|",('Code', '=', values.get('duty_mode')),('NameCN', '=', values.get('duty_mode'))])
            if duty_mode_obj:
                duty_mode_id = duty_mode_obj.id
            else:
                duty_mode_id = ''

        # 成交数量、法定第一数量、第二数量、版本号、货号不从归类库调取，而是使用Excel中的值
        deal_qty = values.get('deal_qty')
        first_qty = values.get('first_qty')
        second_qty = values.get('second_qty')
        version_num = values.get('version_num')
        product_code = values.get('product_code')

        self.env['customs_center.cus_goods_list'].create({
            'customs_declaration_id': customs_dec_brw.id,
            'goods_classification_id': goods_classification_id,
            'ManualSN': ManualSN,
            'goods_name': goods_name,
            'goods_model': goods_model,
            'deal_qty': deal_qty,
            'deal_unit_price': deal_unit_price,
            'deal_unit_id': deal_unit_id,
            'currency_id':currency_id,
            'first_qty': first_qty,
            'second_qty': second_qty,
            'origin_country_id':origin_country_id,
            'destination_country_id':destination_country_id,
            'duty_mode_id': duty_mode_id,
            'version_num': version_num,
            'product_code': product_code
        })

        return True
