# -*- coding: utf-8 -*-

import logging
import os
import shutil

from lxml import etree

from odoo.tools import config

_logger = logging.getLogger(__name__)

# MAIN_PATH = '/home/odoo/Desktop/ParallelsSharedFolders/Home'  # 欧玉斌的本地目录
# MAIN_PATH = '/home/odoo/odooshare'  # 王志强的本地目录
MAIN_PATH = '/mnt/xml_data'  # test测试环境地址 195.186

# pre_ex_client 前置交换客户端路径
PARSE_CUS_TO_WLY_PATH = config.options.get('parse_cus_to_wly_path',
                                           MAIN_PATH + '/about_wly_xml_data/pre_ex_client/cus_to_wly')
PARSE_CUS_TO_WLY_ATTACH_PATH = config.options.get('parse_cus_to_wly_attach_path',
                                                  MAIN_PATH + '/about_wly_xml_data/pre_ex_client/cus_to_wly_attach_send')
PARSE_SEND_ERROR_XML_PATH = config.options.get('parse_send_error_xml_path',
                                               MAIN_PATH + '/about_wly_xml_data/pre_ex_client/send_error_xml_message')
BACKUP_SEND_XML_PATH = config.options.get('backup_send_xml_path',
                                          MAIN_PATH + '/about_wly_xml_data/pre_ex_client/send_backup_xml')  # 新光原始报文备份目录
BACKUP_SEND_ATTACH_XML_PATH = config.options.get('backup_attach_send_xml_path',
                                                 MAIN_PATH + '/about_wly_xml_data/pre_ex_client/send_backup_xml_attach')  # 新光原始报文备份目录

DEBUG = False  # debug=true时，为了调试方便，不执行将报文移动错误或备份文件夹的操作

"""解析从客户发送给物流云的报文（主要是报关单报文、随附单据报文），解析入口后，备份到相应路径"""


def check_and_mkdir(*path):
    for p in path:
        if not os.path.exists(p):
            os.mkdir(p)


