# -*- coding: utf-8 -*-
{
    'name': 'Sale No Auto Subscribe',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'No auto followers in sales orders (extension to the app No Auto Subscription)',
    'description': '''
The app goal is to extend the module No Auto Subscription ('compoze_no_auto_subscribe') in order not to automatically subscribe clients and do not send excess notifications.
* By default receivers are not subscribed to sales orders if they received a notification
* Just flag a check box in an email composer to force automatic subscription
    ''',
    'auto_install': False,
    'application': True,

    'author': 'IT Libertas',
    'website': 'https://odootools.com',
    'depends': [
        'portal_sale',
        'compoze_no_auto_subscribe',
    ],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
            ],
    'qweb': [

            ],
    'js': [

            ],
    'demo': [

            ],
    'test': [

            ],
    'license': 'Other proprietary',
    'images': ['static/description/main.png'],
    'update_xml': [],
    'installable': True,
    'private_category': False,
    'external_dependencies': {
    },
}
