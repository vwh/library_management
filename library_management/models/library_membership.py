from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class LibraryMembership(models.Model):
    _name = 'library.membership'
    _description = 'Library Membership'

    partner_id = fields.Many2one('res.partner', string='Member', required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft')
    product_id = fields.Many2one('product.product', string='Membership Product')
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)

    @api.depends('start_date', 'product_id', 'state')
    def _compute_end_date(self):
        for membership in self:
            if membership.start_date and membership.product_id and membership.state == 'active':
                # Calculate end date as 1 year from start date
                start_date = fields.Date.from_string(membership.start_date)
                membership.end_date = start_date + relativedelta(years=1)
            else:
                membership.end_date = False

    @api.model
    def create(self, vals):
        """Override create to handle initial membership creation"""
        membership = super(LibraryMembership, self).create(vals)
        # If created as active, ensure end_date is computed
        if membership.state == 'active':
            membership._compute_end_date()
        return membership

    def write(self, vals):
        """Override write to handle state changes"""
        res = super(LibraryMembership, self).write(vals)
        # If state is changed to active, recompute end_date
        if 'state' in vals and vals['state'] == 'active':
            self._compute_end_date()
        return res