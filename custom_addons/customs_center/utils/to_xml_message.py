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


def delegate_to_xml(self):
    """ 根据报关单生成xml报文 存放到指定目录 """
    root = etree.Element("DecMessage",  version="3.1", xmlns="http://www.chinaport.gov.cn/dec")
    head = etree.SubElement(root, "DecHead")
    body_list = etree.SubElement(root, "DecLists")
    body_containers_list = etree.SubElement(root, "DecContainers")
    body_license_docus_list = etree.SubElement(root, "DecLicenseDocus")
    body_free_test_list = etree.SubElement(root, "DecFreeTxt")
    body_dec_sign = etree.SubElement(root, "DecSign")
    trn_head_info = etree.SubElement(root, "TrnHead")
    trn_list_info = etree.SubElement(root, "TrnList")
    trn_containers_info = etree.SubElement(root, "TrnContainers")
    trn_conta_goods_list = etree.SubElement(root, "TrnContaGoodsList")
    e_doc_realation_info = etree.SubElement(root, "EdocRealation")

    # client_seq_no = str(uuid.uuid1())  # 客户端唯一编号

    head_node_dic = OrderedDict()
    head_node_dic['AgentCode'] = self.declare_company_id.register_code     # u'申报单位代码'
    head_node_dic['AgentName'] = self.declare_company_id.register_name_cn  # u'申报单位名称'
    head_node_dic['ApprNo'] = None
    head_node_dic['BillNo'] = str(self.bill_no)    # u'提单号'
    head_node_dic['ContrNo'] = str(self.customer_contract_no)   # u'合同编号'
    head_node_dic['CopCode'] = self.cop_code  # u'录入单位代码'   # 后台配置
    head_node_dic['CopName'] = self.cop_name   # u'录入单位名称'   # 后台配置   不能加str()
    head_node_dic['CustomMaster'] = str(self.custom_master_id.Code)  # u'申报地海关'
    head_node_dic['CutMode'] = str(self.CutMode_id.Code)  # u'征免性质'
    head_node_dic['DataSource'] = None
    # head_node_dic['DeclTrnRel'] = str(self.decl_trn_rel)  # u'报关/转关关系标志'
    head_node_dic['DeclTrnRel'] = u'0'  # u'报关/转关关系标志 # 玉斌建议 写入固定值0'
    head_node_dic['DistinatePort'] = str(self.port_id.Code)  # 装货港 delegate_port(2,)  ok
    head_node_dic['DistrictCode'] = str(self.region_id.Code)  # str(self.region_id.Code)  # u'境内目的地'  ok
    # head_node_dic['EntryId'] = str(self.ediId)  # u'报关标志'   # 增加选择字段
    head_node_dic['EntryId'] = None  # u'报关标志'   # 玉斌建议 先配置为空
    head_node_dic['EntryType'] = str(self.entry_type_id.Code)  # u'报关单类型'
    head_node_dic['FeeCurr'] = self.fee_currency_id.Code   # u'运费币制'
    head_node_dic['FeeMark'] = self.fee_mark.Code  # u'运费标记'
    head_node_dic['FeeRate'] = str(self.fee_rate)  # u'运费／率'
    head_node_dic['GrossWet'] = str(self.gross_weight)  # u'毛重'
    head_node_dic['IEDate'] = self.in_out_date   # u'进出日期'
    head_node_dic['IEFlag'] = self.inout   # u'进出口标志'
    head_node_dic['IEPort'] = self.customs_id.Code  # u'进出口岸'
    head_node_dic['InputerName'] = self.inputer_name  # u'录入员姓名'   # 设置界面和操作员同值  不能加str()
    head_node_dic['InRatio'] = None
    head_node_dic['InsurCurr'] = self.insurance_currency_id.Code  # u'保险费币制'
    head_node_dic['InsurMark'] = self.insurance_mark.Code  # u'保险费标记'
    head_node_dic['InsurRate'] = str(self.insurance_rate)  # u'保险费／率'
    head_node_dic['LicenseNo'] = self.licenseNo   # u'许可证编号'
    head_node_dic['ManualNo'] = self.ManualNo     # u'备案号'
    head_node_dic['NetWt'] = str(self.net_weight)      # u'净重'
    head_node_dic['NoteS'] = self.remarks      # u'备注'
    head_node_dic['OtherCurr'] = self.other_currency_id.Code   # u'杂费币制'
    head_node_dic['OtherMark'] = self.other_mark.Code  # u'杂费标志'
    head_node_dic['OtherRate'] = str(self.other_rate)   # u'杂费／率'
    head_node_dic['OwnerCode'] = None  # u'货主单位代码'
    head_node_dic['OwnerName'] = None  # u'货主单位名称'
    head_node_dic['PackNo'] = str(self.qty)  # u'件数'
    head_node_dic['PartenerID'] = None  # u'申报人标识'
    head_node_dic['PayWay'] = str(self.in_ratio)   # u'征税比例' in_ratio  报文PayWay
    head_node_dic['PaymentMark'] = self.payment_mark.Code  # u'纳税单位'
    head_node_dic['PDate'] = None  # u'首次进行暂存操作的系统时间'  非必填
    head_node_dic['PreEntryId'] = self.pre_entry_id  # u'预录入编号'
    head_node_dic['Risk'] = None   # u'风险评估参数'
    head_node_dic['SeqNo'] = self.dec_seq_no   # u'报关单统一编号'
    head_node_dic['TgdNo'] = None   # u'通关申请单号'
    head_node_dic['TradeCode'] = self.business_company_id.register_code   # u'经营单位编号/收发货人海关10位编号'
    head_node_dic['TradeCountry'] = self.origin_arrival_country_id.Code   # u'贸易国别'  启运/抵达国
    head_node_dic['TradeMode'] = self.trade_mode_id.Code  # u'监管方式'
    head_node_dic['TradeName'] = self.business_company_id.register_name_cn    # u'经营单位名称'  # self.business_company_id.register_name_cn
    head_node_dic['TrafMode'] = self.transport_mode_id.code   # u'运输方式代码'
    head_node_dic['TrafName'] = self.NativeShipName  # u'运输工具代码及名称'
    head_node_dic['TransMode'] = self.trade_terms_id.Code   # u'成交方式'
    head_node_dic['Type'] = None   # u'EDI申报备注'
    head_node_dic['TypistNo'] = self.ic_code  # u'录入员IC卡号'   # 必填配置界面
    head_node_dic['WrapType'] = self.packing_id.Code  # u'包装种类'
    head_node_dic['ChkSurety'] = None  # u'担保验放标志'
    head_node_dic['BillType'] = None  # u'备案清单类型' self.bill_type_id.Code
    head_node_dic['AgentCodeScc'] = str(self.dec_seq_no)  # u'申报单位统一编码'
    head_node_dic['CopCodeScc'] = self.cop_code_scc  # u'录入单位统一编码'    # 设置界面
    head_node_dic['OwnerCodeScc'] = self.input_company_id.unified_social_credit_code      # u'货主单位/消费生产单位 社会统一编码'
    head_node_dic['TradeCodeScc'] = self.business_company_id.unified_social_credit_code   # u'经营单位社会统一编码18位'
    head_node_dic['PromiseItmes'] = str(self.promise1.Code+self.promise2.Code+self.promise3.Code)       # u'承诺事项'  字符串拼接
    head_node_dic['TradeAreaCode'] = self.trade_country_id.Code  # u'贸易国别'

    for node in head_node_dic:
        _node = etree.SubElement(head, node)
        value = head_node_dic[node]
        if value:
            _node.text = value

    # edit the bodylist
    i = 0
    for item in self.dec_goods_list_ids:
        i += 1
        product_node_name = OrderedDict()
        product_node_name['ClassMark'] = None  # u'归类标志'
        product_node_name['CodeTS'] = str(item.cus_goods_tariff_id.Code_t)   # u'商品编号'
        product_node_name['ContrItem'] = None   # u'备案序号'
        product_node_name['DeclPrice'] = str(item.deal_unit_price)  # u'申报单价'
        product_node_name['DeclTotal'] = str(item.deal_total_price)  # u'申报总价'
        product_node_name['DutyMode'] = str(item.duty_mode_id.Code)    # u'征减免税方式'
        product_node_name['ExgNo'] = None   # u'货号'
        product_node_name['ExgVersion'] = None  # u'版本号'
        product_node_name['Factor'] = None   # u'申报计量单位与法定单位比例因子'
        product_node_name['FirstQty'] = str(item.first_qty)   # u'第一法定数量'
        # product_node_name['FirstUnit'] = item.first_unit.Code   # u'第一计量单位'
        product_node_name['FirstUnit'] = item.first_unit.Code   # u'第一计量单位'
        product_node_name['GUnit'] = item.deal_unit.Code    # u'申报/成交计量单位'
        product_node_name['GModel'] = str(item.goods_model)    # u'商品规格、型号'
        product_node_name['GName'] = item.goods_name   # u'商品名称'
        product_node_name['GNo'] = str(i)   # u'商品序号'
        product_node_name['GQty'] = str(item.deal_qty)     # u'申报数量（成交计量单位）'
        product_node_name['OriginCountry'] = item.origin_country_id.Code    # u'原产地'
        # product_node_name['SecondUnit'] = item.second_unit.Code   # u'第二计量单位'
        product_node_name['SecondUnit'] = item.second_unit.Code   # u'第二计量单位'
        product_node_name['SecondQty'] = str(item.second_qty)    # u'第二法定数量'
        product_node_name['TradeCurr'] = item.currency_id.Code   # u'成交币制'
        product_node_name['UseTo'] = None   # u'用途/生产厂家'
        product_node_name['WorkUsd'] = None  # u'工缴费'
        product_node_name['DestinationCountry'] = item.destination_country_id.Code    # u'最终目的国(地区)'

        body = etree.SubElement(body_list, "DecList")
        for node in product_node_name:
            _node = etree.SubElement(body, node)
            value = product_node_name[node]
            if value:
                _node.text = value

    # # 集装箱
    # dec_containers = OrderedDict()
    # dec_containers['ContainerId'] = u'集装箱号'
    # dec_containers['ContainerMd'] = u'集装箱规格'
    # dec_containers['ContainerWt'] = u'集装箱自重'
    # body1 = etree.SubElement(body_containers_list, "Container")
    # for node in dec_containers:
    #     _node = etree.SubElement(body1, node)
    #     value = dec_containers[node]
    #     if value:
    #         _node.text = value

    dec_license_docus = OrderedDict()
    dec_license_docus['DocuCode'] = str(self.licenseNo_id.dec_license_doc_type_id)   # u'单证代码/类型'
    dec_license_docus['CertCode'] = str(self.licenseNo_id.dec_license_no)   # u'单证编号'
    body2 = etree.SubElement(body_license_docus_list, "LicenseDocu")
    for node in dec_license_docus:
        _node = etree.SubElement(body2, node)
        value = dec_license_docus[node]
        if value:
            _node.text = value

    # dec_free_test = OrderedDict()
    # dec_free_test['BonNo'] = u'监管仓号'
    # dec_free_test['CusFie'] = u'货场代码'
    # dec_free_test['DecBpNo'] = u'报关员联系方式'
    # dec_free_test['DecNo'] = u'报关员号'
    # dec_free_test['RelId'] = u'关联报关单号'
    # dec_free_test['RelManNo'] = u'关联备案号'
    # dec_free_test['VoyNo'] = u'航次号'

    # for node in dec_free_test:
    #     _node = etree.SubElement(body_free_test_list, node)
    #     value = dec_free_test[node]
    #     if value:
    #         _node.text = value

    dec_sign = OrderedDict()
    # dec_sign['ClientSeqNo'] = client_seq_no.encode('utf8')
    dec_sign['ClientSeqNo'] = str(self.client_seq_no)
    dec_sign['CopCode'] = self.cop_code  # u'操作企业组织机构代码'   # 配置界面设置   不能加str()否则报编码 可能原因，设置默认值渲染到页面之后 已经是unicode
    dec_sign['ICCode'] = self.ic_code  # u'操作员IC卡号'   # 配置界面配置
    dec_sign['OperType'] = 'G'              # u'操作类型'
    dec_sign['OperName'] = self.oper_name  # u'操作员姓名'    # 配置界面
    dec_sign['Sign'] = 'abcdff'  # u'报关单签名'
    dec_sign['SignDate'] = (datetime.now()+timedelta(hours=8)).strftime('%Y%m%d%H%M%S00')  # u'签名时间'
    dec_sign['HostId'] = None  # u'邮箱ID'
    dec_sign['Certificate'] = self.certificate  # u'操作员卡对应的证书号'   # 配置界面

    for node in dec_sign:
        _node = etree.SubElement(body_dec_sign, node)
        value = dec_sign[node]
        if value:
            _node.text = value

    # 转关相关报文头部信息
    # trn_head = OrderedDict()
    # trn_head['ContractorName'] = None  # u'承运单位名称'
    # trn_head['ContractorCode'] = None  # u'承运单位组织机构代码'
    # trn_head['ESealFlag'] = None  # u'是否启用电子关锁标志'
    # trn_head['NativeTrafMode'] = None   # u'境内运输方式'
    # trn_head['NativeShipName'] = None  # u'境内运输工具名称'
    # trn_head['NativeVoyageNo'] = None  # u'境内运输工具航次'
    # trn_head['TrnPreId'] = None   # u'转关单统一编号'
    # trn_head['TransNo'] = None  # u'南方模式中的载货清单号'
    # trn_head['TransFlag'] = None  # u'转关类型'
    # trn_head['TrafCustomsNo'] = None  # u'境内运输工具编号'
    # trn_head['TurnNo'] = None  # u'转关申报单号'
    # trn_head['ValidTime'] = None  # u'预计运抵指运地时间'
    # trn_head['Notes'] = None  # u'备注'
    # trn_head['TrnType'] = None  # u'转关单类型'
    # # trn_head['ApplCodeScc'] = u'转关申报单位统一代码'
    #
    # for node in trn_head:
    #     _node = etree.SubElement(trn_head_info, node)
    #     value = trn_head[node]
    #     if value:
    #         _node.text = value

    # 转关相关报文列表信息
    trn_list = OrderedDict()
    trn_list['BillNo'] = self.bill_no  # u'提单号'
    trn_list['IEDate'] = None  # u'实际进出境日期'
    trn_list['ShipId'] = None  # u'进出境运输工具编号'
    trn_list['ShipNameEn'] = self.NativeShipName  # u'进出境运输工具名称（船舶名称）'
    trn_list['TrafMode'] = None  # u'进出境运输方式'
    trn_list['VoyageNo'] = self.VoyageNo  # u'进出境运输工具航次'

    for node in trn_list:
        _node = etree.SubElement(trn_list_info, node)
        value = trn_list[node]
        if value:
            _node.text = value

    # # 转关相关报文 集装箱信息
    # trn_containers = OrderedDict()
    # trn_containers['ContaNo'] = u'集装箱号'
    # trn_containers['ContaSn'] = u'集装箱序号'
    # trn_containers['ContaModel'] = u'集装箱规格'
    # trn_containers['SealNo'] = u'电子关锁号'
    # trn_containers['TransName'] = u'境内运输工具名称'
    # trn_containers['TransWeight'] = u'运输工具实际重量'
    # body3 = etree.SubElement(trn_containers_info, "TrnContainer")
    #
    # for node in trn_containers:
    #     _node = etree.SubElement(body3, node)
    #     value = trn_containers[node]
    #     if value:
    #         _node.text = value

    # 转关相关报文 商品信息
    # rn_conta_goods = OrderedDict()
    # rn_conta_goods['ContaNo'] = u'集装箱号'
    # rn_conta_goods['ContaGoodsCount'] = u'商品件数'
    # rn_conta_goods['ContaGoodsWeight'] = u'商品重量'
    # rn_conta_goods['GNo'] = u'商品序号'
    # body4 = etree.SubElement(trn_conta_goods_list, "TrnContaGoods")
    #
    # for node in rn_conta_goods:
    #     _node = etree.SubElement(body4, node)
    #     value = rn_conta_goods[node]
    #     if value:
    #         _node.text = value

    # 随附单据信息
    # e_doc_realation = OrderedDict()
    # e_doc_realation['EdocID'] = u'随附单据编号'
    # e_doc_realation['EdocCode'] = u'随附单据类别'
    # e_doc_realation['EdocFomatType'] = u'随附单据格式类型'
    # e_doc_realation['OpNote'] = u'操作说明'
    # e_doc_realation['EdocCopId'] = u'随附单据文件企业名'
    # e_doc_realation['EdocOwnerCode'] = u'所属单位海关编号'
    # e_doc_realation['SignUnit'] = u'签名单位代码'
    # e_doc_realation['SignTime'] = u'签名时间'
    # e_doc_realation['EdocOwnerName'] = u'所属单位名称'
    # e_doc_realation['EdocSize'] = u'随附单据文件大小'
    #
    # for node in e_doc_realation:
    #     _node = etree.SubElement(e_doc_realation_info, node)
    #     value = e_doc_realation[node]
    #     if value:
    #         _node.text = value

    # change the root to xml file
    string = etree.tostring(root, xml_declaration=True, encoding='utf-8')
    # base_dir = config.options['xml_files_path']

    base_dir = config.options.get('xml_files_path', '/mnt/odooshare/customs_declaration_xml')

    # # 企业报关单 存放目录 前端界面配置
    # et_dec_catalog_name = str(self.et_dec_catalog_ids.et_dec_catalog_name)
    # dec_catalog_path = os.path.join(base_dir, et_dec_catalog_name)
    # # 检查并生成相应的目录
    # if not os.path.exists(dec_catalog_path):
    #     os.mkdir(dec_catalog_path)
    # obj_dir = os.path.join(dec_catalog_path, 'DECDATA' + client_seq_no + '.xml')
    # with open(obj_dir, 'w') as fp:
    #     fp.write(string.encode('utf8'))

    ############################################################
    # 报文生成路径 方式1：: 根据当前公司名 自动生成
    # company_name = self.env.user.company_id.name

    # 报文生成路径 方式1： 用户配置界面自定义
    company_name = str(self.cus_dec_dir)
    dec_catalog_path = os.path.join(base_dir, company_name)
    # 检查并生成相应的目录
    if not os.path.exists(dec_catalog_path):
        os.mkdir(dec_catalog_path)
    obj_dir = os.path.join(dec_catalog_path, 'DECDATA' + str(self.client_seq_no) + '.xml')
    with open(obj_dir, 'w') as fp:
        fp.write(string.encode('utf8'))


