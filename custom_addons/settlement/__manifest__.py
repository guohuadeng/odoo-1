# -*- coding: utf-8 -*-
{
    'name': u"费用结算",

    'summary': u"""
        费用结算相关,包括应收费用，应付费用
        """,

    'description': u"""
        费用结算相关,包括应收费用，应付费用
    """,

    'author': u"周杨 王志强",
    'website': "http://www.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'mail', 'service_center'],

    # always loaded
    'data': [
        "data/ir_module_category.xml",
        'security/settlement_security.xml',
        'security/ir.model.access.csv',
        'reports/settlement_report.xml',
        'views/about_pay_status_wizard_views/confirm_payment_btn_wizard_views.xml',
        'views/about_pay_status_wizard_views/pay_apply_pass_audit_btn_wizard_views.xml',
        'views/about_pay_status_wizard_views/pay_apply_submit_audit_btn_wizard_views.xml',
        'views/about_bill_status_wizard_views/account_write_off_btn_views.xml',
        # 'views/about_bill_status_wizard_views/account_invoice_make_out_bit_views.xml',
        # 'views/about_bill_status_wizard_views/account_check_btn_wizard_views.xml',
        # 'views/about_bill_status_wizard_views/account_review_btn_wizard_views.xml',
        'views/about_bill_status_wizard_views/account_checked_abnormal_wizard_views.xml',
        'views/about_bill_status_wizard_views/account_refused_btn_wizard_views.xml',
        'views/pending_review_application.xml',
        'views/expense_receivable_views.xml',
        'views/customer_bill_views.xml',
        'views/expense_payable_views.xml',
        'views/payment_application_sheet_views.xml',
        'views/customer_bill_type_views.xml',
        'views/expense_settlement_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}