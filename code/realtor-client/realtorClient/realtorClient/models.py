from djangodoo.models import OdooModel

class Partner(OdooModel):
    _odoo_model = "res.partner"
    # _odoo_fields = ['name']  # optional; if omitted, all fields are copied
    # _odoo_ignore_fields = None  # optional; fields in this list are not copied