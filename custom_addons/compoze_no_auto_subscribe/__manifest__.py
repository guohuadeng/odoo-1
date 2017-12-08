# -*- coding: utf-8 -*-
{
    'name': 'No Auto Subscription',
    'version': '1.1',
    'category': 'Discuss',
    'summary': 'No Automatic Followers by Notifications',
    'description': '''
No Automatic Followers by Notifications
The app goal is to exclude automatic inclusion of users in followers. By default Odoo make all email receivers as objects followers. This may be dangerous in communication with external partners and may be annoying to your employees.
This app solves the issue and but leave you a tool to use automatic subscription.
* By default receivers are not subscribed to objects if they received a notification
* Just flag a check box in an email composer to force automatic subscription
* The app works for the most of objects. See the documentation to learn how apply it to other models
    ''',
    'price': '49.00',
    'currency': 'EUR',
    'auto_install': False,
    'author': 'IT Libertas',
    'website': 'https://odootools.com',
    'depends': [
        'super_mail',
    ],
    'data': [
        'data/data.xml',
        'wizard/mail_compose_message_view.xml',
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
    'application': True,
    'installable': True,
    'private_category': False,
    'external_dependencies': {
    },
}
