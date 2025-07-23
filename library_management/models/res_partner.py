from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Relationship to show all memberships for this partner
    membership_ids = fields.One2many('library.membership', 'partner_id', string='Memberships')
    
    # Computed field to show if partner has any active memberships
    is_member = fields.Boolean(string='Active Member', compute='_compute_is_member', store=True)

    @api.depends('membership_ids')
    def _compute_is_member(self):
        """Compute if partner has any active memberships"""
        for partner in self:
            # Check if any membership is in active state
            partner.is_member = any(membership.state == 'active' for membership in partner.membership_ids)