# #####################################################################
# # 生成集成通3.0标准格式报文样例 代码
# #####################################################################

# def customs_delegate_to_xml(self):
#     """ 根据报关单生成xml报文 存放到指定目录 """
#     root = etree.Element("DecMessage",  version="3.1", xmlns="http://www.chinaport.gov.cn/dec")
#     head = etree.SubElement(root, "DecHead")
#     body_list = etree.SubElement(root, "DecLists")
#     body_containers_list = etree.SubElement(root, "DecContainers")
#     body_license_docus_list = etree.SubElement(root, "DecLicenseDocus")
#     body_free_test_list = etree.SubElement(root, "DecFreeTxt")
#     body_dec_sign = etree.SubElement(root, "DecSign")
#     trn_head_info = etree.SubElement(root, "TrnHead")
#     trn_list_info = etree.SubElement(root, "TrnList")
#     trn_containers_info = etree.SubElement(root, "TrnContainers")
#     trn_conta_goods_list = etree.SubElement(root, "TrnContaGoodsList")
#     e_doc_realation_info = etree.SubElement(root, "EdocRealation")
#
#     client_seq_no = str(uuid.uuid1())  # 客户端唯一编号
#
#     head_node_dic = OrderedDict()
#     head_node_dic['ClientSeqNo'] = client_seq_no.encode('utf8')
#     head_node_dic['AgentCode'] = u'申报单位代码'
#     head_node_dic['AgentName'] = u'申报单位名称'
#     head_node_dic['ApprNo'] = u'批准文号'
#     head_node_dic['BillNo'] = u'提单号'
#     head_node_dic['ContrNo'] = u'合同号'
#     head_node_dic['CopCode'] = u'录入单位代码'
#     head_node_dic['CopName'] = u'录入单位名称'
#     head_node_dic['CustomMaster'] = u'申报地海关'
#     head_node_dic['CutMode'] = u'征免性质'
#     head_node_dic['DataSource'] = u'数据来源'
#     head_node_dic['DeclTrnRel'] = u'报关/转关关系标志'
#     head_node_dic['DistinatePort'] = u'装货港'
#     head_node_dic['DistrictCode'] = u'境内目的地'
#     head_node_dic['EntryId'] = u'报关标志'
#     head_node_dic['EntryType'] = u'报关单类型'
#     head_node_dic['FeeCurr'] = u'运费币制'
#     head_node_dic['FeeMark'] = u'运费标记'
#     head_node_dic['FeeRate'] = u'运费／率'
#     head_node_dic['GrossWet'] = u'毛重'
#     head_node_dic['IEDate'] = u'进出日期'
#     head_node_dic['IEFlag'] = u'进出口标志'
#     head_node_dic['IEPort'] = u'进出口岸'
#     head_node_dic['InputerName'] = u'录入员姓名'
#     head_node_dic['InRatio'] = u'内销比率'
#     head_node_dic['InsurCurr'] = u'保险费币制'
#     head_node_dic['InsurMark'] = u'保险费标记'
#     head_node_dic['InsurRate'] = u'保险费／率'
#     head_node_dic['LicenseNo'] = u'许可证编号'
#     head_node_dic['ManualNo'] = u'备案号'
#     head_node_dic['NetWt'] = u'净重'
#     head_node_dic['NoteS'] = u'备注'
#     head_node_dic['OtherCurr'] = u'杂费币制'
#     head_node_dic['OtherMark'] = u'杂费标志'
#     head_node_dic['OtherRate'] = u'杂费／率'
#     head_node_dic['OwnerCode'] = u'货主单位代码'
#     head_node_dic['OwnerName'] = u'货主单位名称'
#     head_node_dic['PackNo'] = u'件数'
#     head_node_dic['PartenerID'] = u'申报人标识'
#     head_node_dic['PayWay'] = u'征税比例'
#     head_node_dic['PaymentMark'] = u'纳税单位'
#     head_node_dic['PDate'] = u'首次进行暂存操作的系统时间'
#     head_node_dic['PreEntryId'] = u'预录入编号'
#     head_node_dic['Risk'] = u'风险评估参数'
#     head_node_dic['SeqNo'] = u'报关单统一编号'
#     head_node_dic['TgdNo'] = u'通关申请单号'
#     head_node_dic['TradeCode'] = u'经营单位编号'
#     head_node_dic['TradeCountry'] = u'贸易国别'
#     head_node_dic['TradeMode'] = u'贸易方式'
#     head_node_dic['TradeName'] = u'经营单位名称'
#     head_node_dic['TrafMode'] = u'运输方式代码'
#     head_node_dic['TrafName'] = u'运输工具代码及名称'
#     head_node_dic['TransMode'] = u'成交方式'
#     head_node_dic['Type'] = u'EDI申报备注'
#     head_node_dic['TypistNo'] = u'录入员IC卡号'
#     head_node_dic['WrapType'] = u'包装种类'
#     head_node_dic['ChkSurety'] = u'担保验放标志'
#     head_node_dic['BillType'] = u'备案清单类型'
#     head_node_dic['AgentCodeScc'] = u'申报单位统一编码'
#     head_node_dic['CopCodeScc'] = u'录入单位统一编码'
#     head_node_dic['OwnerCodeScc'] = u'货主单位统一编码'
#     head_node_dic['TradeCodeScc'] = u'经营单位统一编码'
#     head_node_dic['PromiseItmes'] = u'承诺事项'
#     head_node_dic['TradeAreaCode'] = u'贸易国别'
#
#     for node in head_node_dic:
#         _node = etree.SubElement(head, node)
#         value = head_node_dic[node]
#         if value:
#             _node.text = value
#
#     # edit the bodylist
#     for item in self.dec_goods_list_ids:
#         product_node_name = OrderedDict()
#         product_node_name['ClassMark'] = u'归类标志'
#         product_node_name['CodeTS'] = u'商品编号'
#         product_node_name['ContrItem'] = u'备案序号'
#         product_node_name['DeclPrice'] = u'申报单价'
#         product_node_name['DeclTotal'] = u'申报总价'
#         product_node_name['DutyMode'] = u'征减免税方式'
#         product_node_name['ExgNo'] = u'货号'
#         product_node_name['ExgVersion'] = u'版本号'
#         product_node_name['Factor'] = u'申报计量单位与法定单位比例因子'
#         product_node_name['FirstQty'] = u'第一法定数量'
#         product_node_name['FirstUnit'] = u'第一计量单位'
#         product_node_name['GUnit'] = u'申报计量单位'
#         product_node_name['GModel'] = u'商品规格、型号'
#         product_node_name['GName'] = u'商品名称'
#         product_node_name['GNo'] = u'商品序号'
#         product_node_name['GQty'] = u'申报数量（成交计量单位）'
#         product_node_name['OriginCountry'] = u'原产地'
#         product_node_name['SecondUnit'] = u'第二计量单位'
#         product_node_name['SecondQty'] = u'第二法定数量'
#         product_node_name['TradeCurr'] = u'成交币制'
#         product_node_name['UseTo'] = u'用途/生产厂家'
#         product_node_name['WorkUsd'] = u'工缴费'
#         product_node_name['DestinationCountry'] = u'最终目的国(地区)'
#
#         body = etree.SubElement(body_list, "DecList")
#         for node in product_node_name:
#             _node = etree.SubElement(body, node)
#             value = product_node_name[node]
#             if value:
#                 _node.text = value
#
#     # 集装箱
#     dec_containers = OrderedDict()
#     dec_containers['ContainerId'] = u'集装箱号'
#     dec_containers['ContainerMd'] = u'集装箱规格'
#     dec_containers['ContainerWt'] = u'集装箱自重'
#     body1 = etree.SubElement(body_containers_list, "Container")
#     for node in dec_containers:
#         _node = etree.SubElement(body1, node)
#         value = dec_containers[node]
#         if value:
#             _node.text = value
#
#     dec_license_docus = OrderedDict()
#     dec_license_docus['DocuCode'] = u'单证代码'
#     dec_license_docus['CertCode'] = u'单证编号'
#     body2 = etree.SubElement(body_license_docus_list, "LicenseDocu")
#     for node in dec_license_docus:
#         _node = etree.SubElement(body2, node)
#         value = dec_license_docus[node]
#         if value:
#             _node.text = value
#
#     dec_free_test = OrderedDict()
#     dec_free_test['BonNo'] = u'监管仓号'
#     dec_free_test['CusFie'] = u'货场代码'
#     dec_free_test['DecBpNo'] = u'报关员联系方式'
#     dec_free_test['DecNo'] = u'报关员号'
#     dec_free_test['RelId'] = u'关联报关单号'
#     dec_free_test['RelManNo'] = u'关联备案号'
#     dec_free_test['VoyNo'] = u'航次号'
#
#     for node in dec_free_test:
#         _node = etree.SubElement(body_free_test_list, node)
#         value = dec_free_test[node]
#         if value:
#             _node.text = value
#
#     dec_sign = OrderedDict()
#     dec_sign['ClientSeqNo'] = u'客户端报关单编号'
#     dec_sign['CopCode'] = u'操作企业组织机构代码'
#     dec_sign['ICCode'] = u'操作员IC卡号'
#     dec_sign['OperType'] = u'操作类型'
#     dec_sign['OperName'] = u'操作员姓名'
#     dec_sign['Sign'] = u'报关单签名'
#     dec_sign['SignDate'] = u'签名时间'
#     dec_sign['HostId'] = u'邮箱ID'
#     dec_sign['Certificate'] = u'操作员卡对应的证书号'
#
#     for node in dec_sign:
#         _node = etree.SubElement(body_dec_sign, node)
#         value = dec_sign[node]
#         if value:
#             _node.text = value
#
#     # 转关相关报文头部信息
#     trn_head = OrderedDict()
#     trn_head['ContractorName'] = u'承运单位名称'
#     trn_head['ContractorCode'] = u'承运单位组织机构代码'
#     trn_head['ESealFlag'] = u'是否启用电子关锁标志'
#     trn_head['NativeTrafMode'] = u'境内运输方式'
#     trn_head['NativeShipName'] = u'境内运输工具名称'
#     trn_head['NativeVoyageNo'] = u'境内运输工具航次'
#     trn_head['TrnPreId'] = u'转关单统一编号'
#     trn_head['TransNo'] = u'南方模式中的载货清单号'
#     trn_head['TransFlag'] = u'转关类型'
#     trn_head['TrafCustomsNo'] = u'境内运输工具编号'
#     trn_head['TurnNo'] = u'转关申报单号'
#     trn_head['ValidTime'] = u'预计运抵指运地时间'
#     trn_head['Notes'] = u'备注'
#     trn_head['TrnType'] = u'转关单类型'
#     trn_head['ApplCodeScc'] = u'转关申报单位统一代码'
#
#     for node in trn_head:
#         _node = etree.SubElement(trn_head_info, node)
#         value = trn_head[node]
#         if value:
#             _node.text = value
#
#     # 转关相关报文列表信息
#     trn_list = OrderedDict()
#     trn_list['BillNo'] = u'提单号'
#     trn_list['IEDate'] = u'实际进出境日期'
#     trn_list['ShipId'] = u'进出境运输工具编号'
#     trn_list['ShipNameEn'] = u'进出境运输工具名称（船舶名称）'
#     trn_list['TrafMode'] = u'进出境运输方式'
#     trn_list['VoyageNo'] = u'进出境运输工具航次'
#
#     for node in trn_list:
#         _node = etree.SubElement(trn_list_info, node)
#         value = trn_list[node]
#         if value:
#             _node.text = value
#
#     # 转关相关报文 集装箱信息
#     trn_containers = OrderedDict()
#     trn_containers['ContaNo'] = u'集装箱号'
#     trn_containers['ContaSn'] = u'集装箱序号'
#     trn_containers['ContaModel'] = u'集装箱规格'
#     trn_containers['SealNo'] = u'电子关锁号'
#     trn_containers['TransName'] = u'境内运输工具名称'
#     trn_containers['TransWeight'] = u'运输工具实际重量'
#     body3 = etree.SubElement(trn_containers_info, "TrnContainer")
#
#     for node in trn_containers:
#         _node = etree.SubElement(body3, node)
#         value = trn_containers[node]
#         if value:
#             _node.text = value
#
#     # 转关相关报文 商品信息
#     rn_conta_goods = OrderedDict()
#     rn_conta_goods['ContaNo'] = u'集装箱号'
#     rn_conta_goods['ContaGoodsCount'] = u'商品件数'
#     rn_conta_goods['ContaGoodsWeight'] = u'商品重量'
#     rn_conta_goods['GNo'] = u'商品序号'
#     body4 = etree.SubElement(trn_conta_goods_list, "TrnContaGoods")
#
#     for node in rn_conta_goods:
#         _node = etree.SubElement(body4, node)
#         value = rn_conta_goods[node]
#         if value:
#             _node.text = value
#
#     # 随附单据信息
#     e_doc_realation = OrderedDict()
#     e_doc_realation['EdocID'] = u'随附单据编号'
#     e_doc_realation['EdocCode'] = u'随附单据类别'
#     e_doc_realation['EdocFomatType'] = u'随附单据格式类型'
#     e_doc_realation['OpNote'] = u'操作说明'
#     e_doc_realation['EdocCopId'] = u'随附单据文件企业名'
#     e_doc_realation['EdocOwnerCode'] = u'所属单位海关编号'
#     e_doc_realation['SignUnit'] = u'签名单位代码'
#     e_doc_realation['SignTime'] = u'签名时间'
#     e_doc_realation['EdocOwnerName'] = u'所属单位名称'
#     e_doc_realation['EdocSize'] = u'随附单据文件大小'
#
#     for node in e_doc_realation:
#         _node = etree.SubElement(e_doc_realation_info, node)
#         value = e_doc_realation[node]
#         if value:
#             _node.text = value
#
#     # change the root to xml file
#     string = etree.tostring(root, xml_declaration=True, encoding='utf-8')
#     base_dir = config.options['xml_files_path']
#     if not os.path.exists(base_dir):
#         os.mkdir(base_dir)
#     obj_dir = os.path.join(base_dir, client_seq_no + '.xml')
#     with open(obj_dir, 'w') as fp:
#         fp.write(string.encode('utf8'))
