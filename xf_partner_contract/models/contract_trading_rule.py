# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ContractTradingRule(models.Model):
    _name = "contract.trading.rule"
    _description = "Contract Trading Rules"

    name = fields.Char(
        string='Name',
        required=True,
    )

    def unlink(self):
        for recd in self:
            if self.env['xf.partner.contract.line'].search([('delivery_term_id', '=', recd.id)]):
                raise UserError(_('You cannot delete a Delivery Term that is already used for a contract'))
        return super(ContractTradingRule, self).unlink()
