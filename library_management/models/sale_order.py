from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """Override confirm action to create membership records when order contains membership products"""
        res = super(SaleOrder, self).action_confirm()
        
        # Process each confirmed order
        for order in self:
            # Check each order line for membership products
            for line in order.order_line:
                if line.product_id.is_membership_product:
                    # Create draft membership record
                    self.env['library.membership'].create({
                        'partner_id': order.partner_id.id,
                        'product_id': line.product_id.id,
                        'start_date': fields.Date.context_today(self),
                    })
        
        return res

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    # Flag to identify membership products
    is_membership_product = fields.Boolean(string='Is Membership Product')
