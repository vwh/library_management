
from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for move in self:
            if move.move_type == 'out_invoice' and move.payment_state == 'paid':
                for line in move.invoice_line_ids:
                    if line.product_id.is_membership_product:
                        membership = self.env['library.membership'].search([
                            ('partner_id', '=', move.partner_id.id),
                            ('product_id', '=', line.product_id.id),
                            ('state', '=', 'draft'),
                        ], limit=1)
                        if membership:
                            membership.write({'state': 'active'})
        return res
