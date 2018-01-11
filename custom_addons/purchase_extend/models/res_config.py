# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'purchase.config.settings'

    default_notes = fields.Text(default_model='purchase.order')
