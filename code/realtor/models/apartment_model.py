from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Apartment(models.Model):
    _name = 'realtor.apartment'
    _description = 'Modèle d\'un appartement'
    name = fields.Char(string='Nom de l\'appartement', required=True, unique=True)
    description = fields.Char(string='Description de l\'apartment', required=True)
    image = fields.Binary(string='Image', required=True)
    expected_price = fields.Integer(string='Prix attendu', required=True, min=1)
    apartment_area = fields.Integer(string='Surface de l\'appartement', required=True, min=1)
    terrace_area = fields.Integer(string='Surface de la terrasse', required=True, min=1)
    total_area = fields.Integer(string='Surface totale', compute='_compute_total_area')
    offers = fields.Many2many('realtor.offer', string='Offres')
    best_buyer = fields.Many2many('res.partner', string='Acheteurs potentiels')
    best_offer = fields.Integer(string='Meilleure offre')
    # seller = fields.Many2one('realtor.seller', string='Vendeur')
    disponible = fields.Boolean(string='Disponible?', default=False)
    date_creation = fields.Date(string='Date de création de l\'appartement', default=datetime.today(), readonly=True)
    date_disponibility = fields.Date(string='Date de création de l\'appartement', default=datetime.today() + relativedelta(months=3))

    @api.constrains('date_creation', 'date_disponibility')
    def _check_dates( self ):
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
                'La surface totale de l\'appartement doit valloir la somme de la surface de la terrasse et de celle de l\'appartement')

    @api.depends('apartment_area', 'terrace_area')
    def _compute_total_area(self):
        """ Computes the total surface of an apartment """
        for record in self:
            record.total_area = record.terrace_area + record.apartment_area

    @api.depends('expected_price', 'best_offer')
    def _compute_min_price(self):
        """ Checks if the best offer is not lower than 90% of the expected price """
        if self.best_offer < (self.expected_price * 0.9):
            raise ValidationError('L\'offre doit être de minimum 90% du prix attendu')


    # @api.depends('offers')
    # def _compute_best_offer(self):
    #     """ Looks for the best offer for an apartment """
    #     for record in self:
    #         for offer in record:
    #             if record.price < offer.price:
    #                 record.best_buyer = offer.buyer
    #                 record.best_offer = offer.price

    @api.constrains('date_creation', 'date_disponibility', 'disponible')
    def _check_disponibility(self):
            """ Checks if the date of disponibility of the apartment is not lower than 3 months after the date of creation of the offer """
            if self.disponible & self.date_disponibility < (self.date_creation + relativedelta(months=3)) :
                raise ValidationError( "La date de disponibilité doit être de minimum 3 mois après la création de l’appartement. L'appartement ne peut donc pas être disponible !")