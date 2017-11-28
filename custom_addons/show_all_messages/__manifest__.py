
# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'Show All Messages',
    'summary': '',
    'version': '1.0',
    'category': 'Extra Tools',
    'author': 'Hugh',
	'price': 19.99,
	'currency': 'EUR',
    'website': 'http://cssinco.com',
	'images': ['images/main_screenshot.png'],
    'depends': ['base', 'mail'],
    'data': [
        'views/template.xml',
    ],
    'installable': True,
    'qweb': [
        'static/src/xml/base.xml',
    ],
    'application': True,
}


