# –*– coding: utf–8 –*–
{
    'name': 'customer_extend',
    'description': '扩展客户信息界面(考虑后续做成一个通用模块，把原来在博越销售扩展模块加的客户信息字段，移到此模块中)',
    'author': 'ou',
    'depends': ['base','sale','basedata'],
    'data': [
        "views/customer_seal.xml"
        ],
    'application': True,

}