{
    'name': 'yubin随附单据拖拽上传 ',
    'version': '1.0',
    'category': 'all',
    'description': '随附单据拖拽上传',
    'summary': '随附单据拖拽上传',
    'author': 'ouyubin@aeotrade.com',
    'website': 'www.aeotrade.com',
    'support': 'ouyubin@aeotrade.com',
    'depends': [
        'base',
        'ir_attachment_extend',
        'muk_web_preview',

    ],
    'data': [
        'views/import_widget.xml',
    ],
    'qweb': [
        'static/src/xml/multiwidget_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'images': ['images/main_screenshot.png'],
}
