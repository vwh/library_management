
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    membership_ids = fields.One2many('library.membership', 'partner_id', string='Memberships')
    is_member = fields.Boolean(string='Active Member', compute='_compute_is_member', store=True)

    @api.depends('membership_ids.state')
    def _compute_is_member(self):
        for partner in self:
            partner.is_member = any(membership.state == 'active' for membership in partner.membership_ids)
