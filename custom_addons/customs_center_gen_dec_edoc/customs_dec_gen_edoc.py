# –*– coding: utf–8 –*–

from odoo import models, fields, api

class TodoTask(models.Model):
    _inherit = 'cus_center.customs_dec'

    @api.multi
    def gen_dec_edocs(self):
        self.env['report'].get_pdf([self.id],"customs_center.report_customs_dec_edoc_packing_list_template"), 'pdf'
        self.env['report'].get_pdf([self.id], "customs_center.report_customs_dec_edoc_invoice_template"), 'pdf'
        self.env['report'].get_pdf([self.id], "customs_center.report_customs_dec_edoc_contract_template"), 'pdf'
        self.env['report'].get_pdf([self.id], "customs_center.report_customs_dec_edoc_attorney_template"), 'pdf'

        att_model = self.env['ir.attachment']  # 获取附件模型
        for obj in self:
            query = [('res_model', '=', self._name), ('res_id', '=', obj.id)]

        list = att_model.search(query)  # 取得附件list
        ids = []
        if len(list) > 0:
            for i in list:
                ids.append(i.id)

        if len(list) > 0:
            for i in list:
                self.information_attachment_ids = [(6, 0, ids)]
                edoc = self.env['ir.attachment'].search([('id', '=', i.id)])
                dec_edoc_type = ""
                description = ""

                # 识别随附单据类型
                if "箱单" in edoc.name or "packing" in edoc.name:
                    dec_edoc_type = "00000002"
                    #description = "xiang_dan"
                if "发票" in edoc.name or "invoice" in edoc.name:
                    dec_edoc_type = "00000001"
                    #description = "fa_piao"
                if "合同" in edoc.name or "contract" in edoc.name:
                    dec_edoc_type = "00000004"
                    #description = "he_tong"
                if "委托书" in edoc.name or "attorney" in edoc.name:
                    dec_edoc_type = "10000001"
                    # description = "wei_tuo_shu"

                self.env['ir.attachment'].search(
                    [('id', '=', i.id)]).update({'extension': 'pdf',
                                                 'dec_edoc_type': dec_edoc_type, 'description': description})