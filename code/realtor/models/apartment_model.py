from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError
from datetime import date


class Apartment(models.Model):
    _name = 'realtor.apartment'
    _description = 'Modèle d\'un appartement'
    name = fields.Char('Nom de l\'appartement', required=True, unique=True)
    description = fields.Char('Description de l\'apartment', required=True)
    # image = fields.Binary("Image", help='Select image here', required=True)
    date_disponibility = fields.Date.today()
    expected_price = fields.Integer('Prix attendu', required=True, min=1)
    apartment_area = fields.Integer('Surface de l\'appartement', required=True, min=1)
    terrace_area = fields.Integer('Surface de la terrasse', required=True, min=1)
    total_area = fields.Integer('Surface totale', min=2)
    best_buyer = fields.Many2many('res.partner')
    best_offer = fields.Integer('Meilleure offre')
    disponible = fields.Boolean('Disponible?', default=True)

    # @api.constrains('end_date', 'date_disponibility')
    # def date_constrains(self):
    #     for rec in self:
    #         if rec.end_date < rec.date_disponibility:
    #             raise ValidationError('Sorry, End Date Must be greater Than Disponibility Date...')
    #
    # @api.constrains('expected_price')
    # def _check_expected_price(self):
    #     if self.expected_price <= 0:
    #         raise ValidationError('Enter Value For Expected Price Greater Than 0')
    #
    # @api.constrains('apartment_area')
    # def _check_apartment_area(self):
    #     if self.apartment_area <= 0:
    #         raise ValidationError('Enter Value For Area Of The Apartment Greater Than 0')
    #
    # @api.constrains('terrace_area')
    # def _check_terrace_area(self):
    #     if self.terrace_area <= 0:
    #         raise ValidationError('Enter Value For Area Of The Terrace Greater Than 0')
    #
    # @api.depends('apartment_area', 'terrace_area')
    # def _compute_total_area(self):
    #     for record in self:
    #         record.sum = record.apartment_area + record.terrace_area
    #
    # @api.depends('expected_price', 'best_offer')
    # def _compute_min_price(self):
    #     if self.best_offer < (self.expected_price * 0.9):
    #         raise ValidationError('L\'offre doit être de minimum 90% du prix attendu')