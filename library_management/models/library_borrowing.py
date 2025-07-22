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

    # Onchange method to auto-fill return date 7 days after borrow date
    @api.onchange('borrow_date')
    def _onchange_borrow_date(self):
        if self.borrow_date:
            self.return_date = self.borrow_date + timedelta(days=7)

    @api.constrains('borrower_id')
    def _check_member_is_active(self):
        for borrowing in self:
            if not borrowing.borrower_id.is_member:
                raise ValidationError(
                    f"The borrower {borrowing.borrower_id.name} is not an active member."
                )

    # Constraint to check book availability before allowing a new borrowing
    @api.constrains('book_id', 'is_returned')
    def _check_book_availability(self):
        for borrowing in self:
            # If the current borrowing is not yet returned
            if not borrowing.is_returned:
                # Search for other unreturned borrowings of the same book
                other_borrowings = self.search([
                    ('book_id', '=', borrowing.book_id.id),
                    ('is_returned', '=', False),
                    ('id', '!=', borrowing.id) # Exclude the current borrowing record
                ])
                # If other unreturned borrowings exist, raise a validation error
                if other_borrowings:
                    raise ValidationError(
                        f"The book '{borrowing.book_id.name}' is already borrowed by {other_borrowings[0].borrower_id.name} "
                        f"and has not been returned yet."
                    )

    # Override the create method to add a check for book availability
    @api.model_create_multi
    def create(self, vals_list):
        # Ensure vals_list is always a list, even if a single dict is passed
        if not isinstance(vals_list, list):
            vals_list = [vals_list]

        for vals in vals_list:
            if vals.get('book_id'):
                book = self.env['library.book'].browse(vals['book_id'])
                # If the book is not available, prevent borrowing
                if not book.is_available:
                    raise ValidationError(
                        f"The book '{book.name}' is not available for borrowing."
                    )
        return super().create(vals_list)

    # Action method to mark a book as returned
    def action_return_book(self):
        for borrowing in self:
            if not borrowing.is_returned:
                borrowing.is_returned = True
            else:
                raise ValidationError('This book has already been returned.')
        return True