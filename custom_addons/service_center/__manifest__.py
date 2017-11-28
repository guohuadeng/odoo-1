# -*- coding: utf-8 -*-
{
    'name': u"服务中心",

    'summary': u"""
        在客服处理工作单
       """,

    'description': u"""
        建立工作单模型，可以直接从工作单中生成销售订单。工作单模型里有基本信息、货物信息、发运信息、服务类型和委托商品信息。
    """,

    'author': u"周杨",
    'website': "http://www.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['basedata', 'mail', 'sale_contract'],

    # always loaded
    'data': [
        'data/decimal_precision_data.xml',
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/current_state.xml',
        'views/work_sheet_views.xml',
        'views/service_center_dashboard.xml',
        'views/contract.xml',
        'views/menu.xml',
        'reports/work_sheet_report.xml',
        'reports/work_sheet_report_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ]
}