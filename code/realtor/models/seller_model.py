from odoo import api, fields, models


class Seller(models.Model):
    _inherit = 'res.users'

    # _name = 'realtor.seller'
    _description = 'Vendeur d\'un appartement'
    # name = fields.Char('Vendeur de l\'appartement', required=True, unique=True)
    offer = fields.Many2one('realtor.offer', string='Meilleur acheteur')