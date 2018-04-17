# -*- coding: utf-8 -*-
{
    'name':u'云合規',
    'summary':u'货主版云合规：合规&清单',
    'description':u'将合规和通关清单调整给货主使用',
    'author':u'倪港钧——nigangjun@aeotrade.com',
    'version': '0.1',
    'depends':[
        'cus_center',
    ],
    'website': "http://saas.aeotrade.com",
    'data':[
        'data/ir_sequence_data.xml',
        'views/custom_compliance.xml',
        'views/custom_compliance_review.xml',
        'views/custom_model.xml',
        'views/custom_goods_list.xml',
        'views/compliance_config.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}