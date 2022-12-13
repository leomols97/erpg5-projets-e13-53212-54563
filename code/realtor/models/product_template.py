from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Apartment product template'

    apartment_id = fields.Many2one('realtor.apartment', string='Appartement associé à un produit')