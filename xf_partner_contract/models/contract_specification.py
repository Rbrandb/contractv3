# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ContractSpecification(models.Model):
    _name = "contract.specification"
    _description = "Contract Specification"

    name = fields.Char(
        string='Name',
        required=True,
    )

    def unlink(self):
        for recd in self:
            if self.env['xf.partner.contract.line'].search([('specification_id', '=', recd.id)]):
                raise UserError(_('You cannot delete a specification that is already used for a contract'))
        return super(ContractSpecification, self).unlink()
