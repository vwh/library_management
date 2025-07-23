from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class LibraryMembership(models.Model):
    _name = 'library.membership'
    _description = 'Library Membership'

    # Core membership fields
    partner_id = fields.Many2one('res.partner', string='Member', required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    product_id = fields.Many2one('product.product', string='Membership Product')
    
    # Membership lifecycle states
    state = fields.Selection([
        ('draft', 'Draft'),        # Created but not paid
        ('active', 'Active'),      # Paid and active
        ('expired', 'Expired'),    # Past end date
        ('cancelled', 'Cancelled'), # Manually cancelled
    ], string='State', default='draft')
    
    # Auto-computed end date based on start date + 1 year
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)

    @api.depends('start_date', 'product_id', 'state')
    def _compute_end_date(self):
        """Calculate membership end date (start date + 1 year) for active memberships"""
        for membership in self:
            if membership.start_date and membership.product_id and membership.state == 'active':
                # Add 1 year to start date
                start_date = fields.Date.from_string(membership.start_date)
                membership.end_date = start_date + relativedelta(years=1)
            else:
                # Clear end date for non-active memberships
                membership.end_date = False

    @api.model
    def create(self, vals):
        """Override create to handle initial membership setup"""
        membership = super(LibraryMembership, self).create(vals)
        
        # Ensure end_date is computed for active memberships
        if membership.state == 'active':
            membership._compute_end_date()
            
        return membership

    def write(self, vals):
        """Override write to handle state changes"""
        res = super(LibraryMembership, self).write(vals)
        
        # Recompute end_date when membership becomes active
        if 'state' in vals and vals['state'] == 'active':
            self._compute_end_date()
            
        return res
