from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    duration_type = fields.Selection([
        ('long', 'Long-Term Product'),
        ('short', 'Short-Term Product')
    ], string="Duration Classification", default='short')
    