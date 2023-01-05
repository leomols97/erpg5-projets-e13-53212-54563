from odoo import fields, models

class Buyer (models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    apartment = fields.Many2one('realtor.apartment', string="Offres de l'acheteur")
    offer_price= fields.Integer("Prix de l'offre", default=0)