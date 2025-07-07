from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    author_id = fields.Many2one('library.author', string='Author', required=True)
    description = fields.Text(string='Description')
    publish_date = fields.Date(string='Publish Date')
    is_available = fields.Boolean(string='Available', compute='_compute_is_available', store=True)

    borrowing_ids = fields.One2many('library.borrowing', 'book_id', string='Borrowings')

    @api.depends('borrowing_ids.is_returned')
    def _compute_is_available(self):
        for book in self:
            book.is_available = not any(not borrowing.is_returned for borrowing in book.borrowing_ids)
