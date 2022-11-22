# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Fields
    use_contract = fields.Selection(
        string='Use Contract',
        related='company_id.use_contract',
        readonly=True,
    )
    contract_id = fields.Many2one(
        string='Contract',
        comodel_name='xf.partner.contract',
        ondelete='restrict',
        domain=[('state', '=', 'running')],
    )
    contract_no = fields.Char(string='Contract Number', related='contract_id.name')
    # incoterm_id =
    package_id = fields.Many2one('stock.quant.package', 'Packaging',)
    country_origin_id = fields.Many2one('res.country', string='Country of origin')


    # Compute and search fields, in the same order of fields declaration
    # Constraints and onchanges
    # Built-in methods overrides
    # Action methods

    @api.model
    def action_post(self):
        """supering invoice confirming function for amount/uom deduction from contract"""
        if self.invoice_line_ids and self.contract_id:
            contract = self.contract_id
            if contract.contract_amount_type == 'price':
                if contract.amount - self.amount_total < 0:
                    raise ValidationError(_('The bill amount is higher than contract amount'))
                contract.amount = contract.amount - self.amount_total
                if contract.amount == 0:
                    contract.state = 'expired'
            elif contract.contract_amount_type == 'unit':
                qty = self.invoice_line_ids.mapped('quantity')
                if contract.end_units - sum(qty) < 0:
                    raise ValidationError(_('The bill quantity is higher than contract quantity'))
                contract.end_units = contract.end_units - sum(qty)
                if contract.end_units == 0:
                    contract.state = 'expired'
        return super(AccountMove, self).action_post()

    def apply_contract(self):
        for move in self:
            if not move.contract_id:
                continue
            invoice_vals = move.contract_id._prepare_invoice(move.move_type)
            move.write(invoice_vals)
            move.apply_contract_lines()

    def apply_contract_lines(self):
        for move in self:
            if not move.contract_id:
                continue
            lines = self.env['account.move.line']
            for line in move.contract_id.line_ids:
                invoice_line_vals = line._prepare_invoice_line(move.id)
                invoice_line = lines.new(invoice_line_vals)
                invoice_line.account_id = invoice_line._get_computed_account()
                invoice_line._onchange_currency()
                invoice_line._onchange_price_subtotal()
                lines |= invoice_line
            move.with_context(check_move_validity=False).line_ids = lines
            move.with_context(check_move_validity=False)._onchange_invoice_line_ids()

    # Business methods

    def print_custom_invoice(self):
        product = []
        for line in self.invoice_line_ids:
            print('line.container_no', line.container_no)
            lines = {
                'product_id': line.product_id.name,
                'Container': line.container_no,
                'Quantity': line.quantity,
                'Price': line.price_unit,
                'Total': line.price_subtotal
            }
            product.append(lines)
        total = {
            'total_amount': self.amount_total_signed,
            'total_qty': sum(self.invoice_line_ids.mapped('quantity'))
        }
        rec = {
            'line': product,
            'total_amount': self.amount_total_signed,
            'total_qty': sum(self.invoice_line_ids.mapped('quantity')),
            'form': self.read()[0],
            'term': self.invoice_payment_term_id.name,
            'contract': self.contract_id.name,
            'incoterm': self.invoice_incoterm_id.name,
            'package':self.package_id.name,
            'country': self.country_origin_id.name

        }
        return self.env.ref('xf_partner_contract.print_custom_invoice').report_action(self, rec, total)


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    container_no = fields.Char(string='Container Number')
