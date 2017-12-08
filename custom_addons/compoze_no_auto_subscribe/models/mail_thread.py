# -*- coding: utf-8 -*-

import logging

from odoo import exceptions, SUPERUSER_ID
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class mail_thread(models.AbstractModel):
    _inherit = "mail.thread"
    
    @api.multi
    def message_get_suggested_recipients(self):
        """ Returns suggested recipients for ids. Those are a list of
        tuple (partner_id, partner_name, reason), to be managed by Chatter. """
        
        model = self.env.context.get('thread_model', False) if self._name == 'mail.thread' else self._name
        if model and model != self._name and hasattr(self.env[model], 'message_post'):
            del context['thread_model']
            return self.env[model].message_get_suggested_recipients()

        result = dict((res_id, []) for res_id in self.ids)
        if 'user_id' in self._fields:
            for obj in self.sudo():  # SUPERUSER because of a read on res.users that would crash otherwise
                if not obj.user_id or not obj.user_id.partner_id:
                    continue
                obj._message_add_suggested_recipient(
                    result,
                    partner=obj.user_id.partner_id,
                    reason=self._fields['user_id'].string,
                )

        if 'partner_id' in self._fields:
            for obj in self.sudo():  # SUPERUSER because of a read on res.users that would crash otherwise
                if obj.partner_id:
                    self._message_add_suggested_recipient(
                        result,
                        partner=obj.partner_id,
                        reason=self._fields['partner_id'].string,
                    )

        return result
