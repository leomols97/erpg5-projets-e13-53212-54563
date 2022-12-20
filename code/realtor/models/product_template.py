from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Apartment product template'

    quantity = fields.Integer("Quantité d'appartements") # Vient de la consigne "Consultez le produit et notez la quantité disponible en stock"

    apartment_id = fields.Many2one('realtor.apartment', string='Appartement(s) associé(s) à un produit') #, compute='_compute_apartment_price') #, required=False)
    stock_id = fields.Many2one('stock.inventory', string='Stock associé au produit')

    @api.onchange('apartment_id')
    @api.constrains('quantity')
    def _compute_apartment_price(self):
        self.price = self.apartment_id.expected_price

    # @api.constrains('quantity', 'apartment_id')
    # def _compute_apartment_id(self):
    #     for record in self :
    #         if(s)