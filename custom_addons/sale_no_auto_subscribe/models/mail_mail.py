# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

from odoo.addons.portal_sale.models.mail_mail import Mail as mail_portal


class mail_mail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def _postprocess_sent_message(self, mail_sent=True):
        return super(mail_portal, self)._postprocess_sent_message(mail_sent=mail_sent)
