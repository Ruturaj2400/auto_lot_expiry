from odoo import models, fields

class StockQuant(models.Model):
    _inherit = "stock.quant"

    cost = fields.Float(
        related="product_id.standard_price",
        string="Cost",
        readonly=True
    )

    sales_price = fields.Float(
        related="product_id.list_price",
        string="Sales Price",
        readonly=True
    )

    purchase_price = fields.Float(
        related="product_id.standard_price",
        string="Purchase Price",
        readonly=True
    )