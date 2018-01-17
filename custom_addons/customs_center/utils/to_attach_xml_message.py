# -*- coding: utf-8  -*-
import os
import uuid
from datetime import datetime, timedelta
import lxml.etree as etree
from odoo.tools import config
from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def generate_attach_xml_to_single(self):
    """ 生成单一窗口 随附单据报文xml报文 存放到指定目录 """
    for attach in self.information_attachment_ids:
        attach_name = attach.name
        attach_data = attach.datas
        print("**************************666666666666666666******************************************")
        print(attach_data)
        if attach_name and attach_data:
            root = etree.Element("Data")
            tcs_flow201 = etree.SubElement(root, "TcsFlow201")
            tcs_user = etree.SubElement(tcs_flow201, "TcsUser")
            user_id = etree.SubElement(tcs_user, "UserId")
            tcs_flow = etree.SubElement(tcs_flow201, "TcsFlow")
            message_id = etree.SubElement(tcs_flow, "MessageId")
            bp_no = etree.SubElement(tcs_flow, "BpNo")
            action_list = etree.SubElement(tcs_flow, "ActionList")
            action_id = etree.SubElement(action_list, "ActionId")
            task_note = etree.SubElement(tcs_flow, "TaskNote")
            task_note.text = "0"
            corp_task_id = etree.SubElement(tcs_flow, "CorpTaskId")
            task_control = etree.SubElement(tcs_flow, "TaskControl")
            tcs_data = etree.SubElement(tcs_flow201, "TcsData", nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"})

            tcs_data_dic = OrderedDict()
            tcs_data_dic['FILE_NAME'] = attach_name if attach_name else None # u'随附单据名称'
            tcs_data_dic['BINARY_DATA'] = attach_data if attach_data else None  # u'PDF二进制数据'
            tcs_data_dic['AGENTCODE'] = self.declare_company_id.register_code if self.declare_company_id.register_code else None # 申报单位代码
            tcs_data_dic['AGENTNAME'] = self.declare_company_id.register_name_cn if self.declare_company_id.register_name_cn else None # u'申报单位名称'
            tcs_data_dic['OWNERCODE'] = self.input_company_id.register_code  # u'货主单位代码'
            tcs_data_dic['OWNERNAME'] = self.input_company_id.register_name_cn  # 货主单位名称
            tcs_data_dic['TRADECODE'] = self.business_company_id.register_code  # u'经营单位编号'
            tcs_data_dic['TRADENAME'] = self.business_company_id.register_name_cn  # u'经营单位名称'
            tcs_data_dic['PRE_ENTRY_ID'] = None  # u'报关单预录入号'
            tcs_data_dic['ENTRY_ID'] = None  # u'报关单号'
            tcs_data_dic['FORMAT_TYPE'] = 'US' # u'格式类型'
            tcs_data_dic['TRADE_CODE'] = self.input_company_id.register_code if self.input_company_id.register_code else None # u'企业编号'
            tcs_data_dic['MASTER_CUSTOMS_CODE'] = str(self.custom_master_id.Code)  # u'申报口岸关区代码'
            tcs_data_dic['GROUP_ID'] = None  # u'分组标识'
            tcs_data_dic['TRADE_FILE_NAME'] = attach_name if attach_name else None  # u'文件原始名称'
            tcs_data_dic['DECL_TYPE'] = 'F'  # u'上传类型'
            tcs_data_dic['DECL_TIME'] = (datetime.now()+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')   # u'上传时间'
            tcs_data_dic['DECL_CODE'] = self.ic_code if self.ic_code else None  # u'上传人员代码'   操作员IC卡号
            tcs_data_dic['DECL_NAME'] = self.oper_name if self.oper_name else None  # u'上传人员名称'
            tcs_data_dic['FILE_TYPE'] = '00000001'  # u'随附单据类型'
            tcs_data_dic['FILE_SOURCE'] = None  # u'数据来源'
            tcs_data_dic['FILE_DIGEST'] = None  # u'文件摘要'
            tcs_data_dic['SIGN_CERT'] = None  # u'证书名称'
            tcs_data_dic['FILE_SIGN'] = None  # u'外网签名'
            tcs_data_dic['OP_NOTE'] = None  # u'操作说明'

            for node in tcs_data_dic:
                _node = etree.SubElement(tcs_data, node)
                # node_list = ['PRE_ENTRY_ID', 'ENTRY_ID', 'GROUP_ID', 'FILE_SOURCE', 'FILE_DIGEST', 'SIGN_CERT','OP_NOTE']
                # if node in node_list:
                #     _node.set('xsi:nil', "True")
                value = tcs_data_dic[node]
                if value:
                    _node.text = value
            # change the root to xml file
            string = etree.tostring(root, xml_declaration=True, encoding='utf-8')
            # base_dir = config.options['xml_files_path']
            base_dir = config.options.get('xml_files_path', '/mnt/odooshare/customs_declaration_xml')

            # # 企业报关单 存放目录 前端界面配置
            # 报文生成路径 用户配置界面自定义
            company_name = str(self.cus_dec_dir)
            dec_catalog_path = os.path.join(base_dir, company_name)
            # 检查并生成相应的目录
            if not os.path.exists(dec_catalog_path):
                os.mkdir(dec_catalog_path)
            obj_dir = os.path.join(dec_catalog_path, attach_name +'$'+ (datetime.now()+timedelta(hours=8)).strftime('%Y%m%d%H%M%S') + '.xml')
            with open(obj_dir, 'w') as fp:
                fp.write(string.encode('utf8'))








    # root = etree.Element("Data")
    # tcs_flow201 = etree.SubElement(root, "TcsFlow201")
    # tcs_user = etree.SubElement(tcs_flow201, "TcsUser")
    # user_id = etree.SubElement(tcs_user, "UserId")
    # tcs_flow = etree.SubElement(tcs_flow201, "TcsFlow")
    # message_id = etree.SubElement(tcs_flow, "MessageId")
    # bp_no = etree.SubElement(tcs_flow, "BpNo")
    # action_list = etree.SubElement(tcs_flow, "ActionList")
    # action_id = etree.SubElement(action_list, "ActionId")
    # task_note = etree.SubElement(tcs_flow, "TaskNote")
    # task_note.text = "0"
    # corp_task_id = etree.SubElement(tcs_flow, "CorpTaskId")
    # task_control = etree.SubElement(tcs_flow, "TaskControl")
    # tcs_data = etree.SubElement(tcs_flow201, "TcsData", nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"})
    #
    # tcs_data_dic = OrderedDict()
    # tcs_data_dic['FILE_NAME'] = self.declare_company_id.register_code     # u'随附单据名称'
    # tcs_data_dic['BINARY_DATA'] = self.declare_company_id.register_name_cn  # u'PDF二进制数据'
    # tcs_data_dic['AGENTCODE'] = None   # 申报单位代码
    # tcs_data_dic['AGENTNAME'] = str(self.bill_no)    # u'申报单位名称'
    # tcs_data_dic['OWNERCODE'] = str(self.customer_contract_no)   # u'货主单位代码'
    # tcs_data_dic['OWNERNAME'] = self.cop_code  # u'录入单位代码'   # 货主单位名称
    # tcs_data_dic['TRADECODE'] = self.cop_name   # u'经营单位编号'
    # tcs_data_dic['TRADENAME'] = str(self.custom_master_id.Code)  # u'经营单位名称'
    # tcs_data_dic['PRE_ENTRY_ID'] = str(self.custom_master_id.Code)  # u'报关单预录入号'
    # tcs_data_dic['ENTRY_ID'] = str(self.custom_master_id.Code)  # u'报关单号'
    # tcs_data_dic['FORMAT_TYPE'] = str(self.custom_master_id.Code)  # u'格式类型'
    # tcs_data_dic['TRADE_CODE'] = str(self.custom_master_id.Code)  # u'企业编号'
    # tcs_data_dic['MASTER_CUSTOMS_CODE'] = str(self.custom_master_id.Code)  # u'申报口岸关区代码'
    # tcs_data_dic['GROUP_ID'] = str(self.custom_master_id.Code)  # u'分组标识'
    # tcs_data_dic['TRADE_FILE_NAME'] = str(self.custom_master_id.Code)  # u'文件原始名称'
    # tcs_data_dic['DECL_TYPE'] = str(self.custom_master_id.Code)  # u'上传类型'
    # tcs_data_dic['DECL_TIME'] = str(self.custom_master_id.Code)  # u'上传时间'
    # tcs_data_dic['DECL_CODE'] = str(self.custom_master_id.Code)  # u'上传人员代码'
    # tcs_data_dic['DECL_NAME'] = str(self.custom_master_id.Code)  # u'上传人员名称'
    # tcs_data_dic['FILE_TYPE'] = str(self.custom_master_id.Code)  # u'随附单据类型'
    # tcs_data_dic['FILE_SOURCE'] = str(self.custom_master_id.Code)  # u'数据来源'
    # tcs_data_dic['FILE_DIGEST'] = str(self.custom_master_id.Code)  # u'证书名称'
    # tcs_data_dic['SIGN_CERT'] = str(self.custom_master_id.Code)  # u'外网签名'
    # tcs_data_dic['FILE_SIGN'] = str(self.custom_master_id.Code)  # u'申报地海关'
    # tcs_data_dic['OP_NOTE'] = str(self.custom_master_id.Code)  # u'操作说明'
    #
    # for node in tcs_data_dic:
    #     _node = etree.SubElement(tcs_data, node)
    #     value = tcs_data_dic[node]
    #     if value:
    #         _node.text = value
    #
    #
    # # change the root to xml file
    # string = etree.tostring(root, xml_declaration=True, encoding='utf-8')
    # # base_dir = config.options['xml_files_path']
    # base_dir = config.options.get('xml_files_path', '/mnt/odooshare/customs_declaration_xml')
    #
    # # # 企业报关单 存放目录 前端界面配置
    # # 报文生成路径 用户配置界面自定义
    # company_name = str(self.cus_dec_dir)
    # dec_catalog_path = os.path.join(base_dir, company_name)
    # # 检查并生成相应的目录
    # if not os.path.exists(dec_catalog_path):
    #     os.mkdir(dec_catalog_path)
    # obj_dir = os.path.join(dec_catalog_path, 'attach' + str(self.client_seq_no) + '.xml')
    # with open(obj_dir, 'w') as fp:
    #     fp.write(string.encode('utf8'))