# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': u'合同管理',
    'version': '1.0',
    'summary': u'在原有销售模块中增加合同管理',
    'description': u'在原有销售模块中增加合同管理',
    'category': '',
    'author': u'王志强， 周杨',
    'website': '',
    'license': '',
    'depends': ['sale'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/contract_manage.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
}
