from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Apartment product template'

    quantity = fields.Float("Quantité d'appartements") # Vient de la consigne "Consultez le produit et notez la quantité disponible en stock"

    apartment_id = fields.Many2one('realtor.apartment', string='Appartement(s) associé(s) à un produit', require=True) #, compute='_compute_apartment_price')
    stock_id = fields.Many2one('stock.inventory', string='Stock associé au produit', required=True)

    @api.constrains('qty_available')
    def _compute_product_qty_available_error(self):
        """ Checks if the qty_available is not lower than 0 or 0"""
        if self.qty_available < 1:
            raise ValidationError(
                "La quantité du produit doit être supérieure à 0. A quoi bon créer un produit si il n'y a pas d'appartement ?")

    # @api.constrains('apartment_id')
    # def _compute_apartment_price_error(self):
    #     """ Checks if the price of the product is not different than the expected price of the apartment """
    #     if self.list_price != self.apartment_id.expected_price:
    #         raise ValidationError(
    #             "Le prix du produit doit être égal au prix attendu de l'appartement. Resélectionnez l'appartement pour avoir le bon prix.")

    @api.onchange('apartment_id', 'expected_price', 'quantity')
    def _compute_apartment_price(self):
        """ Sets the price, the qty_available and the name of the product to the expected price, qty_available and name of the apartment.
        Also sets the type of the product to 'product' for it to be a storable product"""
        # self.price = self.apartment_id.best_offer_price
        # self.standard_price = self.apartment_id.best_offer_price
        self.list_price = self.apartment_id.expected_price
        # self.qty_available = self.quantity
        # self.virtual_available = self.quantity
        # self.name = self.apartment_id.name
        self.type = 'product'