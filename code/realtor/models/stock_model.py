from odoo import fields, models

class Stock(models.Model):
    _inherit = 'stock.inventory'
    _description = 'Stocker plusieurs produits'

    product_ids = fields.One2many('product.template', 'stock_id',
                                  string='Plusieurs produits associés au stock',
                                  # Readonly car il est demandé de ne pas ajouter des produits à un sotck lors de sa création, mais d'associer des produits à un stocks lors de leur création
                                  readonly=True)