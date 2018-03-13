# -*- coding: utf-8 -*-
{
    'name': u"海关参数",

    'summary': u"""
       海关参数，完全独立的模块 
        """,

    'description': u"""
        hs编码、申报要素、国家地区、商品单位、币种和报关单中的运输方式、
        免征性质、成交方式、装运港、进出口岸、监管方式、境内目的地、包装方式。
    """,

    'author': u"慧泽商通",
    'website': "http://saas.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/country.xml',
        'views/currency.xml',
        'views/customs.xml',
        'views/cut_mode.xml',
        'views/dec_license_doc_type.xml',
        'views/declare_element.xml',
        'views/duty_mode.xml',
        'views/entry_type.xml',
        'views/filing_bill_type.xml',
        'views/goods_tariff.xml',
        'views/packing.xml',
        'views/port.xml',
        'views/region.xml',
        'views/trade_mode.xml',
        'views/trade_terms.xml',
        'views/transport_mode.xml',
        'views/unit.xml',
        'views/menu.xml'
    ],
}