# -*- coding: utf-8 -*-
{
    'name': "cus_args",# 通关参数
    'summary': "cus_args",# 通关参数
    'description': u"包括报关基础参数、商品税则库数据、企业库数据,数据与通关参数中心同步",
    'author': "aeotrade",
    'website': "http://saas.aeotrade.com",
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/country_view.xml',
        'views/currency_view.xml',
        'views/cus_register_company_view.xml',
        'views/customs_view.xml',
        'views/cut_mode_view.xml',
        'views/dec_license_doc_type_view.xml',
        'views/duty_mode_view.xml',
        'views/entry_type_view.xml',
        'views/filing_bill_type_view.xml',
        'views/goods_declare_element_view.xml',
        'views/goods_tariff_view.xml',
        'views/internal_district_view.xml',
        'views/port_view.xml',
        'views/trade_mode_view.xml',
        'views/trade_terms_view.xml',
        'views/trade_mode_view.xml',
        'views/transport_mode_view.xml',
        'views/unit_view.xml',
        'views/wrap_type_view.xml',
        'views/menu.xml',

    ],
}
