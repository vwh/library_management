
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                if line.product_id.is_membership_product:
                    self.env['library.membership'].create({
                        'partner_id': order.partner_id.id,
                        'product_id': line.product_id.id,
                        'start_date': fields.Date.context_today(self),
                    })
        return res

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_membership_product = fields.Boolean(string='Is Membership Product')
