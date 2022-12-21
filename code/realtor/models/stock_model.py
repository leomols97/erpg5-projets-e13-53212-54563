from odoo import fields, models

class Stock(models.Model):
    _inherit = 'stock.inventory'
    _description = 'Stocker plusieurs produits'

    product_ids = fields.One2many('product.template', 'stock_id', string='Plusieurs produits associés à un stock')

