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

# 路径配置

GENERATE_WLY_TO_EX_SINGLE_PATH = config.options.get('generate_wly_to_ex_single_path',
                                              '/home/odoo/Desktop/ParallelsSharedFolders/Home/about_wly_xml_data/post_ex_client/send_wly_to_ex_single')
GENERATE_WLY_TO_EX_QP_PATH = config.options.get('generate_wly_to_ex_qp_path',
                                          '/home/odoo/Desktop/ParallelsSharedFolders/Home/about_wly_xml_data/post_ex_client/send_wly_to_ex_qp')

"""生成海关需要的xml报文，并从物流云发送到海关系统"""


def generate_customs_dec_xml(self):
    """生成报关单xml报文"""
    """ 根据报关单生成xml报文 存放到指定目录 """
    root = etree.Element("DecMessage", version="3.1", xmlns="http://www.chinaport.gov.cn/dec")
    head = etree.SubElement(root, "DecHead")
    body_list = etree.SubElement(root, "DecLists")
    body_containers_list = etree.SubElement(root, "DecContainers")
    body_license_docus_list = etree.SubElement(root, "DecLicenseDocus")
    body_free_test_list = etree.SubElement(root, "DecFreeTxt")
    body_dec_sign = etree.SubElement(root, "DecSign")
    # trn_head_info = etree.SubElement(root, "TrnHead")
    # trn_list_info = etree.SubElement(root, "TrnList")
    # trn_containers_info = etree.SubElement(root, "TrnContainers")
    # trn_conta_goods_list = etree.SubElement(root, "TrnContaGoodsList")
    # e_doc_realation_info = etree.SubElement(root, "EdocRealation")

    # client_seq_no = str(uuid.uuid1())  # 客户端唯一编号
    # 报关单发送通道
    dec_send_way = self.cus_dec_sent_way

    head_node_dic = OrderedDict()
    # head_node_dic['AgentCode'] = self.declare_company_id.register_code if self.declare_company_id.register_code else None    # u'申报单位代码'
    # head_node_dic['AgentName'] = self.declare_company_id.register_name_cn if self.declare_company_id.register_name_cn else None # u'申报单位名称'

    # 申报单位直接读取配置文件的写法
    head_node_dic['AgentCode'] = self.dec_company_customs_code if self.dec_company_customs_code else None  # u'申报单位代码'
    # head_node_dic['AgentName'] = self.dec_company if self.dec_company else None   # u'申报单位名称'
    head_node_dic[
        'AgentName'] = self.declare_company_id.register_name_cn if self.declare_company_id.register_name_cn else None  # u'申报单位名称'

    head_node_dic['ApprNo'] = None
    head_node_dic['BillNo'] = str(self.bill_no) if self.bill_no else None  # u'提单号'
    head_node_dic['ContrNo'] = str(self.customer_contract_no) if self.customer_contract_no else None  # u'合同编号'
    head_node_dic['CopCode'] = self.cop_code if self.cop_code else None  # u'录入单位代码'   # 后台配置
    head_node_dic['CopName'] = self.cop_name if self.cop_name else None  # u'录入单位名称'   # 后台配置   不能加str()
    head_node_dic['CustomMaster'] = str(self.custom_master_id.code) if self.custom_master_id.code else None  # u'申报地海关'
    head_node_dic['CutMode'] = str(self.cut_mode_id.code) if self.cut_mode_id.code else None  # u'征免性质'
    head_node_dic['DataSource'] = None
    # head_node_dic['DeclTrnRel'] = str(self.decl_trn_rel)  # u'报关/转关关系标志'
    head_node_dic['DeclTrnRel'] = u'0'  # u'报关/转关关系标志 # 玉斌建议 写入固定值0'
    head_node_dic['DistinatePort'] = str(self.port_id.code) if self.port_id.code else None  # 装货港 delegate_port(2,)  ok
    head_node_dic['DistrictCode'] = str(
        self.internal_district_id.code) if self.internal_district_id.code else None  # str(self.region_id.Code)  # u'境内目的地'  ok
    # head_node_dic['EdiId'] = str(self.ediId)  # u'报关标志'   # 增加选择字段
    head_node_dic['EdiId'] = '1'  # u'报关标志'   # 增加选择字段
    head_node_dic['EntryId'] = None  # u'海关编号'   # 玉斌建议 先配置为空
    head_node_dic['EntryType'] = str(self.entry_type_id.code) if self.entry_type_id.code else None  # u'报关单类型'
    head_node_dic['FeeCurr'] = self.fee_currency_id.code if self.fee_currency_id.code else None  # u'运费币制'
    head_node_dic['FeeMark'] = self.fee_mark.code if self.fee_mark.code else None  # u'运费标记'
    head_node_dic['FeeRate'] = str(self.fee_rate) if self.fee_rate or self.fee_rate == '0.0' else None  # u'运费／率'
    head_node_dic['GrossWet'] = str(self.gross_weight) if self.gross_weight else None  # u'毛重'
    ie_date = self.in_out_date.split(' ')[0] if self.in_out_date else None  # 日期格式 精确到日 2017-11-24
    head_node_dic['IEDate'] = ie_date  # u'进出日期'
    head_node_dic['IEFlag'] = self.inout if self.inout else None  # u'进出口标志'
    head_node_dic['IEPort'] = self.customs_id.code if self.customs_id.code else None  # u'进出口岸'
    head_node_dic['InputerName'] = self.inputer_name if self.inputer_name else None  # u'录入员姓名'   # 设置界面和操作员同值  不能加str()
    head_node_dic['InRatio'] = None
    head_node_dic[
        'InsurCurr'] = self.insurance_currency_id.code if self.insurance_currency_id.code else None  # u'保险费币制'
    head_node_dic['InsurMark'] = self.insurance_mark.code if self.insurance_mark.code else None  # u'保险费标记'
    head_node_dic['InsurRate'] = str(
        self.insurance_rate) if self.insurance_rate or self.insurance_rate == '0.0' else None  # u'保险费／率'
    head_node_dic['LicenseNo'] = self.license_no if self.license_no else None  # u'许可证编号'
    head_node_dic['ManualNo'] = self.manual_no if self.manual_no else None  # u'备案号'
    head_node_dic['NetWt'] = str(self.net_weight) if self.net_weight else None  # u'净重'
    head_node_dic['NoteS'] = self.remarks if self.remarks else None  # u'备注'
    head_node_dic['OtherCurr'] = self.other_currency_id.code if self.other_currency_id.code else None  # u'杂费币制'
    head_node_dic['OtherMark'] = self.other_mark.code if self.other_mark.code else None  # u'杂费标志'
    head_node_dic['OtherRate'] = str(self.other_rate) if self.other_rate or self.other_rate else None  # u'杂费／率'
    head_node_dic[
        'OwnerCode'] = self.input_company_id.register_code if self.input_company_id.register_code else None  # u'货主单位代码'
    head_node_dic[
        'OwnerName'] = self.input_company_id.register_name_cn if self.input_company_id.register_name_cn else None  # u'货主单位名称'
    head_node_dic['PackNo'] = str(self.qty) if self.qty else None  # u'件数'
    head_node_dic['PartenerID'] = None  # u'申报人标识'
    head_node_dic['PayWay'] = str(
        self.in_ratio) if self.in_ratio or self.in_ratio == '0' else None  # u'征税比例' in_ratio  报文PayWay
    head_node_dic['PaymentMark'] = self.payment_mark.code if self.payment_mark.code else None  # u'纳税单位'
    head_node_dic['PDate'] = None  # u'首次进行暂存操作的系统时间'  非必填
    head_node_dic['PreEntryId'] = self.pre_entry_id if self.pre_entry_id else None  # u'预录入编号'
    head_node_dic['Risk'] = None  # u'风险评估参数'
    head_node_dic['SeqNo'] = self.dec_seq_no if self.dec_seq_no else None  # u'报关单统一编号'
    head_node_dic['TgdNo'] = None  # u'通关申请单号'
    head_node_dic[
        'TradeCode'] = self.business_company_id.register_code if self.business_company_id.register_code else None  # u'经营单位编号/收发货人海关10位编号'
    head_node_dic[
        'TradeCountry'] = self.origin_arrival_country_id.code if self.origin_arrival_country_id.code else None  # u'贸易国别'  启运/抵达国
    head_node_dic['TradeMode'] = self.trade_mode_id.code if self.trade_mode_id.code else None  # u'监管方式'
    head_node_dic[
        'TradeName'] = self.business_company_id.register_name_cn if self.business_company_id.register_name_cn else None  # u'经营单位名称'  # self.business_company_id.register_name_cn
    head_node_dic['TrafMode'] = self.transport_mode_id.code if self.transport_mode_id.code else None  # u'运输方式代码'
    head_node_dic['TrafName'] = self.native_ship_name if self.native_ship_name else None  # u'运输工具代码及名称'
    head_node_dic['TransMode'] = self.trade_terms_id.code if self.trade_terms_id.code else None  # u'成交方式'
    head_node_dic['Type'] = None  # u'EDI申报备注'
    head_node_dic['TypistNo'] = self.ic_code if self.ic_code else None  # u'录入员IC卡号'   # 必填配置界面
    head_node_dic['WrapType'] = self.wrap_type_id.code if self.wrap_type_id.code else None  # u'包装种类'
    head_node_dic['ChkSurety'] = None  # u'担保验放标志'
    head_node_dic['BillType'] = None  # u'备案清单类型' self.bill_type_id.code
    head_node_dic['AgentCodeScc'] = str(self.dec_seq_no).strip().strip("\n").strip("\t").strip(
        "\r") if self.dec_seq_no else None  # u'申报单位统一编码'
    head_node_dic['CopCodeScc'] = str(self.cop_code_scc).strip().strip("\n").strip("\t").strip(
        "\r") if self.cop_code_scc else None  # u'录入单位统一编码'    # 设置界面
    head_node_dic[
        'OwnerCodeScc'] = self.input_company_id.unified_social_credit_code if self.input_company_id.unified_social_credit_code else None  # u'货主单位/消费生产单位 社会统一编码'
    head_node_dic[
        'TradeCodeScc'] = self.business_company_id.unified_social_credit_code if self.business_company_id.unified_social_credit_code else None  # u'经营单位社会统一编码18位'
    promise1 = self.promise1.code if self.promise1.code else '0'
    promise2 = self.promise2.code if self.promise2.code else '0'
    promise3 = self.promise3.code if self.promise3.code else '0'
    head_node_dic['PromiseItmes'] = str(promise1 + promise2 + promise3)  # u'承诺事项'  字符串拼接
    head_node_dic['TradeAreaCode'] = self.trade_country_id.code if self.trade_country_id.code else None  # u'贸易国别'

    for node in head_node_dic:
        _node = etree.SubElement(head, node)
        value = head_node_dic[node]
        if value:
            _node.text = value

    # edit the bodylist
    i = 0
    for item in self.dec_goods_list:
        i += 1
        product_node_name = OrderedDict()
        product_node_name['ClassMark'] = None  # u'归类标志'
        product_node_name[
            'CodeTS'] = item.goods_tariff_id.code_ts if item.goods_tariff_id.code_ts else None  # u'商品编号'
        product_node_name['ContrItem'] = None  # u'备案序号'
        product_node_name['DeclPrice'] = str(item.deal_unit_price) if item.deal_unit_price else None  # u'申报单价'
        dec_total = ("%.2f" % item.deal_total_price) if item.deal_total_price else None
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(type(item.deal_total_price))
        print(dec_total)
        product_node_name['DeclTotal'] = dec_total  # u'申报总价'
        # product_node_name['DeclTotal'] = dec_total # u'申报总价'
        product_node_name['DutyMode'] = item.duty_mode_id.code if item.duty_mode_id.code else None  # u'征减免税方式'
        product_node_name['ExgNo'] = None  # u'货号'
        product_node_name['ExgVersion'] = None  # u'版本号'
        product_node_name['Factor'] = None  # u'申报计量单位与法定单位比例因子'
        product_node_name['FirstQty'] = str(item.first_qty) if item.first_qty else None  # u'第一法定数量'
        product_node_name['FirstUnit'] = item.first_unit_id.code if item.first_unit_id.code else None  # u'第一计量单位'
        product_node_name['GUnit'] = item.deal_unit_id.code if item.deal_unit_id.code else None  # u'申报/成交计量单位'
        product_node_name['GModel'] = item.goods_model if item.goods_model else None  # u'商品规格、型号'
        product_node_name['GName'] = item.goods_name if item.goods_name else None  # u'商品名称'
        product_node_name['GNo'] = str(i)  # u'商品序号'
        product_node_name['GQty'] = str(item.deal_qty) if item.deal_qty else None  # u'申报数量'
        product_node_name[
            'OriginCountry'] = item.origin_country_id.code if item.origin_country_id.code else None  # u'原产地'
        product_node_name['SecondUnit'] = item.second_unit_id.code if item.second_unit_id.code else None  # u'第二计量单位'
        product_node_name['SecondQty'] = str(item.second_qty) if item.second_qty else None  # u'第二法定数量'
        product_node_name['TradeCurr'] = item.currency_id.code if item.currency_id.code else None  # u'成交币制'
        product_node_name['UseTo'] = None  # u'用途/生产厂家'
        product_node_name['WorkUsd'] = None  # u'工缴费'
        product_node_name[
            'DestinationCountry'] = item.destination_country_id.code if item.destination_country_id.code else None  # u'最终目的国(地区)'

        body = etree.SubElement(body_list, "DecList")
        for node in product_node_name:
            _node = etree.SubElement(body, node)
            value = product_node_name[node]
            if value:
                _node.text = value

    # 集装箱
    i = 0
    for item in self.dec_container_ids:
        i += 1
        dec_containers = OrderedDict()
        dec_containers['ContainerId'] = item.containerNo if item.containerNo else None  # u'集装箱号'
        dec_containers['ContainerMd'] = item.spec_code if item.spec_code else None  # u'集装箱规格'
        dec_containers['ContainerWt'] = str(item.weight) if item.weight else None  # u'集装箱自重'
        body1 = etree.SubElement(body_containers_list, "Container")
        for node in dec_containers:
            _node = etree.SubElement(body1, node)
            value = dec_containers[node]
            if value:
                _node.text = value

    # 单证信息
    for lic_item in self.dec_lic_doc_list:
        dec_license_docus = OrderedDict()
        dec_license_docus[
            'DocuCode'] = lic_item.dec_license_doc_type_id.code if lic_item.dec_license_doc_type_id.code else None  # u'单证代码/类型'
        dec_license_docus['CertCode'] = lic_item.dec_license_no if lic_item.dec_license_no else None  # u'单证编号'
        body2 = etree.SubElement(body_license_docus_list, "LicenseDocu")
        for node in dec_license_docus:
            _node = etree.SubElement(body2, node)
            value = dec_license_docus[node]
            if value:
                _node.text = value

    # 报关单关联信息
    dec_free_test = OrderedDict()
    dec_free_test['BonNo'] = self.bonded_No if self.bonded_No else None  # u'监管仓号'
    dec_free_test['CusFie'] = self.customs_field if self.customs_field else None  # u'货场代码'
    dec_free_test['DecBpNo'] = None  # u'报关员联系方式'
    dec_free_test['DecNo'] = None  # u'报关员号'
    dec_free_test['RelId'] = self.rel_dec_No if self.rel_dec_No else None  # u'关联报关单号'
    dec_free_test['RelManNo'] = self.rel_man_No if self.rel_man_No else None  # u'关联备案号'
    dec_free_test['VoyNo'] = self.voyage_no if self.voyage_no else None  # u'航次号'

    for node in dec_free_test:
        _node = etree.SubElement(body_free_test_list, node)
        value = dec_free_test[node]
        if value:
            _node.text = value

    # 报关单签名
    dec_sign = OrderedDict()
    # dec_sign['ClientSeqNo'] = client_seq_no.encode('utf8')
    dec_sign['ClientSeqNo'] = str(self.client_seq_no)
    dec_sign['CopCode'] = self.cop_code  # u'操作企业组织机构代码'   # 配置界面设置   不能加str()否则报编码 可能原因，设置默认值渲染到页面之后 已经是unicode
    dec_sign['ICCode'] = self.ic_code  # u'操作员IC卡号'   # 配置界面配置
    dec_sign['OperType'] = 'G'  # u'操作类型'
    dec_sign['OperName'] = self.oper_name  # u'操作员姓名'    # 配置界面
    dec_sign['Sign'] = 'abcdff'  # u'报关单签名'
    dec_sign['SignDate'] = (datetime.now() + timedelta(hours=8)).strftime('%Y%m%d%H%M%S00')  # u'签名时间'
    dec_sign['HostId'] = None  # u'邮箱ID'
    dec_sign['Certificate'] = self.certificate  # u'操作员卡对应的证书号'   # 配置界面

    for node in dec_sign:
        _node = etree.SubElement(body_dec_sign, node)
        value = dec_sign[node]
        if value:
            _node.text = value

    # 随附单据信息
    attach_list = []
    for item in self.information_attachment_ids:
        e_doc_realation = OrderedDict()
        e_doc_realation['EdocID'] = item.name if item.name else None  # u'随附单据编号'
        e_doc_realation['EdocCode'] = item.description if item.description else None  # u'随附单据类别' 必填
        e_doc_realation['EdocFomatType'] = 'US'  # u'随附单据格式类型'  必填
        e_doc_realation['OpNote'] = None  # u'操作说明'
        e_doc_realation['EdocCopId'] = None  # u'随附单据文件企业名'
        e_doc_realation['EdocOwnerCode'] = str(self.custom_master_id.code)  # u'所属单位海关编号' 必填
        e_doc_realation['SignUnit'] = self.declare_company_id.register_code  # u'签名单位代码'
        e_doc_realation['SignTime'] = str((datetime.now() + timedelta(hours=8)).strftime('%Y%m%d%H%M%S'))  # u'签名时间' 必填
        e_doc_realation['EdocOwnerName'] = self.business_company_id.register_name_cn  # u'所属单位名称'
        e_doc_realation['EdocSize'] = None  # u'随附单据文件大小'
        attach_list.append(e_doc_realation)

    for e_doc_realation in attach_list:
        attach_tag = etree.SubElement(root, "EdocRealation")
        for node in e_doc_realation:
            _node = etree.SubElement(attach_tag, node)
            value = e_doc_realation[node]
            if value:
                _node.text = value

    # change the root to xml file
    string = etree.tostring(root, pretty_print=True, xml_declaration=True,
                            encoding='utf-8')  # pretty_print=True, 该参数可以生成格式化后的XML
    # base_dir = config.options['xml_files_path']

    return string


