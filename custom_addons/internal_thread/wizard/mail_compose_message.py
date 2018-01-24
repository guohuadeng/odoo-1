# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class mail_compose_message(models.TransientModel):
    _inherit = 'mail.compose.message'

    send_only_internal = fields.Boolean(string='Send only for selected users', default=True)

    @api.multi
    def send_mail(self, auto_commit=False):
        # context = self.env.context.copy()
        for wizard in self:
            if wizard.send_only_internal:
                return super(
                    mail_compose_message,
                    self.with_context(put_this_subtype_instead='internal_thread.mt_internal_mes'),
                ).send_mail(auto_commit=auto_commit)
        return super(mail_compose_message, self).send_mail(auto_commit=auto_commit)

