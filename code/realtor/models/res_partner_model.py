from odoo import fields, models

class ResPartner (models.Model):
    _inherit = 'res.partner'

    apartment_ids = fields.Many2many('apartment', string='Appartements associés à l\'acheteur')
    # offer_id = fields.Many2one('offer', string='Offres de l\'acheteur')