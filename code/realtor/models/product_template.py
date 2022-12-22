from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Apartment product template'

    quantity = fields.Integer('Quantité d\'appartements') # Vient de la consigne "Consultez le produit et notez la quantité disponible en stock"

    apartment_id = fields.Many2one('realtor.apartment', string='Appartement associé à un produit')
    stock_id = fields.Many2one('stock.inventory', string='Stock associé au produit')
    