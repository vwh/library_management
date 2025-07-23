import logging
from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    def action_invoice_in_payment(self):
        res = super().action_invoice_in_payment()
        if tools.config.get('library_membership.activate_on_in_payment'):
            self._activate_related_memberships()
        return res

    def action_invoice_paid(self):
        res = super().action_invoice_paid()
        # Always activate on full payment
        self._activate_related_memberships()
        return res

    def _activate_related_memberships(self):
        """
        Iterate through invoice lines flagged as `is_membership_product`
        and flip the latest draft membership to active.
        """
        membership_model = self.env['library.membership']
        for move in self.filtered(lambda m: m.move_type == 'out_invoice'):
            for line in move.invoice_line_ids:
                if not getattr(line.product_id, 'is_membership_product', False):
                    continue

                domain = [
                    ('partner_id', '=', move.partner_id.id),
                    ('product_id', '=', line.product_id.id),
                    ('state', '=', 'draft'),
                ]
                membership = membership_model.search(domain, order='create_date desc', limit=1)
                if membership:
                    membership.state = 'active'
                    membership.activation_date = fields.Date.context_today(self)
                    # Optionally compute expiry:
                    # membership.expiry_date = fields.Date.add(...)
                    _logger.info(
                        "Activated membership %s for partner %s",
                        membership.display_name,
                        move.partner_id.display_name,
                    )
                else:
                    _logger.warning(
                        "Unable to locate draft membership for partner %s and product %s",
                        move.partner_id.display_name,
                        line.product_id.display_name,
                    )
