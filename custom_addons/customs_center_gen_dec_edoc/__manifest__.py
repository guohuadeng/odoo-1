# –*– coding: utf–8 –*–
{
    'name': 'customs_center_gen_dec_edoc',
    'description': '关务中心-报关单-添加一键自动生成随附单据功能',
    'author': 'ouyubin@aeotrade.com',
    'depends': ['base','customs_center','customer_extend'],
    'data': [
        "views/customs_declaration_extend_gen_dec_edoc.xml",
        "reports/customs_dec_edoc_report.xml",
        "reports/customs_dec_edoc_report_template.xml",
        ],
    'application': True,

}