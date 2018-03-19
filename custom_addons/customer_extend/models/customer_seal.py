# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Customer(models.Model):
    _inherit = 'res.partner'
    # 公章
    seal_company = fields.Binary("seal_company", attachment=True,
                          help="This field holds the image used as avatar for this contact, limited to 1024x1024px", )
    # 法人章
    seal_legal_representative = fields.Binary("seal_legal_representative", attachment=True,
                          help="This field holds the image used as avatar for this contact, limited to 1024x1024px", )