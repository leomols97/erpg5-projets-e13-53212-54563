from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError
from datetime import datetime


class Apartment(models.Model):
    _name = 'realtor.apartment'
    _description = 'Modèle d\'un appartement'
    name = fields.Char('Nom de l\'appartement', required=True, unique=True)
    description = fields.Char('Description de l\'apartment', required=True)
    image = fields.Binary("Image") #, required=True)
    expected_price = fields.Integer('Prix attendu', required=True, min=1)
    apartment_area = fields.Integer('Surface de l\'appartement', required=True, min=1)
    terrace_area = fields.Integer('Surface de la terrasse', required=True, min=1)
    total_area = fields.Integer('Surface totale', min=2)
    best_buyer = fields.Many2many('res.partner', string='Meilleur acheteur')
    best_offer = fields.Integer('Meilleure offre')
    disponible = fields.Boolean('Disponible?', default=False)
    date_creation = fields.Date(string='Date de création de l\'appartement', default=datetime.today())
    date_disponibility = fields.Date(string='Date de création de l\'appartement', default=datetime.today())

    # @api.constrains('end_date', 'date_disponibility')
    # def date_constrains(self):
    #     for rec in self:
    #         if rec.end_date < rec.date_creation:
    #             raise ValidationError('Sorry, End Date Must be greater Than Disponibility Date...')

    @api.constrains('expected_price')
    def _check_expected_price(self):
        if self.expected_price <= 0:
            raise ValidationError('Entrez une valeur plus grande que 0 pour le prix attendu')

    @api.constrains('apartment_area')
    def _check_apartment_area(self):
        if self.apartment_area <= 0:
            raise ValidationError('Entrez une valeur plus grande que 0 pour la surface de l\'appartement')

    @api.constrains('terrace_area')
    def _check_terrace_area(self):
        if self.terrace_area <= 0:
            raise ValidationError('Entrez une valeur plus grande que 0 pour la surface de la terrasse')

    @api.constrains('total_area')
    @api.depends('apartment_area', 'terrace_area')
    def _compute_total_area(self):
        if self.apartment_area + self.terrace_area != self.total_area:
            raise ValidationError('La surface totale de l\'appartement doit valloir la somme de la surface de la terrasse et de celle de l\'appartement')

    @api.depends('expected_price', 'best_offer')
    def _compute_min_price(self):
        if self.best_offer < (self.expected_price * 0.9):
            raise ValidationError('L\'offre doit être de minimum 90% du prix attendu')