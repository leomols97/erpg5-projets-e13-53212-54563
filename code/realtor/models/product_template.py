from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Apartment product template'

    quantity = fields.Integer("Quantité d'appartements") # Vient de la consigne "Consultez le produit et notez la quantité disponible en stock"

    apartment_id = fields.Many2one('realtor.apartment', string='Appartement(s) associé(s) à un produit',
                                   required=True) #, compute='_compute_apartment_price')
    stock_id = fields.Many2one('stock.inventory', string='Stock associé au produit', required=True)


    @api.onchange('apartment_id')
    def _compute_apartment_price(self):
        self.list_price = self.apartment_id.expected_price

    # @api.constrains('apartment_id')
    # def _compute_apartment_price_error(self):
    #     if self.list_price != self.apartment_id.expected_price:
    #         raise ValidationError("Le prix du produit doit être égal au prix attendu de l'appartement. Resélectionnez l'appartement pour avoir le bon prix.")

    @api.onchange('quantity')
    def _compute_product_quantity(self):
        self.qty_available = self.quantity

    # @api.constrains('quantity')
    # def _compute_product_quantity_error(self):
    #     if self.quantity < 1:
    #         raise ValidationError("La quantité du produit doit être supérieure à 0. A quoi bon créer un produit si il n'y a pas d'appartement ?")

    # @api.constrains('quantity', 'apartment_id')
    # def _compute_apartment_id(self):
    #     for record in self :
    #         if(s)