# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    specification = fields.Boolean(default=False)
    specification_id = fields.Many2one('contract.specification', string='Specification', readonly=True)
