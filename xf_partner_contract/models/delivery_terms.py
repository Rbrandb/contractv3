# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class DeliveryTerms(models.Model):
    _name = "delivery.terms"
    _description = "Contract Delivery Terms"

    name = fields.Char(
        string='Name',
        required=True,
    )

    def unlink(self):
        for recd in self:
            if self.env['xf.partner.contract.line'].search([('delivery_term_id', '=', recd.id)]):
                raise UserError(_('You cannot delete a Delivery Term that is already used for a contract'))
        return super(DeliveryTerms, self).unlink()
