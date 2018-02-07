# -*- coding: utf-8 -*-
{
    'name': u"博越销售扩展模块",

    'summary': u"""
        扩展销售模块，满足博越的业务需求
        """,

    'description': u"""
        扩展的功能：
        1.引用基础数据中的各个通关信息
        2.
    """,

    'author': u"周杨 王志强",
    'website': "http://www.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['basedata', 'sale_contract', 'purchase', 'hr', 'service_center', 'website_quote'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/contract_wizard.xml',
        'views/sale_info_kanban.xml',
        'views/order.xml',
        # 'views/quotes.xml',
        # 'report/quote_report.xml',
        # 'data/mail_template_data.xml',
        'views/certificate_manage_views.xml',
        'views/sale_customer_info.xml',
        'views/incoterm.xml',
        'views/template.xml',
        'views/order_quote_view.xml',
        'data/delete_order_menu.xml',
    ],
    'qweb': [
        'static/src/xml/widget.xml',
    ],
    # only loaded in demonstr   ation mode
    'demo': [
        # 'demo/demo.xml',
    ],
}