def send_customs_dec_xml_to_ex(self):
    """发送报关单xml报文到单一窗口"""
    dec_send_way = self.cus_dec_sent_way

    string = generate_customs_dec_xml(self)

    # 企业报关单 报文生成路径  用户配置界面自定义
    company_name = str(self.dec_company_customs_code)  # 申报单位海关编码 用作报文存放路径
    if dec_send_way:
        if dec_send_way == 'single':
            dec_catalog_path = os.path.join(GENERATE_WLY_TO_EX_SINGLE_PATH, company_name)
            # 检查并生成相应的目录
            if not os.path.exists(dec_catalog_path):
                os.mkdir(dec_catalog_path)
            obj_dir = os.path.join(dec_catalog_path, 'DECDATA-SINGLE-' + str(self.client_seq_no) + '.xml')
            with open(obj_dir, 'w') as fp:
                fp.write(string.encode('utf8'))
        elif dec_send_way == 'QP':
            dec_catalog_path = os.path.join(GENERATE_WLY_TO_EX_QP_PATH, company_name)
            # 检查并生成相应的目录
            if not os.path.exists(dec_catalog_path):
                os.mkdir(dec_catalog_path)
            obj_dir = os.path.join(dec_catalog_path, 'DECDATA-QP-' + str(self.client_seq_no) + '.xml')
            with open(obj_dir, 'w') as fp:
                fp.write(string.encode('utf8'))

    pass



