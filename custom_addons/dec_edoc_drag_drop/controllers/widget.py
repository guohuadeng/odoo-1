# –*– coding: utf–8 –*–
from odoo import models,api,fields

class widget_data(models.Model):
    _inherit = 'ir.attachment'

    extension = fields.Char()
    sortable = fields.Integer()

    @api.model
    def upload_dragndrop_dec_edoc(self,res_model_id,res_model_name,name, base64, extension, sortable):
        Model = self

        dec_edoc_type = ""
        description = ""

        # 识别随附单据类型
        if "箱单" in name or "packing" in name:
            dec_edoc_type = "00000002"
            description = "xiang_dan"
        if "发票" in name or "invoice" in name:
            dec_edoc_type = "00000001"
            description = "fa_piao"
        if "合同" in name or "contract" in name:
            dec_edoc_type = "00000004"
            description = "he_tong"
        if "委托书" in name or "attorney" in name:
            dec_edoc_type = "10000001"
            description = "wei_tuo_shu"

        try:
            attachment_id = Model.create({
                'name': name,
                'datas': base64,
                'extension': extension,
                'dec_edoc_type': dec_edoc_type,
                'datas_fname': name,
                'res_model': res_model_name,
                # 'description': '',
                'description': description,
                'sortable': sortable,
                'res_id': res_model_id
            })
            args = {
                'filename': name,
                'id':  attachment_id
            }
        except Exception:
            args = {'error': "Something horrible happened"}
        # return out % (simplejson.dumps(callback), simplejson.dumps(args))
        return attachment_id.id

    @api.model
    def attachment_update_description(self, id, description):
        attachment_id = self.env['ir.attachment'].search([('id', '=', int(id))])[0]
        attachment_id.description = description

    @api.model
    def attachment_update_dec_edoc_type(self, id, dec_edoc_type):
        attachment_id = self.env['ir.attachment'].search([('id', '=', int(id))])[0]
        attachment_id.dec_edoc_type=dec_edoc_type

    @api.model
    def update_sort_attachment(self, attachments_ids):
        attachments = self.env['ir.attachment'].search([('id', 'in', attachments_ids)])
        for attach in attachments:
            #cambio il campo sortable
            sort_number = attachments_ids.index(str(attach.id))
            attach.sortable = sort_number


class widget_ir_config_parameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    def get_base_url(self):
        base_url = ""
        config_parameter_ids = self.env['ir.config_parameter'].search([('key', '=', 'web.base.url')])[0]
        if config_parameter_ids.value:
            base_url = config_parameter_ids.value
        return base_url

widget_data()
widget_ir_config_parameter()