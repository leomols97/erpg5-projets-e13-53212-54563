from odoo import fields, models

class Buyer (models.Model):
    _inherit = 'res.partner'

    # _name = 'realtor.buyers'
    # apartment_ids = fields.Many2many('apartment', string='Appartements associés à l\'acheteur')
    # potential_buyers = fields.Many2many('realtor.offer', string='Offre liée à l\'acheteur')
    offer = fields.Many2one('realtor.offer', string='Offres de l\'acheteur')