def parse_customs_dec_xml(self):
    """从客户给物流云发送的报关单报文文件夹中，解析报关单报文（解析入库后生成报关单和随附单据（空附件））"""

    customs_dec_model_dic = self.env['cus_center.customs_dec'].default_get(
        ['dec_company_customs_code'])  # 获取报关单模型对象
    company_xml_parse_path = customs_dec_model_dic.get('dec_company_customs_code')  # 获取配置信息中的 申报单位海关编码 作为解析路径

    print(company_xml_parse_path)
    parse_xml_path = os.path.join(PARSE_CUS_TO_WLY_PATH, company_xml_parse_path.encode('utf-8'))  # 原始报文解析目录
    parse_attach_path = os.path.join(PARSE_CUS_TO_WLY_ATTACH_PATH,
                                     company_xml_parse_path.encode('utf-8'))  # 随附单据解析目录
    parse_error_xml_path = os.path.join(PARSE_SEND_ERROR_XML_PATH, company_xml_parse_path.encode('utf-8'))
    backup_xml_path = os.path.join(BACKUP_SEND_XML_PATH, company_xml_parse_path.encode('utf-8'))  # 原始报文备份目录
    backup_attach_xml_path = os.path.join(BACKUP_SEND_ATTACH_XML_PATH,
                                          company_xml_parse_path.encode('utf-8'))  # 随附单据报文备份目录

    # 检查并生成相应的目录
    check_and_mkdir(parse_xml_path, parse_attach_path, parse_error_xml_path, backup_xml_path,
                    backup_attach_xml_path)

    files = os.listdir(parse_xml_path)
    files = [filename for filename in files if filename.endswith('.xml')]
    if not files:
        return True
    files = [os.path.join(parse_xml_path, i) for i in files]

    # 读文件，用lxml解析报文
    for xml_message in files:

        with open(xml_message, 'r') as f:
            xml_str = str(f.read())
            xml_str = xml_str.replace('xmlns="http://www.chinaport.gov.cn/dec"', '')
            root = etree.fromstring(xml_str)  # 打开xml文档

            customs_dec_dic = {}
            root_name = etree.QName(root).localname
            print(root_name)  # DecMessage
            if root_name == u'DecMessage':
                head_node = root.find('DecHead')
                body_list = root.find('DecLists')
                body_containers_list = root.find('DecContainers')
                body_license_docus_list = root.find('DecLicenseDocus')
                body_free_test_list = root.find('DecFreeTxt')
                body_dec_sign = root.find('DecSign')
                trn_head_info = root.find('TrnHead')
                trn_list_info = root.find('TrnList')
                trn_containers_info = root.find('TrnContainers')
                trn_conta_goods_list = root.find('TrnContaGoodsList')
                e_doc_realation_info = root.findall('EdocRealation')  # 随附单据标签

                customs_dec_dic['DecHead'] = {}
                if head_node:
                    for child in head_node:
                        if child.text:
                            customs_dec_dic['DecHead'][child.tag] = child.text
                # 报文中的商品列表
                customs_dec_dic['DecLists'] = {}
                d_list = 0
                for child in body_list:
                    customs_dec_dic['DecLists'][d_list] = {}
                    for child_son in child:
                        if child_son.text:
                            customs_dec_dic['DecLists'][d_list][child_son.tag] = child_son.text
                    d_list += 1
                dec_goods_list_dic = customs_dec_dic['DecLists']

                customs_dec_dic['DecContainers'] = {}
                if body_containers_list:
                    for child in body_containers_list:
                        if child.text:
                            customs_dec_dic['DecContainers'][child.tag] = child.text

                customs_dec_dic['DecLicenseDocus'] = {}
                if body_license_docus_list:
                    for child in body_license_docus_list:
                        if child.text:
                            customs_dec_dic['DecLicenseDocus'][child.tag] = child.text

                customs_dec_dic['DecFreeTxt'] = {}
                if body_free_test_list:
                    for child in body_free_test_list:
                        if child.text:
                            customs_dec_dic['DecFreeTxt'][child.tag] = child.text

                customs_dec_dic['DecFreeTxt'] = {}
                if body_free_test_list:
                    for child in body_free_test_list:
                        if child.text:
                            customs_dec_dic['DecFreeTxt'][child.tag] = child.text

                customs_dec_dic['DecSign'] = {}
                if body_dec_sign:
                    for child in body_dec_sign:
                        if child.text:
                            customs_dec_dic['DecSign'][child.tag] = child.text

                customs_dec_dic['TrnHead'] = {}
                if trn_head_info:
                    for child in trn_head_info:
                        if child.text:
                            customs_dec_dic['TrnHead'][child.tag] = child.text

                customs_dec_dic['TrnList'] = {}
                if trn_list_info:
                    for child in trn_list_info:
                        if child.text:
                            customs_dec_dic['TrnList'][child.tag] = child.text

                customs_dec_dic['TrnContainers'] = {}
                if trn_containers_info:
                    for child in trn_containers_info:
                        if child.text:
                            customs_dec_dic['TrnContainers'][child.tag] = child.text

                customs_dec_dic['TrnContaGoodsList'] = {}
                if trn_conta_goods_list:
                    for child in trn_conta_goods_list:
                        if child.text:
                            customs_dec_dic['TrnContaGoodsList'][child.tag] = child.text

                # 随附单据
                customs_dec_dic['EdocRealation'] = {}
                if e_doc_realation_info:
                    d_list = 0
                    for child in e_doc_realation_info:
                        customs_dec_dic['EdocRealation'][d_list] = {}
                        for child_son in child:
                            if child_son.text:
                                customs_dec_dic['EdocRealation'][d_list][child_son.tag] = child_son.text
                        d_list += 1
                attach_list_dic = customs_dec_dic['EdocRealation']  # # 随附单据字典
            else:
                _logger.error(u'Find error format xml message: %s' % xml_message.decode('utf-8'))
                shutil.move(xml_message, parse_error_xml_path)
                continue

        if customs_dec_dic:
            client_seq_no = customs_dec_dic['DecSign'].get('ClientSeqNo', None)  # 报关单客户端编号
            inout = customs_dec_dic['DecHead'].get('IEFlag', None)  # u'进出口标志'

            custom_master_code = customs_dec_dic['DecHead'].get('CustomMaster', None)  # u'申报地海关'
            custom_master_id = self.env['cus_args.customs'].search([('code', '=', custom_master_code)])

            dec_seq_no = customs_dec_dic['DecHead'].get('AgentCodeScc', None)  # u'统一编号'  申报单位统一编码
            pre_entry_id = customs_dec_dic['DecHead'].get('PreEntryId', None)  # u'预录入编号'

            customs_code = customs_dec_dic['DecHead'].get('IEPort', None)  # u'进出口岸'
            customs_id = self.env['cus_args.customs'].search([('code', '=', customs_code)])

            manual_no = customs_dec_dic['DecHead'].get('ManualNo', None)  # u'备案号'
            customer_contract_no = customs_dec_dic['DecHead'].get('ContrNo', None)  # u'合同编号'

            in_out_date = customs_dec_dic['DecHead'].get('IEDate', None)  # u'进出口日期'

            business_company_register_code = customs_dec_dic['DecHead'].get('TradeCode', None)  # 收发货人
            business_company_id = self.env['cus_args.register_company'].search(
                [('register_code', '=', business_company_register_code)])

            input_company_register_code = customs_dec_dic['DecHead'].get('OwnerCode', None)  # 消费使用单位 货主单位
            input_company_id = self.env['cus_args.register_company'].search(
                [('register_code', '=', input_company_register_code)])

            declare_company_register_code = customs_dec_dic['DecHead'].get('AgentCode', None)  # 申报单位
            declare_company_id = self.env['cus_args.register_company'].search(
                [('register_code', '=', declare_company_register_code)])

            transport_mode_code = customs_dec_dic['DecHead'].get('TrafMode', None)  # u'运输方式'
            transport_mode_id = self.env['cus_args.transport_mode'].search([('code', '=', transport_mode_code)])

            native_ship_name = customs_dec_dic['DecHead'].get('TrafName', None)  # u'运输工具名称'
            voyage_no = customs_dec_dic['TrnList'].get('voyage_no', None)  # u'航次号'
            bill_no = customs_dec_dic['DecHead'].get('BillNo', None)  # u'提运单号'

            trade_mode_code = customs_dec_dic['DecHead'].get('TradeMode', None)  # u'监管方式'
            trade_mode_id = self.env['cus_args.trade_mode'].search([('code', '=', trade_mode_code)])

            CutMode_code = customs_dec_dic['DecHead'].get('CutMode', None)  # u'征免性质'
            cut_mode_id = self.env['cus_args.cut_mode'].search([('code', '=', CutMode_code)])

            payment_mark_code = customs_dec_dic['DecHead'].get('PaymentMark', None)  # u'纳税单位'
            payment_mark = self.env['cus_center.pay_mark_type'].search([('code', '=', payment_mark_code)])

            licenseNo = customs_dec_dic['DecHead'].get('LicenseNo', None)  # u'许可证编号'

            origin_arrival_country_code = customs_dec_dic['DecHead'].get('TradeCountry', None)  # u'启运国/抵达国'
            origin_arrival_country_id = self.env['cus_args.country'].search(
                [('code', '=', origin_arrival_country_code)])

            port_code = customs_dec_dic['DecHead'].get('DistinatePort', None)  # u'装货/指运港'
            port_id = self.env['cus_args.port'].search([('code', '=', port_code)])

            internal_district_code = customs_dec_dic['DecHead'].get('DistrictCode', None)  # u'境内目的/货源地'
            internal_district_id = self.env['cus_args.internal_district'].search(
                [('code', '=', internal_district_code)])

            trade_terms_code = customs_dec_dic['DecHead'].get('TransMode', None)  # u'成交方式 or 贸易条款'
            trade_terms_id = self.env['cus_args.trade_terms'].search([('code', '=', trade_terms_code)])

            fee_mark_code = customs_dec_dic['DecHead'].get('FeeMark', None)  # u'运费标记'
            fee_mark = self.env['cus_center.exp_mark_type'].search([('code', '=', fee_mark_code)])
            fee_rate = customs_dec_dic['DecHead'].get('FeeRate', None)  # u'运费／率'

            fee_currency_code = customs_dec_dic['DecHead'].get('FeeCurr', None)  # u'运费币制'
            fee_currency_id = self.env['cus_args.currency'].search([('code', '=', fee_currency_code)])

            insurance_mark_code = customs_dec_dic['DecHead'].get('InsurMark', None)  # u'保险费标记'
            insurance_mark = self.env['cus_center.exp_mark_type'].search([('code', '=', insurance_mark_code)])
            insurance_rate = customs_dec_dic['DecHead'].get('InsurRate', None)  # u'保险费／率'

            insurance_currency_code = customs_dec_dic['DecHead'].get('InsurCurr', None)  # u'保险费币制'
            insurance_currency_id = self.env['cus_args.currency'].search(
                [('code', '=', insurance_currency_code)])

            other_mark_code = customs_dec_dic['DecHead'].get('OtherMark', None)  # u'杂费标记'
            other_mark = self.env['cus_center.exp_mark_type'].search([('code', '=', other_mark_code)])
            other_rate = customs_dec_dic['DecHead'].get('OtherRate', None)  # u'杂费／率'

            other_currency_code = customs_dec_dic['DecHead'].get('OtherCurr', None)  # u'杂费币制'
            other_currency_id = self.env['cus_args.currency'].search([('code', '=', other_currency_code)])

            qty = customs_dec_dic['DecHead'].get('PackNo', None)  # u'件数'

            wrap_type_code = customs_dec_dic['DecHead'].get('WrapType', None)  # u'包装种类'
            wrap_type_id = self.env['cus_args.wrap_type'].search([('code', '=', wrap_type_code)])

            gross_weight = customs_dec_dic['DecHead'].get('GrossWet', None)  # u'毛重'
            net_weight = customs_dec_dic['DecHead'].get('NetWt', None)  # u'净重'

            trade_country_code = customs_dec_dic['DecHead'].get('TradeAreaCode', None)  # u'贸易国别'
            trade_country_id = self.env['cus_args.country'].search([('code', '=', trade_country_code)])

            in_ratio = customs_dec_dic['DecHead'].get('PayWay', None)  # u'征税比例' in_ratio  报文PayWay

            promise1_promise2_promise3_code = customs_dec_dic['DecHead'].get('PromiseItmes', None)  # u'承诺事项'  字符串拼接

            promise1_code = str(promise1_promise2_promise3_code)[0] if promise1_promise2_promise3_code else None
            promise2_code = str(promise1_promise2_promise3_code)[1] if promise1_promise2_promise3_code else None
            promise3_code = str(promise1_promise2_promise3_code)[2] if promise1_promise2_promise3_code else None
            promise1 = self.env['cus_center.whet_mark_type'].search([('code', '=', promise1_code)])  # 特殊关系确认
            promise2 = self.env['cus_center.whet_mark_type'].search([('code', '=', promise2_code)])  # 价格影响确认
            promise3 = self.env['cus_center.whet_mark_type'].search(
                [('code', '=', promise3_code)])  # 支付特许权使用费确认

            entry_type_code = customs_dec_dic['DecHead'].get('EntryType', None)  # u'报关单类型'
            entry_type_id = self.env['cus_args.entry_type'].search([('code', '=', entry_type_code)])

            remarks = customs_dec_dic['DecHead'].get('NoteS', None)  # u'备注'

            cop_code = customs_dec_dic['DecHead'].get('CopCode', None)  # u'录入单位企业组织机构代码'
            cop_name = customs_dec_dic['DecHead'].get('CopName', None)  # u'录入单位名称'
            cop_code_scc = customs_dec_dic['DecHead'].get('CopCodeScc', None)  # u'录入单位社会信用统一编码'
            inputer_name = customs_dec_dic['DecHead'].get('InputerName', None)  # u'录入员姓名'
            oper_name = customs_dec_dic['DecSign'].get('OperName', None)  # u'操作员姓名'
            certificate = customs_dec_dic['DecSign'].get('Certificate', None)  # u'操作员卡的证书号'
            ic_code = customs_dec_dic['DecHead'].get('TypistNo', None)  # u'操作员IC卡号/录入员IC卡号'

            customs_dec_dic = {
                'synergism_seq_no': client_seq_no,  # 报关单客户端编号
                'client_seq_no': client_seq_no,  # 报关单客户端编号
                'inout': inout,  # u'进出口标志'
                'custom_master_id': custom_master_id[0].id if len(custom_master_id) else None,  # 申报口岸 / 申报地海关
                'dec_seq_no': dec_seq_no,  # u'统一编号'
                'pre_entry_id': pre_entry_id,  # u'预录入编号'
                'customs_id': customs_id[0].id if len(customs_id) else None,  # u'进出口岸'
                'manual_no': manual_no,  # u'备案号'
                'customer_contract_no': customer_contract_no,  # u'合同协议号'
                'in_out_date': in_out_date,  # u'进出口日期'
                'business_company_id': business_company_id[0].id if len(business_company_id) else None,  # 收发货人
                'input_company_id': input_company_id[0].id if len(input_company_id) else None,  # 消费使用单位 货主单位
                'declare_company_id': declare_company_id[0].id if len(declare_company_id) else None,  # 申报单位
                'transport_mode_id': transport_mode_id[0].id if len(transport_mode_id) else None,  # u'运输方式'
                'native_ship_name': native_ship_name,  # u'运输工具名称'
                'voyage_no': voyage_no,  # u'航次号'
                'bill_no': bill_no,  # u'提运单号'
                'trade_mode_id': trade_mode_id[0].id if len(trade_mode_id) else None,  # u'监管方式'
                'cut_mode_id': cut_mode_id[0].id if len(cut_mode_id) else None,  # u'征免性质'
                'payment_mark': payment_mark[0].id if len(payment_mark) else None,  # 纳税单位 id
                'licenseNo': licenseNo,  # u'许可证编号'
                'origin_arrival_country_id': origin_arrival_country_id[0].id if len(
                    origin_arrival_country_id) else None,  # 启运国/抵达国
                'port_id': port_id[0].id if len(port_id) else None,  # 装货/指运港 id
                'internal_district_id': internal_district_id[0].id if len(internal_district_id) else None,
                # 境内目的/货源地 id
                'trade_terms_id': trade_terms_id[0].id if len(trade_terms_id) else None,  # 成交方式 or 贸易条款 id
                'fee_mark': fee_mark[0].id if len(fee_mark) else None,  # # 运费标记 id
                'fee_rate': fee_rate,  # 运费/率
                'fee_currency_id': fee_currency_id[0].id if len(fee_currency_id) else None,  # 运费币制
                'insurance_mark': insurance_mark[0].id if len(insurance_mark) else None,  # 保险费标记
                'insurance_rate': insurance_rate,  # 保险费/率
                'insurance_currency_id': insurance_currency_id[0].id if len(insurance_currency_id) else None,
                # 保险费币制
                'other_mark': other_mark[0].id if len(other_mark) else None,  # 杂费标记
                'other_rate': other_rate,  # 杂费/率
                'other_currency_id': other_currency_id[0].id if len(other_currency_id) else None,  # 杂费币制
                'qty': qty,  # 件数
                'wrap_type_id': wrap_type_id[0].id if len(wrap_type_id) else None,  # 包装种类、方式 id
                'gross_weight': gross_weight,  # 毛重
                'net_weight': net_weight,  # 净重
                'trade_country_id': trade_country_id[0].id if len(trade_country_id) else None,  # 贸易国别
                'in_ratio': in_ratio,  # u'征税比例' in_ratio  报文PayWay
                'promise1': promise1[0].id if len(promise1) else None,  # 特殊关系确认
                'promise2': promise2[0].id if len(promise2) else None,  # 价格影响确认
                'promise3': promise3[0].id if len(promise3) else None,  # 支付特许权使用费确认
                'entry_type_id': entry_type_id[0].id if len(entry_type_id) else None,  # 报关单类型 关联报关单类型字典表
                'remarks': remarks,  # 备注
                'cop_code': cop_code,  # 录入单位企业组织机构代码
                'cop_name': cop_name,  # 录入单位名称
                'cop_code_scc': cop_code_scc,  # 录入单位社会信用统一编码
                'inputer_name': inputer_name,  # 录入员姓名
                'oper_name': oper_name,  # 操作员姓名
                'certificate': certificate,  # 操作员卡的证书号
                'ic_code': ic_code,  # 操作员IC卡号/录入员IC卡号
            }
            customs_dec_dic = {item: customs_dec_dic[item] for item in customs_dec_dic if customs_dec_dic[item]}
        else:
            _logger.error(u'Find error format xml message: %s' % xml_message.decode('utf-8'))
            if not DEBUG:
                shutil.copy2(xml_message, parse_error_xml_path)
                os.remove(xml_message)
            continue

        try:
            customs_declaration_obj = self.env['cus_center.customs_dec'].create(customs_dec_dic)
            # 创建报关单后 同时创建 空的 随附单据附件
            # 首先解析随附单据目录的文件  可能多个附件

            # 生成附件
            if attach_list_dic:  # 报关单中的随附单据数据 attach_list_dic
                for keys, values_dic in attach_list_dic.items():
                    if values_dic:
                        genarate_attach_list_dic = {}
                        for k, values in values_dic.items():
                            if k == 'EdocID':
                                attach_id = values  # u'随附单据编号'
                                genarate_attach_list_dic['name'] = attach_id
                                genarate_attach_list_dic['datas_fname'] = attach_id

                                # # 查询和文件名匹配的二进制数据   正向生成的时候 有个问题 就是报关单报文到了 随附单据报文还未接收到
                                # if xml_attach_message_list:
                                #     for attach_dic in xml_attach_message_list:
                                #         if attach_dic.get('FILE_NAME') == attach_id:
                                #             binary_data = attach_dic.get('BINARY_DATA', None)
                                #             genarate_attach_list_dic['datas'] = binary_data
                            if k == 'EdocCode':
                                edoc_code = values  # u'随附单据类别'
                                print('************22222**********')
                                print(edoc_code)
                                # genarate_attach_list_dic['description'] = edoc_code # 原先第一次实现 用的附件模型字段自带的description字段 临时存放了
                                # genarate_attach_list_dic['attach_type'] = edoc_code   # 第二种方案 关务中心附件上传 扩展了附件模型 增加单据类型字段attach_type
                                genarate_attach_list_dic['dec_edoc_type'] = edoc_code  # 第三种方案 附件拖拽上传 扩展了附件字段

                        # 如果报关单对象为真 并且随附单据字典数据不为空 才会创建随附单据空附件
                        if customs_declaration_obj.id and genarate_attach_list_dic:
                            genarate_attach_list_dic['res_model'] = "cus_center.customs_dec"
                            genarate_attach_list_dic['res_id'] = customs_declaration_obj.id
                            genarate_attach_list_dic = {item: genarate_attach_list_dic[item] for item in
                                                        genarate_attach_list_dic if
                                                        genarate_attach_list_dic[item]}

                            new_attachment = self.env['ir.attachment'].create(genarate_attach_list_dic)
                            edoc_queue_obj = self.env['cus_center.edoc_queue'].create({
                                'edoc_id': genarate_attach_list_dic['name'],
                                'edoc_code': genarate_attach_list_dic['dec_edoc_type'],
                                'cus_dec_id': genarate_attach_list_dic['res_id']
                            })

                            # if not attach_files_list or not new_attachment:
                            if not edoc_queue_obj:
                                return True
                            # for xml_attach_message in attach_files_list:  # xml_attach_message是单据名
                            #     if xml_attach_message:
                            #         strlist = xml_attach_message.split('$')
                            #         filename = strlist[0]
                            #         if genarate_attach_list_dic.get('name' , None) == filename:  # 如果解析出的随附单据名 和 生成的随附单据名相同 就把报文移动到附件报文备份目录
                            #             # 这里 其实物流云不必放到备份目录再生成一遍随附单据报文 可以直接丢到 wly_to_ex_atach目录
                            #             xml_attach_message_path = os.path.join(parse_attach_path, xml_attach_message)
                            #             shutil.move(xml_attach_message_path, backup_attach_xml_path)
                            #             _logger.info(u'Had parsed the attach xml message %s' % xml_attach_message.decode('utf-8'))

            # 商品列表 字典
            # dec_goods_list_dic = customs_dec_dic['DecLists']
            if dec_goods_list_dic:
                for keys, values_dic in dec_goods_list_dic.items():
                    if values_dic:
                        dec_goods_list = {}
                        for k, values in values_dic.items():
                            if k == 'CodeTS':
                                cus_goods_tariff_code_ts = values  # u'商品编号'
                                cus_goods_tariff_id = self.env['cus_args.goods_tariff'].search(
                                    [('code_ts', '=', cus_goods_tariff_code_ts)])
                                dec_goods_list['goods_tariff_id'] = cus_goods_tariff_id[0].id if len(
                                    cus_goods_tariff_id) else None
                            elif k == 'GName':
                                goods_name = values  # u'商品名称'
                                dec_goods_list['goods_name'] = goods_name
                            elif k == 'GModel':
                                goods_model = values  # u'商品规格、型号'
                                dec_goods_list['goods_model'] = goods_model
                            elif k == 'GQty':
                                deal_qty = values  # u'申报数量  成交数量'
                                dec_goods_list['deal_qty'] = deal_qty
                            elif k == 'DeclPrice':
                                deal_unit_price = values  # u'申报单价 成交单价'
                                dec_goods_list['deal_unit_price'] = deal_unit_price
                            elif k == 'GUnit':
                                deal_unit_code = values  # u'申报/成交计量单位'
                                deal_unit_id = self.env['cus_args.unit'].search([('code', '=', deal_unit_code)])
                                dec_goods_list['deal_unit_id'] = deal_unit_id[0].id if len(deal_unit_id) else None
                            elif k == 'DeclTotal':
                                deal_total_price = values  # u'申报总价 成交总价'
                                dec_goods_list['deal_total_price'] = deal_total_price
                            elif k == 'TradeCurr':
                                currency_code = values  # u'成交币制'
                                currency_id = self.env['cus_args.currency'].search(
                                    [('code', '=', currency_code)])
                                dec_goods_list['currency_id'] = currency_id[0].id if len(currency_id) else None
                            elif k == 'FirstQty':
                                first_qty = values  # u'第一法定数量'
                                dec_goods_list['first_qty'] = first_qty
                            elif k == 'FirstUnit':
                                first_unit_code = values  # u'第一计量单位'
                                first_unit_id = self.env['cus_args.unit'].search(
                                    [('code', '=', first_unit_code)])
                                dec_goods_list['first_unit_id'] = first_unit_id[0].id if len(
                                    first_unit_id) else None
                            elif k == 'SecondQty':
                                second_qty = values  # u'第二法定数量'
                                dec_goods_list['second_qty'] = second_qty
                            elif k == 'SecondUnit':
                                second_unit_code = values  # u'第二计量单位'
                                second_unit_id = self.env['cus_args.unit'].search(
                                    [('code', '=', second_unit_code)])
                                dec_goods_list['second_unit_id'] = second_unit_id[0].id if len(
                                    second_unit_id) else None
                            elif k == 'DutyMode':
                                duty_mode_code = values  # u'征减免税方式'
                                duty_mode_id = self.env['cus_args.duty_mode'].search(
                                    [('code', '=', duty_mode_code)])
                                dec_goods_list['duty_mode_id'] = duty_mode_id[0].id if len(duty_mode_id) else None
                            elif k == 'OriginCountry':
                                origin_country_code = values  # u'原产地'
                                origin_country_id = self.env['cus_args.country'].search(
                                    [('code', '=', origin_country_code)])
                                dec_goods_list['origin_country_id'] = origin_country_id[0].id if len(
                                    origin_country_id) else None
                            elif k == 'DestinationCountry':
                                destination_country_code = values  # u'最终目的国'
                                destination_country_id = self.env['cus_args.country'].search(
                                    [('code', '=', destination_country_code)])
                                dec_goods_list['destination_country_id'] = destination_country_id[0].id if len(
                                    destination_country_id) else None

                        try:
                            customs_declaration_id = customs_declaration_obj.id
                            dec_goods_list['customs_dec_id'] = customs_declaration_id
                            dec_goods_list = {item: dec_goods_list[item] for item in dec_goods_list if
                                              dec_goods_list[item]}

                            cus_goods_list_obj = self.env['cus_center.dec_goods_list'].create(dec_goods_list)
                        except Exception, error_info:
                            _logger.error(
                                u'{} {}'.format(xml_message.decode('utf-8'), str(error_info).decode('utf-8')))

                            if not DEBUG:
                                shutil.move(xml_message, parse_error_xml_path)
                            continue
        except Exception, error_info:
            _logger.error(u'{} {}'.format(xml_message.decode('utf-8'), str(error_info).decode('utf-8')))
            if not DEBUG:
                shutil.copy2(xml_message, parse_error_xml_path)
                os.remove(xml_message)

            continue
        else:
            if not DEBUG:
                shutil.copy2(xml_message, backup_xml_path)
                os.remove(xml_message)
            _logger.info(u'Had parsed the xml message %s' % xml_message.decode('utf-8'))


