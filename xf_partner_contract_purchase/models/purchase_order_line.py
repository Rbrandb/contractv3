# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    specification = fields.Boolean(default=False)
    specification_id = fields.Many2one('contract.specification', string='Specification', readonly=True)