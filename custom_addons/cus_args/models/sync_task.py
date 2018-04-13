# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests


class SyncTask(models.Model):
    _name = 'cus_args.sync_task'
    _rec_name = 'sync_model'
    _description = 'Data Sync Task'

    scheme = fields.Selection(string="Scheme", selection=[('http', 'Http'), ('https', 'Https'), ], required=True, )
    base_url = fields.Char(string="Source URL", required=True, )
    data_uri = fields.Char(string="URI", required=True, )
    sync_model = fields.Char(string="Model", required=True, )
    port = fields.Char(string="Port", required=True, )


    @api.multi
    def sync_data(self):
        """同步数据"""
        print(u"开始同步数据!")
        if self.sync_model not in ['cus_args.goods_tariff', 'cus_args.goods_declare_element', 'cus_args.register_company']:
            self.general_data()
        elif self.sync_model in ['cus_args.goods_tariff']:
            self.goods_tariff_data()
        elif self.sync_model in ['cus_args.goods_declare_element']:
            self.declare_element_data()
        elif self.sync_model in ['cus_args.register_company']:
            self.register_company_data()

        return True

    @api.multi
    def general_data(self):
        records = self.env[self.sync_model].search([])
        if not records:
            codes = {}
        else:
            codes = records.mapped(lambda r: {r.code: r.id})
            codes_dic = {}
            for dic in codes:
                codes_dic.update(dic)
            codes = codes_dic
        print(codes)
        source_url = self.scheme + '://' + self.base_url + ':' + self.port + '/' + self.data_uri
        print(source_url)
        rest_codes = set()
        while(source_url):
            response = requests.get(source_url)
            print('response code: {}'.format(response.status_code))
            response.raise_for_status()
            response = response.json()
            source_url = response.get('next')
            for item in response.get('results'):
                code = item.get('code')
                rest_codes.add(code)
                if code not in codes:
                    self.env[self.sync_model].create({'code': code, 'name_cn': item.get('name_cn')})
                else:
                    self.env[self.sync_model].browse(codes[code]).write({'name_cn': item.get('name_cn')})

        rm_codes = set(codes.keys())- rest_codes
        if rm_codes:
            rm_obj_ids = [codes[obj_id] for obj_id in rm_codes]
            rm_objs = self.env[self.sync_model].search([('id', 'in', rm_obj_ids)])
            rm_objs.unlink()

    @api.multi
    def goods_tariff_data(self):
        records = self.env[self.sync_model].search([])
        if not records:
            codes = {}
        else:
            codes = records.mapped(lambda r: {r.code_ts: r.id})
            codes_dic = {}
            for dic in codes:
                codes_dic.update(dic)
            codes = codes_dic
        print(codes)
        source_url = self.scheme + '://' + self.base_url + ':' + self.port + '/' + self.data_uri
        print(source_url)
        rest_codes = set()
        while(source_url):
            response = requests.get(source_url)
            print('response code: {}'.format(response.status_code))
            response.raise_for_status()
            response = response.json()
            source_url = response.get('next')
            for item in response.get('results'):
                code = item.get('code_ts')
                rest_codes.add(code)
                if code not in codes:
                    self.env[self.sync_model].create({
                        'code_ts': code,
                        'code_t': item.get('code_t'),
                        'code_s': item.get('code_s'),
                        'first_unit_id': self.env['cus_args.unit'].
                            search([('code', '=', item.get('first_unit'))])[0].id if item.get('first_unit') else False,
                        'second_unit_id': self.env['cus_args.unit'].
                            search([('code', '=', item.get('second_unit'))])[0].id if item.get('second_unit') else False,
                        'name_cn': item.get('name_cn'),
                        'supervision_condition': item.get('supervision_condition')
                    })
                else:
                    self.env[self.sync_model].browse(codes[code]).write({
                        'name_cn': item.get('name_cn'),
                        'code_t': item.get('code_t'),
                        'code_s': item.get('code_s'),
                        'first_unit_id': self.env['cus_args.unit'].
                            search([('code', '=', item.get('first_unit'))])[0].id if item.get('first_unit') else False,
                        'second_unit_id': self.env['cus_args.unit'].
                            search([('code', '=', item.get('second_unit'))])[0].id if item.get(
                            'second_unit') else False,
                        'supervision_condition': item.get('supervision_condition')
                    })

        rm_codes = set(codes.keys())- rest_codes
        if rm_codes:
            rm_obj_ids = [codes[obj_id] for obj_id in rm_codes]
            rm_objs = self.env[self.sync_model].search([('id', 'in', rm_obj_ids)])
            rm_objs.unlink()

    @api.multi
    def declare_element_data(self):
        records = self.env[self.sync_model].search([])
        records.unlink()
        source_url = self.scheme + '://' + self.base_url + ':' + self.port + '/' + self.data_uri
        print(source_url)
        while(source_url):
            response = requests.get(source_url)
            print('response code: {}'.format(response.status_code))
            response.raise_for_status()
            response = response.json()
            source_url = response.get('next')
            for item in response.get('results'):
                self.env[self.sync_model].create({
                    'goods_tariff_hs_code': item['cus_goods_tariff_id'],
                    'name_cn': item.get('name'),
                    'sequence': item.get('sequence')
                })

    @api.multi
    def register_company_data(self):
        records = self.env[self.sync_model].search([])
        if not records:
            codes = {}
        else:
            codes = records.mapped(lambda r: {r.register_code: r.id})
            codes_dic = {}
            for dic in codes:
                codes_dic.update(dic)
            codes = codes_dic
        print(codes)
        source_url = self.scheme + '://' + self.base_url + ':' + self.port + '/' + self.data_uri
        print(source_url)
        rest_codes = set()
        while(source_url):
            response = requests.get(source_url)
            print('response code: {}'.format(response.status_code))
            response.raise_for_status()
            response = response.json()
            source_url = response.get('next')
            for item in response.get('results'):
                code = item.get('register_code')
                rest_codes.add(code)
                if code not in codes:
                    self.env[self.sync_model].create({'register_code': code,
                                                      'register_name_cn': item.get('register_name_cn'),
                                                      'unified_social_credit_code': item.get('unified_social_credit_code')})
                else:
                    self.env[self.sync_model].browse(codes[code]).write({'register_name_cn': item.get('register_name_cn'),
                                                                         'unified_social_credit_code': item.get('unified_social_credit_code')})

        rm_codes = set(codes.keys())- rest_codes
        if rm_codes:
            rm_obj_ids = [codes[obj_id] for obj_id in rm_codes]
            rm_objs = self.env[self.sync_model].search([('id', 'in', rm_obj_ids)])
            rm_objs.unlink()


