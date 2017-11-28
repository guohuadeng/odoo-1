# -*- coding: utf-8 -*-
{
    'name': u"关务",

    'summary': u"""
        在服务中心的工作单中加入报关、报检功能
        """,

    'description': u"""
        1. 创建原始清单模型
        2. 将原始清单模型与工作单进行衔接
        3. 与慧贸1.0系统进行接口对接
    """,

    'author': u"周杨 王志强",
    'website': "http://www.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['service_center'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/clearance_draft.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}