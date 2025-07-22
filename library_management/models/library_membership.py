
from odoo import models, fields

class LibraryMembership(models.Model):
    _name = 'library.membership'
    _description = 'Library Membership'

    partner_id = fields.Many2one('res.partner', string='Member', required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    end_date = fields.Date(string='End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft')
    product_id = fields.Many2one('product.product', string='Membership Product')

    def _compute_end_date(self):
        for membership in self:
            if membership.start_date and membership.product_id:
                # Assuming the membership duration is 1 year
                membership.end_date = fields.Date.from_string(membership.start_date).replace(year=membership.start_date.year + 1)
            else:
                membership.end_date = False
