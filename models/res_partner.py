from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    untrustworthy = fields.Boolean("Untrustworthy")
