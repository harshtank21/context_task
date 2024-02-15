from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "purchase.order"
    _description = "task"

    unique = fields.Char('unique')
