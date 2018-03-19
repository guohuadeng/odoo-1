{
    'name': 'Drag & Drop Multiple Files',
    'version': '2.0',
    'category': 'all',
    'description': 'Drag & Drop Multiple Files',
    'summary': 'Drag & Drop Multiple Files',
    'author': 'hexcode',
    'website': 'www.hexcode.it',
    'support': 'federico@hexcode.it',
    'depends': [
        'base', 'product'
    ],
    'data': [
        'views/import_widget.xml',
    ],
    'qweb': [
        'static/src/xml/multiwidget_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'price': 49,
    'currency': 'EUR',
    'images': ['images/main_screenshot.png'],
}
