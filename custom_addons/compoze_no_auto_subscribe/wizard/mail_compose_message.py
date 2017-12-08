# -*- coding: utf-8 -*-

import logging

from odoo import exceptions, SUPERUSER_ID
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class mail_compose_message(models.TransientModel):
    _inherit = 'mail.compose.message'

    subscribe_recipients = fields.Boolean(string='Subscribe recipients')

    @api.multi
    def send_mail(self, auto_commit=False):
        context = self.env.context.copy()
        for wizard in self:
            if not wizard.subscribe_recipients:
                return super(
                    mail_compose_message,
                    self.with_context(mail_post_autofollow=False, mail_create_nosubscribe=True),
                ).send_mail(auto_commit=auto_commit)
        return super(mail_compose_message, self).send_mail(auto_commit=auto_commit)
