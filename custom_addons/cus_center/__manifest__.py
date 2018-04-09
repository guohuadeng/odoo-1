# -*- coding: utf-8 -*-
{
    'name': u"cus_center",
    'summary': u"关务中心",
    'description': u"""
        1. 创建通关清单模型、报关模型、商品列表、回执模型
        2. 生成XML报文 通过云交换发送到海关报关系统(单一窗口或QP)
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
    'depends': ['cus_args', 'service_center', 'mail', 'decimal_precision', 'web_sheet_full_width'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/cus_expenses_mark_type.xml',
        # 'data/cus_whether_mark_type.xml',
        # 'data/payment_mark_type.xml',
        # 'data/ir_sequence_data.xml',
        # 'data/parse_message.xml',
        # 'data/result_status.xml',
        # 'views/customs_center_dashboard.xml',
        'views/pending_review_goods_views.xml',
        'views/goods_classification_views.xml',
        'views/customs_declaration_view.xml',
        'views/customs_order_view.xml',
        # 'views/result_status.xml',
        # 'views/customs_receipt.xml',
        'views/setting_declaration.xml',
        'views/menu.xml',
        # 'views/template.xml',
        # 'reports/customs_dec_report.xml',
        # 'reports/customs_dec_report_template.xml',
    ],
}
