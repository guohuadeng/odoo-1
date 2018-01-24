# -*- coding: utf-8 -*-
{
    'name': "purchase_extend",

    'summary': """
        extend purchase module for customs system 
        """,

    'description': u"""
        1. 加入报关相关字段\n
        2. 修改询价单命名规则\n
        3. 加入新的关注者\n
    """,

    'author': u"周杨",
    'website': "http://saas.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'basedata', 'crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase.xml',
        'views/res_config.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}