def generate_customs_dec_edoc_xml(self):
    """生成报关单随附单据报文"""
    # """ 生成单一窗口 随附单据报文xml报文 存放到指定目录 """
    # # 获取 报关单发送通道 QP or 单一窗口
    # for attach in self.information_attachment_ids:
    #     attach_name = attach.name
    #     attach_data = attach.datas
    #     attach_description = attach.description
    #     attach_edoc_type = attach.dec_edoc_type
    #
    #     if attach_name and attach_data:
    #         root = etree.Element("Data")
    #         tcs_flow201 = etree.SubElement(root, "TcsFlow201")
    #         tcs_user = etree.SubElement(tcs_flow201, "TcsUser")
    #         user_id = etree.SubElement(tcs_user, "UserId")
    #         tcs_flow = etree.SubElement(tcs_flow201, "TcsFlow")
    #         message_id = etree.SubElement(tcs_flow, "MessageId")
    #         bp_no = etree.SubElement(tcs_flow, "BpNo")
    #         action_list = etree.SubElement(tcs_flow, "ActionList")
    #         action_id = etree.SubElement(action_list, "ActionId")
    #         task_note = etree.SubElement(tcs_flow, "TaskNote")
    #         task_note.text = "0"
    #         corp_task_id = etree.SubElement(tcs_flow, "CorpTaskId")
    #         task_control = etree.SubElement(tcs_flow, "TaskControl")
    #         tcs_data = etree.SubElement(tcs_flow201, "TcsData",
    #                                     nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"})
    #
    #         tcs_data_dic = OrderedDict()
    #         tcs_data_dic['FILE_NAME'] = attach_name if attach_name else None  # u'随附单据名称'
    #         tcs_data_dic['BINARY_DATA'] = attach_data if attach_data else None  # u'PDF二进制数据'
    #         tcs_data_dic[
    #             'AGENTCODE'] = self.declare_company_id.register_code if self.declare_company_id.register_code else None  # 申报单位代码
    #         tcs_data_dic[
    #             'AGENTNAME'] = self.declare_company_id.register_name_cn if self.declare_company_id.register_name_cn else None  # u'申报单位名称'
    #         tcs_data_dic['OWNERCODE'] = self.input_company_id.register_code  # u'货主单位代码'
    #         tcs_data_dic['OWNERNAME'] = self.input_company_id.register_name_cn  # 货主单位名称
    #         tcs_data_dic['TRADECODE'] = self.business_company_id.register_code  # u'经营单位编号'
    #         tcs_data_dic['TRADENAME'] = self.business_company_id.register_name_cn  # u'经营单位名称'
    #         tcs_data_dic['PRE_ENTRY_ID'] = None  # u'报关单预录入号'
    #         tcs_data_dic['ENTRY_ID'] = None  # u'报关单号'
    #         tcs_data_dic['FORMAT_TYPE'] = 'US'  # u'格式类型'
    #         tcs_data_dic[
    #             'TRADE_CODE'] = self.input_company_id.register_code if self.input_company_id.register_code else None  # u'企业编号'
    #         tcs_data_dic['MASTER_CUSTOMS_CODE'] = str(self.custom_master_id.Code)  # u'申报口岸关区代码'
    #         tcs_data_dic['GROUP_ID'] = None  # u'分组标识'
    #         tcs_data_dic['TRADE_FILE_NAME'] = attach_name if attach_name else None  # u'文件原始名称'
    #         tcs_data_dic['DECL_TYPE'] = 'F'  # u'上传类型'
    #         tcs_data_dic['DECL_TIME'] = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')  # u'上传时间'
    #         tcs_data_dic['DECL_CODE'] = self.ic_code if self.ic_code else None  # u'上传人员代码'   操作员IC卡号
    #         tcs_data_dic['DECL_NAME'] = self.oper_name if self.oper_name else None  # u'上传人员名称'
    #         tcs_data_dic['FILE_TYPE'] = attach_edoc_type if attach_edoc_type else None  # u'随附单据类型'
    #         tcs_data_dic['FILE_SOURCE'] = None  # u'数据来源'
    #         tcs_data_dic['FILE_DIGEST'] = None  # u'文件摘要'
    #         tcs_data_dic['SIGN_CERT'] = None  # u'证书名称'
    #         tcs_data_dic['FILE_SIGN'] = None  # u'外网签名'
    #         tcs_data_dic['OP_NOTE'] = None  # u'操作说明'
    #
    #         for node in tcs_data_dic:
    #             _node = etree.SubElement(tcs_data, node)
    #             value = tcs_data_dic[node]
    #             if value:
    #                 _node.text = value
    #         # change the root to xml file
    #         string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')
    #
    #         # 单一窗口报文发送根目录
    #         base_dir_send_single_attach = config.options.get('generate_wly_to_ex_single_attach_path',
    #                                                          '/mnt/xml_data/about_wly_xml_data/post_ex_client/send_wly_to_ex_single_attach')
    #         # QP 报文发送根目录
    #         base_dir_send_qp_attach = config.options.get('generate_wly_to_ex_qp_attach_path',
    #                                                      '/mnt/xml_data/about_wly_xml_data/post_ex_client/send_wly_to_ex_qp_attach')
    #
    #         company_name = str(self.dec_company_customs_code)  # 申报单位海关编码 用作报文存放路径
    #         if dec_send_way:
    #             if dec_send_way == 'single':
    #                 dec_catalog_path = os.path.join(base_dir_send_single_attach, company_name)
    #                 # 检查并生成相应的目录
    #                 if not os.path.exists(dec_catalog_path):
    #                     os.mkdir(dec_catalog_path)
    #                 obj_dir = os.path.join(dec_catalog_path,
    #                                        attach_description + '$' + (datetime.now() + timedelta(hours=8)).strftime(
    #                                            '%Y%m%d%H%M%S') + '.xml')
    #                 with open(obj_dir.encode('utf8'), 'w') as fp:
    #                     fp.write(string.encode('utf8'))
    #             elif dec_send_way == 'QP':
    #                 dec_catalog_path = os.path.join(base_dir_send_qp_attach, company_name)
    #                 # 检查并生成相应的目录
    #                 if not os.path.exists(dec_catalog_path):
    #                     os.mkdir(dec_catalog_path)
    #                 obj_dir = os.path.join(dec_catalog_path,
    #                                        attach_description + '$' + (datetime.now() + timedelta(hours=8)).strftime(
    #                                            '%Y%m%d%H%M%S') + '.xml')
    #                 with open(obj_dir.encode('utf8'), 'w') as fp:
    #                     fp.write(string.encode('utf8'))


def send_customs_dec_edoc_xml_to_ex(self):
    """发送报关单随附单据报文到单一窗口"""
    pass


