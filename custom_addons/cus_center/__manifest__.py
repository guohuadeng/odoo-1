# -*- coding: utf-8 -*-
{
    'name': u"关务",

    'summary': u"""
        关务模块，基础通用版
        """,

    'description': u"""
        1. 创建原始清单模型、报关模型、商品列表、回执模型
        2. 生成XML报文 通过云交换发送到单一窗口
        3. 安装之前需要先更新海关参数模块
    """,

    'author': u"周杨 王志强",
    'website': "http://saas.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['customs_args', 'mail', 'web_sheet_full_width'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
}