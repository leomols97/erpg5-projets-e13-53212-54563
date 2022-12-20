from odoo import api, fields, models


class Offer(models.Model):
    _name = 'realtor.offer'
    _description = 'Offre pour un appartement'
    name = fields.Char('Offre de l\'appartement', required=True, unique=True)
    description = fields.Char('Description de l\'offre', required=True)
    price = fields.Integer('Montant de l\'offre', required=True, min=1)
    apartment = fields.Many2one('realtor.apartment', string='Appartement')
    # seller = fields.Many2one('res.users', string='Vendeur')
    # buyer = fields.Many2one('res.partner', string='Acheteurs potentiels')