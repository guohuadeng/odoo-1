# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

from odoo.addons.portal_sale.models.sale_order import SaleOrder as sale_order_portal

class sale_order(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        return super(sale_order_portal, self).action_confirm()

    sale_order_portal.action_confirm = action_confirm
