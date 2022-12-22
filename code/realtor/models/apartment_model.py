from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Apartment(models.Model):
    _name = 'realtor.apartment'
    _description = "Modèle d'un appartement"
    name = fields.Char(string="Nom de l'appartement", required=True)
    description = fields.Char(string="Description de l'apartment")
    image = fields.Binary(string='Image')
    expected_price = fields.Integer(string="Prix attendu", required=True)
    apartment_area = fields.Integer(string="Surface de l'appartement", required=True)
    terrace_area = fields.Integer(string="Surface de la terrasse", required=True)
    total_area = fields.Integer(string="Surface totale", compute='_compute_total_area')
    best_offer_price = fields.Integer(string="Meilleure offre", compute='_compute_min_price')
    disponibility = fields.Boolean(string="Disponible ?", default=False)
    date_creation = fields.Date(string="Date de création de l'appartement", default=datetime.today(), readonly=True)
    date_disponibility = fields.Date(string="Date de disponibilité de l'appartement", default=datetime.today() + relativedelta(months=3))

    seller = fields.Many2one('res.users', string="Vendeur")
    buyer = fields.Char(string="Acheteur potentiel")
    # best_buyer = fields.Many2one('res.partner', string='Acheteurs potentiels')
    # Les 2 fields suivants permettent, avec les fonctions 'compute_for_only_one_apartment' et 'asset_inverse_for_one_product' d'empêcher qu'un product soit associé à plusieurs apartment et inversement
    product_id = fields.Many2one('product.template', compute='compute_for_only_one_apartment', inverse='asset_inverse_for_one_product', string='Premier produit associé à cet appartement')
    product_ids = fields.One2many('product.template', 'apartment_id', string='Produits associés à cet appartement')

    @api.constrains('date_creation', 'date_disponibility')
    def _check_dates(self):
        """ Checks if the date of disponibility of the apartment is not lower than 3 months after the date of creation of the offer """
        if self.date_disponibility < (self.date_creation + relativedelta(months=3)):
            raise ValidationError( "La date de disponibilité doit être de minimum 3 mois après la création de l’appartement.'" )

    @api.constrains('expected_price')
    def _check_expected_price(self):
        """ Checks if the expected price is not lower than 0 """
        if self.expected_price <= 0:
            raise ValidationError('Entrez une valeur plus grande que 0 pour le prix attendu')

    @api.constrains('apartment_area')
    def _check_apartment_area(self):
        """ Checks if the apartment area is not lower than 0 """
        if self.apartment_area <= 0:
            raise ValidationError('Entrez une valeur plus grande que 0 pour la surface de l\'appartement')

    @api.constrains('terrace_area')
    def _check_terrace_area(self):
        """ Checks if the terrace area is not lower than 0 """
        if self.terrace_area <= 0:
            raise ValidationError('Entrez une valeur plus grande que 0 pour la surface de la terrasse')

    @api.constrains('total_area')
    @api.depends('apartment_area', 'terrace_area')
    def _check_total_area(self):
        """ Checks if the total area is the sum of the areas of the apartment and the terrace """
        if self.apartment_area + self.terrace_area != self.total_area:
            raise ValidationError(
                "La surface totale de l'appartement doit valloir la somme de la surface de la terrasse et de celle de l'appartement")

    @api.depends('apartment_area', 'terrace_area')
    def _compute_total_area(self):
        """ Computes the total surface of an apartment """
        for record in self:
            record.total_area = record.terrace_area + record.apartment_area

    @api.depends('expected_price', 'best_offer_price')
    def _compute_min_price(self):
        """ Checks if the best offer is not lower than 90% of the expected price """
        for record in self:
            record.best_offer_price = 0
            record.buyer = None
            offer_price_min = record.expected_price * 0.9
            potential_buyers = self.env['res.partner'].search([('apartment', 'in', record.name)])
            best_buyer = None
            buyer_offer = 0
            for buyer in potential_buyers:
                if buyer.offer_price > buyer_offer and buyer.offer_price >= offer_price_min:
                    buyer_offer = buyer.offer_price
                    best_buyer = buyer.name
            record.buyer = best_buyer
            record.best_offer_price = buyer_offer

            # if record.best_offer_price < record.expected_price * 0.9:
            #     raise ValidationError('La meilleure offre ne peut être inférieure à 90% du prix attendu')

    # @api.depends('best_offer_price')
    # def _compute_best_offer_price(self):
    #     """ Looks for the best offer price for an apartment """
    #     for record in self:
    #         for best_offer_price in record:
    #             if record.price < best_offer_price.price:
    #                 record.buyer = best_offer_price.buyer
    #                 record.best_offer_price = best_offer_price.price

    @api.constrains('date_creation', 'date_disponibility', 'disponibility')
    def _check_disponibility(self):
        """ Checks if the date of disponibility of the apartment is not lower than 3 months after the date of creation of the offer """
        if self.disponibility and self.date_disponibility < (self.date_creation + relativedelta(months=3)) :
            raise ValidationError( "La date de disponibilité doit être de minimum 3 mois après la création de l’appartement. L'appartement ne peut donc pas être disponible !")

    # @api.depends('product_ids')
    # def compute_for_only_one_apartment(self):
    #     """ From the apartment, makes the program save only one product at a time """
    #     if len(self.product_ids) > 0:
    #         self.product_id = self.product_ids[0]
    #
    # def asset_inverse_for_one_product(self):
    #     """ From the product, makes the program save only one apartment at a time """
    #     if len(self.product_ids) > 0:
    #         # delete previous reference
    #         asset = self.env['product.template'].browse(self.product_ids[0].id)
    #         asset.apartment_id = False
    #     # set new reference
    #     self.product_id.apartment_id = self


    # def write(self):
    #     if self.date_disponibility < (self.date_creation + relativedelta(months=3)):
    #         raise ValidationError( "La date de disponibilité doit être de minimum 3 mois après la création de l’appartement.'" )
    #     if self.expected_price <= 0:
    #         raise ValidationError('Entrez une valeur plus grande que 0 pour le prix attendu')
    #     if self.apartment_area <= 0:
    #         raise ValidationError('Entrez une valeur plus grande que 0 pour la surface de l\'appartement')
    #     if self.terrace_area <= 0:
    #         raise ValidationError('Entrez une valeur plus grande que 0 pour la surface de la terrasse')
    #     if self.apartment_area + self.terrace_area != self.total_area:
    #         raise ValidationError(
    #             'La surface totale de l\'appartement doit valloir la somme de la surface de la terrasse et de celle de l\'appartement')
    #     for record in self:
    #         record.total_area = record.terrace_area + record.apartment_area
    #     if self.best_offer_price < (self.expected_price * 0.9):
    #         raise ValidationError('L\'offre doit être de minimum 90% du prix attendu')
    #     if self.disponibility and self.date_disponibility < (self.date_creation + relativedelta(months=3)) :
    #         raise ValidationError( "La date de disponibilité doit être de minimum 3 mois après la création de l’appartement. L'appartement ne peut donc pas être disponible !")
    #     super().write()
