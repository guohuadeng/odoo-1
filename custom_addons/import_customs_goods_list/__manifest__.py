# -*- coding: utf-8 -*-
# Excel导入通关商品列表(包括通关清单及报关单商品列表)
{
    'name': 'Excel导入通关商品',
    'version': '10.0.0.0',
    'summary': 'Excel导入通关商品(包括通关清单及报关单中的商品列表)',
    'description': "",
    'author': 'ouyubin@aeotrade.com',
    'depends': ['base','customs_center','basedata'],
    'data': [
        'import_customs_order_goods_list_view.xml',
        'import_customs_dec_goods_list_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    "images": ['static/description/Banner.png'],
}