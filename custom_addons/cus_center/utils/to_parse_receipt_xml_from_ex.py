# -*- coding: utf-8  -*-

import os, shutil
from odoo.tools import config
from lxml import etree
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

# MAIN_PATH = '/home/odoo/Desktop/ParallelsSharedFolders/Home'  # 欧玉斌的本地目录
# MAIN_PATH = '/home/odoo/odooshare'  #王志强的本地目录
MAIN_PATH = '/mnt/xml_data'  # test测试环境地址 195.186

RECV_XML_BASE_PATH = config.options.get('parse_rec_ex_to_wly',
                                        MAIN_PATH + '/about_wly_xml_data/post_ex_client/rec_ex_to_wly')
ERROR_XML_BASE_PATH = config.options.get('parse_rec_error_xml_path',
                                         MAIN_PATH + '/about_wly_xml_data/post_ex_client/error_xml_message')
BAKUP_XML_BASE_PATH = config.options.get('backup_rec_xml_path',
                                         MAIN_PATH + '/about_wly_xml_data/post_ex_client/backup_rec_xml')

DEBUG = False  # debug=true时，为了调试方便，不执行将报文移动错误或备份文件夹的操作


def check_and_mkdir(*path):
    for p in path:
        if not os.path.exists(p):
            os.mkdir(p)


def parse_receipt_xml(self):
    """解析从交换发送给物流云的回执，解析入库后，备份到相应路径"""

    customs_dec_model_dic = self.env['cus_center.customs_dec'].default_get(['dec_company_customs_code'])  # 获取报关单模型对象
    company_xml_parse_path = customs_dec_model_dic.get('dec_company_customs_code')  # 获取配置信息中的 申报单位海关编码 作为解析路径

    recv_path = os.path.join(RECV_XML_BASE_PATH, company_xml_parse_path.encode('utf-8'))
    error_path = os.path.join(ERROR_XML_BASE_PATH, company_xml_parse_path.encode('utf-8'))
    bakup_path = os.path.join(BAKUP_XML_BASE_PATH, company_xml_parse_path.encode('utf-8'))

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
                business_dic['DEC_RESULT'] = {}
                for child in result_node.iterchildren():
                    if child.text:
                        business_dic['DEC_RESULT'][child.tag] = child.text
                        business_dic['RESULT_INFO'] = result_info_node.text if result_info_node.text else ''
            else:
                _logger.error(u'Find error format xml message: %s' % xml_message.decode('utf-8'))

                if not DEBUG:
                    shutil.copy2(xml_message, error_path)
                    os.remove(xml_message)
                continue

        # 根据报文中客户端代码找到关联的报关单
        rep_client_no = response_dic.get('ClientSeqNo')
        bus_client_no = business_dic['DEC_RESULT'].get('CLIENTSEQ_NO') if business_dic.get('DEC_RESULT') else None

        # 报关单对象
        dec_sheets = self.env['cus_center.customs_dec'].search(
            [('client_seq_no', '=', rep_client_no or bus_client_no)])

        if not dec_sheets:
            _logger.error(
                u'{} Can\'t find related declaration sheet according to ClientSeqNo {}'
                    .format(xml_message.decode('utf-8'), rep_client_no or bus_client_no))

            if not DEBUG:
                shutil.copy2(xml_message, error_path)
                os.remove(xml_message)

            continue
        dec_sheet = dec_sheets[0]

        # 如果还没有回填相关字段
        if not dec_sheet.dec_seq_no:
            dec_sheet.dec_seq_no = response_dic.get('SeqNo') or business_dic.get('SEQ_NO')  # 回填统一编号
        # if not dec_sheet.entry_id:
        #     dec_sheet.entry_id = business_dic.get('ENTRY_ID', None)  # 根据回执 回填海关编号
        # if not dec_sheet.dec_date:
        #     dec_date_str = business_dic.get('D_DATE', None)
        #     dec_date = datetime.strptime(dec_date_str,'%Y%m%d')  # 将字符串日期 转换为日期格式
        #     dec_sheet.dec_date = dec_date  # 回填申报日期
        if response_dic:
            resp_code = response_dic.get('ResponseCode')
            status = self.env['cus_center.dec_res_status'].search([('code', '=', resp_code)])
            print(response_dic)
            message = response_dic['ErrorMessage']
        else:
            resp_code = business_dic['DEC_RESULT']['CHANNEL']
            status = self.env['cus_center.dec_res_status'].search([('code', '=', resp_code)])
            message = business_dic['RESULT_INFO']
            dec_sheet.entry_id = business_dic['DEC_RESULT'].get('ENTRY_ID', None)
            dec_date_str = business_dic['DEC_RESULT'].get('D_DATE', None)
            if dec_date_str:
                dec_date = datetime.strptime(dec_date_str, '%Y%m%d')  # 将字符串日期 转换为日期格式
                dec_sheet.dec_date = dec_date  # 回填申报日期

        receipt_dic = {
            'status_id': status[0].id if status else None,
            'message': message,
            'customs_dec_id': dec_sheet.id
        }
        try:
            self.env['cus_center.dec_result'].create(receipt_dic)

            # 如果该票报关单 业务回执状态为：报关单放行 则将该报关单下的商品 自动归类
            # 注意，已经进行过归类的商品不需要重新归类（如果该商品有客户料号（说明选的时候就是来自于归类库），或者归类库中已有同收发货人、同商品名称、同规格型号的商品，说明已经进行过归类，不再自动归类）
            if status[0].code == 'P':  # 报关单放行
                self.create_classify_goods(dec_sheet)


        except Exception, error_info:
            _logger.error(u'{} {}'.format(xml_message.decode('utf-8'), str(error_info).decode('utf-8')))

            if not DEBUG:
                shutil.copy2(xml_message, error_path)
                os.remove(xml_message)

            continue
        else:
            if not DEBUG:
                shutil.copy2(xml_message, bakup_path)
                os.remove(xml_message)

                _logger.info(u'Had parsed the xml message %s' % xml_message.decode('utf-8'))
