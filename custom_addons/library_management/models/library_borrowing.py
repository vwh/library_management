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

    def action_return_book(self):
        for borrowing in self:
            if not borrowing.is_returned:
                borrowing.is_returned = True
            else:
                raise ValidationError('This book has already been returned.')
        return True
