# -*- coding: utf-8 -*-
{
    'name': u"关务(单一窗口)",

    'summary': u"""
        走单一窗口通道的报关模块
        """,

    'description': u"""
        1. 创建原始清单模型、报关模型、商品列表、回执模型
        2. 将原始清单模型与工作单进行衔接
        3. 生成XML报文 通过云交换发送到单一窗口
        4. 安装之前需要先更新基础数据模块
    """,

    'author': u"周杨 王志强",
    'website': "http://saas.aeotrade.com",

    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['service_center','basedata'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/parse_message.xml',
        'data/result_status.xml',
        'views/pending_review_goods_views.xml',
        'views/customs_dec_attachs.xml',
        'views/goods_classification_views.xml',
        'views/pending_classified_goods_views.xml',
        'views/customs_declaration.xml',
        'views/customs_order.xml',
        'views/result_status.xml',
        'views/setting_declaration.xml',
        'views/menu.xml',
        'views/template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}