def parse_customs_dec_edoc_xml(self):
    """ 从客户给物流云发送的随附单据文件夹中，解析随附单据报文（解析入库后，给相应的附件模型data赋值）"""
    """ 自动解析随附单据入库 从随附单据报文到报关单 反向查找"""
    # company_xml_parse_path = '0000016165'  # 做成前端界面可配置

    # 先判断随附单据队列模型里是否有数据
    edoc_queue_ids = self.env['customs_center.edoc_queue'].search([])
    if not edoc_queue_ids:
        return

    customs_dec_model_dic = self.env['customs_center.customs_dec'].default_get(
        ['dec_company_customs_code'])  # 获取报关单模型对象
    company_xml_parse_path = customs_dec_model_dic.get(
        'dec_company_customs_code')  # 获取配置信息中的 申报单位海关编码 作为解析路径

    parse_xml_path = os.path.join(PARSE_CUS_TO_WLY_PATH, company_xml_parse_path.encode('utf-8'))  # 新光原始报文解析目录
    parse_attach_path = os.path.join(PARSE_CUS_TO_WLY_ATTACH_PATH,
                                     company_xml_parse_path.encode('utf-8'))  # 新光随附单据解析目录
    parse_error_xml_path = os.path.join(PARSE_SEND_ERROR_XML_PATH, company_xml_parse_path.encode('utf-8'))
    backup_xml_path = os.path.join(BACKUP_SEND_XML_PATH, company_xml_parse_path.encode('utf-8'))  # 新光原始报文备份目录
    backup_attach_xml_path = os.path.join(BACKUP_SEND_ATTACH_XML_PATH,
                                          company_xml_parse_path.encode('utf-8'))  # 新光随附单据报文备份目录

    # 检查并生成相应的目录
    check_and_mkdir(parse_xml_path, parse_attach_path, parse_error_xml_path, backup_xml_path,
                    backup_attach_xml_path)

    # 首先解析随附单据目录的文件 可能多个附件
    attach_files = os.listdir(parse_attach_path)
    attach_files_list = {attach_filename.split('$')[0]: attach_filename for attach_filename in attach_files if
                         attach_filename.endswith('.xml')}

    if not attach_files_list:
        return True
    # attach_files = {os.path.join(parse_attach_path, i) for i in attach_files_list}

    # 读文件，用lxml解析报文
    attach_ids = []  # 附件id用于将解析的随附单据加在 随附单据拖拽上传page页
    attach_name_list = []
    # edoc_queue_ids = edoc_queue_ids.ids
    for edoc_queue_obj in edoc_queue_ids:
        name = edoc_queue_obj.edoc_id
        datas_fname = edoc_queue_obj.edoc_id
        dec_edoc_type = edoc_queue_obj.edoc_code
        cus_dec_id = edoc_queue_obj.cus_dec_id

        if name not in attach_files_list:
            continue
        xml_attach_message = os.path.join(parse_attach_path, attach_files_list[name])
        with open(xml_attach_message, 'r') as f:
            attach_xml_str = str(f.read())
            attach_xml_str1 = attach_xml_str.replace('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"', '')
            attach_xml_str = attach_xml_str1.replace('xsi:nil="true"', '')
            # print xml_str
            root = etree.fromstring(attach_xml_str)  # 打开xml文档

            root_name = etree.QName(root).localname
            print(root_name)  # 根标签 Data
            xml_attach_message_dic = {}  # 随附单据报文中的数据  即将xml随附单据TcsData标签部分 转换为字典形式
            if root_name == u'Data':
                attach_data_node = root.xpath('.//TcsData')
                for child in attach_data_node[0]:
                    xml_attach_message_dic[child.tag] = child.text
            attach_name_in_xml = xml_attach_message_dic.get('FILE_NAME', None)  # 获取随附单据报文中的文件名
            binary_data = xml_attach_message_dic.get('BINARY_DATA', None)  # 获取随附单据报文中的二进制数据
            trade_file_name = xml_attach_message_dic.get('TRADE_FILE_NAME', None)  # 获取随附单据报文中的trade file name

            # # 根据上述获取的附件名称 在附件模型中查找 对应的附件ID
            # attach_id = self.env['ir.attachment'].search([('res_model', '=', 'customs_center.customs_dec'),('name', '=', attach_name_in_xml)])
            # print("*******************^^6666666665555555555555666666666666**********************")
            # print(attach_id)
            # # 根据附件ID 找到对应的报关单ID
            # res_id = attach_id.res_id
            # print("*******************^^66666666666666666666666666666666**********************")
            # print(res_id)

            # 根据队列里的内容创建附件， 并删除相应的记录
            if attach_name_in_xml == name:
                attach_file_obj = self.env['ir.attachment'].create({
                    'name': trade_file_name,  # 该字段 用于前端界面显示
                    'datas_fname': datas_fname,
                    'extension': 'pdf',
                    'res_model': 'customs_center.customs_dec',
                    'res_id': cus_dec_id,
                    'dec_edoc_type': dec_edoc_type,
                    'datas': binary_data,
                    'description': name
                })

                edoc_queue_obj.unlink()
                attach_name_list.append(xml_attach_message)

                attach_ids.append(attach_file_obj.id)
                # 附件id用于将解析的随附单据加在 随附单据拖拽上传page页
                customs_dec_model_obj = self.env['customs_center.customs_dec'].search([('id', '=', cus_dec_id)])
                customs_dec_model_obj.information_attachment_ids = [(6, 0, attach_ids)]


                # # 根据上方找到的报关单ID 找到该报关单对应的附件列表
                # information_attachment_ids = self.env['ir.attachment'].search(
                #     [('res_model', '=', 'customs_center.customs_dec'), ('res_id', '=', res_id)])  # 取得附件list
                # print(information_attachment_ids)
                # for i in information_attachment_ids:
                #     attach_name = i.name
                #     attach_name_list.append(attach_name)
                #
                #     if attach_name == attach_name_in_xml:
                #         new_attachment = self.env['ir.attachment'].search(
                #             [('res_model', '=', 'customs_center.customs_dec'), ('res_id', '=', res_id),
                #              ('name', '=', attach_name)]).update({'datas': binary_data})

    # 将解析成功的随附单据报文 移动到随附单据备份目录
    for xml_attach_message in attach_name_list:  # xml_attach_message是单据名
        if not DEBUG:
            shutil.copy2(xml_attach_message, backup_attach_xml_path)
            os.remove(xml_attach_message)
        _logger.info(
            u'Had parsed the attach xml message %s' % xml_attach_message.decode('utf-8'))
