# -*- coding: utf-8 -*-
{
    'name': 'Project Management Dashboard',
    'version': '1.0',
    'price': 15,
    'currency': 'EUR',
    'author': 'Zadsolutions, Ahmed Hefni',
    'category': 'Project Management',
    'website': "http://zadsolutions.com",
    'summary': """""",
    'depends': [
        'project','hr_timesheet','project_issue_sheet'
    ],
    'data': [
        "views/templates.xml",
        "views/project_management_dashboard_view.xml"
    ],
    'images': [
        'static/description/icon.png',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
}
