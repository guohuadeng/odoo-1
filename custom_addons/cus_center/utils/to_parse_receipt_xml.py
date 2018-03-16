# -*- coding: utf-8  -*-

import os, shutil
from odoo.tools import config
from lxml import etree
from datetime import datetime

RECV_XML_BASE_PATH = config.options.get('parse_rec_ex_to_wly', '/mnt/odooshare/about_wly_xml_data/post_ex_client/rec_ex_to_wly')
ERROR_XML_BASE_PATH = config.options.get('parse_rec_error_xml_path','/mnt/odooshare/about_wly_xml_data/post_ex_client/error_xml_message')
BAKUP_XML_BASE_PATH = config.options.get('backup_rec_xml_path','/mnt/odooshare/about_wly_xml_data/post_ex_client/backup_rec_xml')


def check_and_mkdir(*path):
    for p in path:
        if not os.path.exists(p):
            os.mkdir(p)


def parse_receipt_message_xml(self, company_path, _logger):
    """解析回执报文"""
    recv_path = os.path.join(RECV_XML_BASE_PATH, company_path)
    error_path = os.path.join(ERROR_XML_BASE_PATH, company_path)
    bakup_path = os.path.join(BAKUP_XML_BASE_PATH, company_path)

    # 检查并生成相应的目录
    check_and_mkdir(recv_path, error_path, bakup_path)
    files = os.listdir(recv_path)
    files = [filename for filename in files if filename.endswith('.xml')]
    if not files:
        return True
    files = [os.path.join(recv_path, i) for i in files]

        # 读文件，用lxml解析报文
    for xml_message in files:
        with open(xml_message, 'r') as f:
            tree = etree.parse(f)
            root = tree.getroot()
            response_dic = {}
            business_dic = {}
            root_name = etree.QName(root).localname
            if root_name == u'DecImportResponse':
                for child in root.iterchildren():
                    key = etree.QName(child).localname
                    value = child.text
                    response_dic[key] = value
            elif root_name == u'DEC_DATA':
                result_node = root.find('DEC_RESULT')
                result_info_node = root.find('RESULT_INFO')
                business_dic['RESULT_INFO'] = result_info_node.text if result_info_node.text else ''
                business_dic['DEC_RESULT'] = {}
                for child in result_node.iterchildren():
                    if child.text:
                        business_dic['DEC_RESULT'][child.tag] = child.text
            else:
                _logger.error(u'Find error format xml message: %s' % xml_message.decode('utf-8'))
                shutil.move(xml_message, error_path)
                continue
        # 根据报文中客户端代码找到关联的报关单
        rep_client_no = response_dic.get('ClientSeqNo')
        bus_client_no = business_dic['DEC_RESULT'].get('CLIENTSEQ_NO') if business_dic.get('DEC_RESULT') else None

        dec_sheets = self.env['customs_center.customs_dec'].search(
            [('client_seq_no', '=', rep_client_no or bus_client_no)])

        if not dec_sheets:
            _logger.error(
                u'{} Can\'t find related declaration sheet according to ClientSeqNo {}'
                    .format(xml_message.decode('utf-8'), rep_client_no or bus_client_no))
            shutil.move(xml_message, error_path)
            continue
        dec_sheet = dec_sheets[0]
        if not dec_sheet.dec_seq_no:
            dec_sheet.dec_seq_no = response_dic.get('SeqNo') or business_dic.get('SEQ_NO')  # 回填统一编号

        if response_dic:
            resp_code = response_dic.get('ResponseCode')
            status = self.env['customs_center.dec_res_status'].search([('code', '=', resp_code)])
            message = response_dic['ErrorMessage']
        else:
            resp_code = business_dic['DEC_RESULT']['CHANNEL']
            status = self.env['customs_center.dec_res_status'].search([('code', '=', resp_code)])
            message = business_dic['RESULT_INFO']
            dec_sheet.entry_id = business_dic['DEC_RESULT'].get('ENTRY_ID', None)
            dec_date_str = business_dic['DEC_RESULT'].get('D_DATE', None)
            if dec_date_str:
                dec_date = datetime.strptime(dec_date_str, '%Y%m%d')  # 将字符串日期 转换为日期格式
                dec_sheet.dec_date = dec_date  # 回填申报日期

        if not status:
            _logger.error(
                u'%s Can\'t find related status obj according to response code' % xml_message.decode('utf-8'))
            shutil.move(xml_message, error_path)
            continue
        receipt_dic = {
            'status_id': status[0].id,
            'message': message,
            'customs_declaration_id': dec_sheet.id
        }
        try:
            self.env['customs_center.dec_result'].create(receipt_dic)
            dec_sheet.cus_dec_rec_state = status[0].name if status[0].name else None # 更新 报关单模型的回执状态字段
        except Exception, error_info:
            _logger.error(u'{} {}'.format(xml_message.decode('utf-8'), str(error_info).decode('utf-8')))
            shutil.move(xml_message, error_path)
            continue
        else:
            shutil.move(xml_message, bakup_path)
            _logger.info(u'Had parsed the xml message %s' % xml_message.decode('utf-8'))

