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
    dec_send_way = self.cus_dec_sent_way  # 获取 报关单发送通道 QP or 单一窗口
    dec_name = self.name   # 获取 报关单号
    for attach in self.information_attachment_ids:
        attach_id = attach.id
        attach_name = attach.name
        attach_data = attach.datas
        attach_edoc_type = attach.dec_edoc_type if attach.dec_edoc_type else "88888888"  # 随附单据类型  如果类型为空 默认值为8个8
        attach_xml_send_name = dec_name + "$" + attach_edoc_type + "$" + str(attach_id)   # 随附单据报文名字命名规范
        # attach_description = attach.description if attach.description else attach_xml_send_name  # 单据原始文件名
        if attach.description:
            attach_description = attach.description
        else:
            attach_description = attach_xml_send_name
            attach_dec_obj = self.env['ir.attachment'].search([('id', '=', attach_id)])
            attach_dec_obj.update({'description': attach_description})

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
            tcs_data_dic['FILE_NAME'] = attach_name if attach_name else None  # u'随附单据名称'
            tcs_data_dic['BINARY_DATA'] = attach_data if attach_data else None  # u'PDF二进制数据'
            tcs_data_dic['AGENTCODE'] = self.declare_company_id.register_code if self.declare_company_id.register_code else None # 申报单位代码
            tcs_data_dic['AGENTNAME'] = self.declare_company_id.register_name_cn if self.declare_company_id.register_name_cn else None # u'申报单位名称'
            tcs_data_dic['OWNERCODE'] = self.input_company_id.register_code  # u'货主单位代码'
            tcs_data_dic['OWNERNAME'] = self.input_company_id.register_name_cn  # 货主单位名称
            tcs_data_dic['TRADECODE'] = self.business_company_id.register_code  # u'经营单位编号'
            tcs_data_dic['TRADENAME'] = self.business_company_id.register_name_cn  # u'经营单位名称'
            tcs_data_dic['PRE_ENTRY_ID'] = None  # u'报关单预录入号'
            tcs_data_dic['ENTRY_ID'] = None  # u'报关单号'
            tcs_data_dic['FORMAT_TYPE'] = 'US'  # u'格式类型'
            tcs_data_dic['TRADE_CODE'] = self.input_company_id.register_code if self.input_company_id.register_code else None # u'企业编号'
            tcs_data_dic['MASTER_CUSTOMS_CODE'] = str(self.custom_master_id.Code)  # u'申报口岸关区代码'
            tcs_data_dic['GROUP_ID'] = None  # u'分组标识'
            tcs_data_dic['TRADE_FILE_NAME'] = attach_description if attach_description else None  # u'文件原始名称'
            tcs_data_dic['DECL_TYPE'] = 'F'  # u'上传类型'
            tcs_data_dic['DECL_TIME'] = (datetime.now()+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')   # u'上传时间'
            tcs_data_dic['DECL_CODE'] = self.ic_code if self.ic_code else None  # u'上传人员代码'   操作员IC卡号
            tcs_data_dic['DECL_NAME'] = self.oper_name if self.oper_name else None  # u'上传人员名称'
            tcs_data_dic['FILE_TYPE'] = attach_edoc_type if attach_edoc_type else None  # u'随附单据类型'
            tcs_data_dic['FILE_SOURCE'] = None  # u'数据来源'
            tcs_data_dic['FILE_DIGEST'] = None  # u'文件摘要'
            tcs_data_dic['SIGN_CERT'] = None  # u'证书名称'
            tcs_data_dic['FILE_SIGN'] = None  # u'外网签名'
            tcs_data_dic['OP_NOTE'] = None  # u'操作说明'

            for node in tcs_data_dic:
                _node = etree.SubElement(tcs_data, node)
                value = tcs_data_dic[node]
                if value:
                    _node.text = value
            # change the root to xml file
            string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')

            # 单一窗口报文发送根目录
            base_dir_send_single_attach = config.options.get('generate_wly_to_ex_single_attach_path',
                                                      '/mnt/xml_data/odooshare/about_wly_xml_data/post_ex_client/send_wly_to_ex_single_attach')
            # QP 报文发送根目录
            base_dir_send_qp_attach = config.options.get('generate_wly_to_ex_qp_attach_path',
                                                  '/mnt/xml_data/odooshare/about_wly_xml_data/post_ex_client/send_wly_to_ex_qp_attach')

            company_name = str(self.dec_company_customs_code)  # 申报单位海关编码 用作报文存放路径
            if dec_send_way:
                if dec_send_way == 'single':
                    dec_catalog_path = os.path.join(base_dir_send_single_attach, company_name)
                    # 检查并生成相应的目录
                    if not os.path.exists(dec_catalog_path):
                        os.mkdir(dec_catalog_path)
                    obj_dir = os.path.join(dec_catalog_path, attach_description +'$'+ (datetime.now()+timedelta(hours=8)).strftime('%Y%m%d%H%M%S') + '.xml')
                    with open(obj_dir.encode('utf8'), 'w') as fp:
                        fp.write(string.encode('utf8'))
                elif dec_send_way == 'QP':
                    dec_catalog_path = os.path.join(base_dir_send_qp_attach, company_name)
                    # 检查并生成相应的目录
                    if not os.path.exists(dec_catalog_path):
                        os.mkdir(dec_catalog_path)
                    obj_dir = os.path.join(dec_catalog_path, attach_description +'$'+ (datetime.now()+timedelta(hours=8)).strftime('%Y%m%d%H%M%S') + '.xml')
                    with open(obj_dir.encode('utf8'), 'w') as fp:
                        fp.write(string.encode('utf8'))

