from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class LibraryBorrowing(models.Model):
    _name = 'library.borrowing'
    _description = 'Library Borrowing'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.context_today)
    return_date = fields.Date(string='Return Date')
    is_returned = fields.Boolean(string='Returned', default=False)

    @api.onchange('borrow_date')
    def _onchange_borrow_date(self):
        if self.borrow_date:
            self.return_date = self.borrow_date + timedelta(days=7)

    @api.constrains('book_id', 'is_returned')
    def _check_book_availability(self):
        for borrowing in self:
            if not borrowing.is_returned:
                other_borrowings = self.search([
                    ('book_id', '=', borrowing.book_id.id),
                    ('is_returned', '=', False),
                    ('id', '!=', borrowing.id)
                ])
                if other_borrowings:
                    raise ValidationError(
                        f"The book '{borrowing.book_id.name}' is already borrowed by {other_borrowings[0].borrower_id.name} "
                        f"and has not been returned yet."
                    )

    @api.model
    def create(self, vals):
        if vals.get('book_id'):
            book = self.env['library.book'].browse(vals['book_id'])
            if not book.is_available:
                raise ValidationError(
                    f"The book '{book.name}' is not available for borrowing."
                )
        return super().create(vals)

    def action_return_book(self):
        for borrowing in self:
            if not borrowing.is_returned:
                borrowing.is_returned = True
            else:
                raise ValidationError('This book has already been returned.')
        return True