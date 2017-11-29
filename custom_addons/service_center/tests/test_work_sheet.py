# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class WorkSheetTestCase(TransactionCase):
    """工作单测试用例"""


    def setUp(self):
        super(WorkSheetTestCase, self).setUp()
        group_user = self.env.ref('base.group_user')
        self.user = self.env['res.users'].create({
            'name': 'Customs officers A',
            'login': 'user',
            'email': 'c.o.a@example.com',
            'signature': '--\nMark',
            'groups_id': [(6, 0, [group_user.id])]
        })
        work_sheet_model = self.env['work_sheet'].sudo(
            self.user.id
        )
        self.work_sheet_model = work_sheet_model
        self.customer_id = self.ref('service_center.work_sheet_partner_1')
        self.settlement_id = self.ref('service_center.work_sheet_partner_2')

        self.work_sheet_1 = self.work_sheet_model.\
            with_context({'default_business_type': self.ref('basedata.business_type_for_sea_import')}).create({
                'customer': self.customer_id,
                'settlement_object': self.settlement_id,
                'business_type': self.ref('basedata.business_type_for_sea_import')
        })

    def test_name_rule(self):
        """测试命名规则是否正确"""
        self.assertEqual(len(self.work_sheet_1.name), 10, 'The length of work sheet name error')
        self.assertEqual(self.work_sheet_1.name[0:2], 'SI', 'The business type of work sheet error')
        self.assertTrue(self.work_sheet_1.name[2:].isdigit(), 'The datatime of work sheet name is wrong')

    def test_check_hs_code(self):
        """测试hs_code的长度限制"""
        with self.assertRaises(ValidationError) as e:
            self.work_sheet_1.hs_code = '12345'
        self.assertIn('HS code', str(e.exception), 'The check length of HS code does not work!')
