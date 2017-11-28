# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)

class AllMessage(models.Model):

    _inherit = "mail.message"
    allmessage = fields.Boolean(
        'All Messages', compute='_get_allmessage', search='_search_allmessage',
        help='All Messages')

    @api.multi
    def _get_allmessage(self):
        """ Need action on a mail.message = notified on my channel """
        all_messages = self.sudo().search([])
        for message in self:
            message.allmessage = message in all_messages

    @api.model
    def _search_allmessage(self, operator, operand):

        return ['|',('starred_partner_ids', 'in', [self.env.user.partner_id.id]),  ('needaction_partner_ids', 'in', [self.env.user.partner_id.id])]

    @api.model
    def mark_all_as_read(self, channel_ids=None, domain=None):
        """ Remove all needactions of the current partner. If channel_ids is
            given, restrict to messages written in one of those channels. """
        partner_id = self.env.user.partner_id.id
        delete_mode = 0  # delete employee notifs, keep customer ones
        if domain is None and delete_mode:
            query = "DELETE FROM mail_message_res_partner_needaction_rel WHERE res_partner_id IN %s"
            args = [(partner_id,)]
            if channel_ids:
                query += """
                    AND mail_message_id in
                        (SELECT mail_message_id
                        FROM mail_message_mail_channel_rel
                        WHERE mail_channel_id in %s)"""
                args += [tuple(channel_ids)]
            query += " RETURNING mail_message_id as id"
            self._cr.execute(query, args)
            self.invalidate_cache()

            ids = [m['id'] for m in self._cr.dictfetchall()]
        else:
            # not really efficient method: it does one db request for the
            # search, and one for each message in the result set to remove the
            # current user from the relation.
            msg_domain = [('needaction_partner_ids', 'in', partner_id)]
            if channel_ids:
                msg_domain += [('channel_ids', 'in', channel_ids)]
            unread_messages = self.search(expression.AND([msg_domain, domain]))
            notifications = self.env['mail.notification'].sudo().search([
                ('mail_message_id', 'in', unread_messages.ids),
                ('res_partner_id', '=', self.env.user.partner_id.id),
                ('is_read', '=', False)])
            if delete_mode:
                notifications.unlink()
            else:
                notifications.write({'is_read': True})
            ids = unread_messages.mapped('id')

        notification = {'type': 'mark_as_read', 'message_ids': ids, 'channel_ids': channel_ids}
        self.env['bus.bus'].sendone((self._cr.dbname, 'res.partner', self.env.user.partner_id.id), notification)

        return ids
    @api.multi
    def set_message_done(self):
        """ Remove the needaction from messages for the current partner. """

        partner_id = self.env.user.partner_id
        delete_mode = 0  # delete employee notifs, keep customer ones

        notifications = self.env['mail.notification'].sudo().search([
            ('mail_message_id', 'in', self.ids),
            ('res_partner_id', '=', partner_id.id),
            ('is_read', '=', False)])

        if not notifications:
            return

        # notifies changes in messages through the bus.  To minimize the number of
        # notifications, we need to group the messages depending on their channel_ids
        groups = []
        messages = notifications.mapped('mail_message_id')
        current_channel_ids = messages[0].channel_ids
        current_group = []
        for record in messages:
            if record.channel_ids == current_channel_ids:
                current_group.append(record.id)
            else:
                groups.append((current_group, current_channel_ids))
                current_group = [record.id]
                current_channel_ids = record.channel_ids

        groups.append((current_group, current_channel_ids))
        current_group = [record.id]
        current_channel_ids = record.channel_ids

        if delete_mode:
            notifications.unlink()
        else:
            notifications.write({'is_read': True})

        for (msg_ids, channel_ids) in groups:
            notification = {'type': 'mark_as_read', 'message_ids': msg_ids, 'channel_ids': [c.id for c in channel_ids]}
            self.env['bus.bus'].sendone((self._cr.dbname, 'res.partner', partner_id.id), notification)

    @api.multi
    def message_format(self):

        message_values = self.read([
            'id', 'body', 'date', 'author_id', 'email_from','needaction',  # base message fields
            'message_type', 'subtype_id', 'subject',  # message specific
            'model', 'res_id', 'record_name',  # document related
            'channel_ids', 'partner_ids',  # recipients
            'needaction_partner_ids',  # list of partner ids for whom the message is a needaction
            'starred_partner_ids',  # list of partner ids for whom the message is starred
        ])
        message_tree = dict((m.id, m) for m in self.sudo())
        self._message_read_dict_postprocess(message_values, message_tree)

        # add subtype data (is_note flag, subtype_description). Do it as sudo
        # because portal / public may have to look for internal subtypes
        subtypes = self.env['mail.message.subtype'].sudo().search(
            [('id', 'in', [msg['subtype_id'][0] for msg in message_values if msg['subtype_id']])]).read(['internal', 'description'])
        subtypes_dict = dict((subtype['id'], subtype) for subtype in subtypes)
        for message in message_values:
            message['is_note'] = message['subtype_id'] and subtypes_dict[message['subtype_id'][0]]['internal']
            message['subtype_description'] = message['subtype_id'] and subtypes_dict[message['subtype_id'][0]]['description']
        return message_values