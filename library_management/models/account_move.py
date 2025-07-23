from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    def reconcile(self):
        # Store moves that might become paid after reconciliation
        moves_to_check = self.mapped('move_id').filtered(
            lambda m: m.move_type == 'out_invoice' and m.payment_state != 'paid'
        )
        
        _logger.info(f"=== Before reconciliation: Found {len(moves_to_check)} invoices to check ===")
        
        # Perform the reconciliation
        res = super(AccountMoveLine, self).reconcile()
        
        # Check which moves became paid after reconciliation
        for move in moves_to_check:
            if move.payment_state == 'paid':
                _logger.info(f"Invoice {move.name} became paid after reconciliation")
                move._activate_related_memberships()
        
        return res

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def _activate_related_memberships(self):
        for move in self:
            if move.move_type == 'out_invoice' and move.payment_state == 'paid':
                _logger.info(f"Invoice {move.name} is paid, looking for memberships...")
                
                # Get the sale order from the invoice
                sale_orders = move.invoice_line_ids.sale_line_ids.order_id
                _logger.info(f"Related sale orders: {sale_orders.ids}")
                
                # Find memberships created from these sale orders
                memberships = self.env['library.membership'].search([
                    ('state', '=', 'draft')
                ])
                
                # Filter memberships that belong to the same partner as this invoice
                # FIX: Use partner_id instead of member_id
                related_memberships = memberships.filtered(
                    lambda m: m.partner_id == move.partner_id
                )
                
                _logger.info(f"Found {len(related_memberships)} memberships to activate for partner {move.partner_id.name}")
                
                for membership in related_memberships:
                    _logger.info(f"Activating membership {membership.id} for member {membership.partner_id.name}")
                    membership.write({
                        'state': 'active',
                        'activation_date': fields.Date.context_today(self),
                    })
                    membership._compute_end_date()
                    _logger.info(f"Membership {membership.id} activated successfully")

