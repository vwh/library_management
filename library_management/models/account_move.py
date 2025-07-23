import logging
from odoo import fields, models, tools

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_invoice_in_payment(self):
        """Called when invoice enters 'in payment' state"""
        res = super().action_invoice_in_payment()
        
        # Activate memberships early if configured
        if tools.config.get('library_membership.activate_on_in_payment'):
            self._activate_related_memberships()
        
        return res

    def action_invoice_paid(self):
        """Called when invoice is fully paid and reconciled"""
        res = super().action_invoice_paid()
        
        # Always activate memberships when fully paid
        self._activate_related_memberships()
        
        return res

    def _activate_related_memberships(self):
        """
        Find and activate draft memberships for paid membership products
        """
        membership_model = self.env['library.membership']
        
        # Process only customer invoices
        for move in self.filtered(lambda m: m.move_type == 'out_invoice'):
            # Check each invoice line
            for line in move.invoice_line_ids:
                # Skip non-membership products
                if not getattr(line.product_id, 'is_membership_product', False):
                    continue

                # Search for draft membership to activate
                domain = [
                    ('partner_id', '=', move.partner_id.id),
                    ('product_id', '=', line.product_id.id),
                    ('state', '=', 'draft'),
                ]
                
                membership = membership_model.search(domain, order='create_date desc', limit=1)
                
                if membership:
                    # Activate the membership
                    membership.state = 'active'
                    membership.activation_date = fields.Date.context_today(self)
                    
                    _logger.info(
                        "Activated membership %s for partner %s",
                        membership.display_name,
                        move.partner_id.display_name,
                    )
                else:
                    # Log warning if no draft membership found
                    _logger.warning(
                        "Unable to locate draft membership for partner %s and product %s",
                        move.partner_id.display_name,
                        line.product_id.display_name,
                    )
