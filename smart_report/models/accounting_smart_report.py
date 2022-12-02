# -*- coding: utf-8 -*-
from odoo.http import request

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountingSmartReport(models.Model):
    _name = 'accounting.smart.report'

    @api.model
    def get_company(self):
        company = self.env['res.company'].search(
            [])
        default_company = self.env.company
        comp = []
        for rec in company:
            comp.append(
                {'name': rec.name,
                 'id': rec.id
                 }
            )
        return comp, default_company.id

    @api.model
    def get_properties(self, options=None):
        if options:
            default_company = int(options)
        else:
            default_company = self.env.company.id
        current_yr = fields.datetime.now().year
        values = self.env['ir.config_parameter'].sudo().get_param('smart_report.property_ids')
        if not values:
            raise ValidationError(_('Please add your properties in settings'))
        product = self.env['product.product'].search([
            ('id', 'in', eval(values))
        ])
        accnt_move_line = self.env['account.move.line'].search([('company_id', '=', default_company)])
        invoice = accnt_move_line.filtered(lambda x: x.move_id.move_type == 'out_invoice')
        bills = accnt_move_line.filtered(lambda x: x.move_id.move_type == 'in_invoice')
        comp = []
        current_year_turnover = []
        last_year_turnover = []
        open_invoice_list = []
        open_bill_list = []
        cost_current_yr_list = []
        cost_last_yr_list = []
        current_yr_margin = []
        last_yr_margin = []
        total = []
        for pro in product:
            comp.append(
                pro.name
            )

            order_current_yr = invoice.filtered(lambda l: l.product_id == pro and l.create_date.year == current_yr)
            current_year_turnover_amount = sum(order_current_yr.mapped('price_subtotal'))
            if current_year_turnover_amount:
                current_year_turnover.append(current_year_turnover_amount)
            else:
                current_year_turnover.append(0)
            orders_last_yr = invoice.filtered(lambda l: l.product_id == pro and l.create_date.year == current_yr - 1)
            turn_over_last_yr_amt = sum(orders_last_yr.mapped('price_subtotal'))
            if turn_over_last_yr_amt:
                last_year_turnover.append(turn_over_last_yr_amt)
            else:
                last_year_turnover.append(0)
            open_invoice = invoice.filtered(lambda l: l.product_id == pro)
            open_invoice_amount = sum(open_invoice.mapped('price_subtotal'))
            if open_invoice_amount:
                open_invoice_list.append(open_invoice_amount)
            else:
                open_invoice_list.append(0)
            open_bills = bills.filtered(lambda l: l.product_id == pro)
            open_bill_amount = sum(open_bills.mapped('price_subtotal'))
            if open_bill_amount:
                open_bill_list.append(open_bill_amount)
            else:
                open_bill_list.append(0)
            cost_current_yr = bills.filtered(lambda l: l.product_id == pro and l.create_date.year == current_yr)
            current_yr_cost = sum(cost_current_yr.mapped('price_subtotal'))
            if current_yr_cost:
                cost_current_yr_list.append(current_yr_cost)
            else:
                cost_current_yr_list.append(0)
            cost_last_yr = bills.filtered(lambda l: l.product_id == pro and l.create_date.year == current_yr - 1)
            last_yr_cost = sum(cost_last_yr.mapped('price_subtotal'))
            if last_yr_cost:
                cost_last_yr_list.append(last_yr_cost)
            else:
                cost_last_yr_list.append(0)
            margin_current_yr = sum(order_current_yr.mapped('price_subtotal')) - sum(cost_current_yr.mapped('price_subtotal'))
            if margin_current_yr:
                current_yr_margin.append(margin_current_yr)
            else:
                current_yr_margin.append(0)
            margin_last_yr = sum(orders_last_yr.mapped('price_subtotal')) - sum(cost_last_yr.mapped('price_subtotal'))
            if margin_last_yr:
                last_yr_margin.append(margin_last_yr)
            else:
                last_yr_margin.append(0)
            total.append(
                current_year_turnover_amount + turn_over_last_yr_amt + open_invoice_amount + open_bill_amount +
                current_yr_cost + last_yr_cost + margin_current_yr + margin_last_yr
            )
            if total == []:
                total.append(0)
        return comp, current_year_turnover, last_year_turnover, open_invoice_list, open_bill_list, cost_current_yr_list, cost_last_yr_list, current_yr_margin, last_yr_margin, total

    @api.model
    def smart_pdf_report(self, option, current):
        report_values = self.env['accounting.smart.report'].search([('id', '=', option[0])])
        data = {
            # 'report_type': report_values.report_type,
            'model': self,
        }

        current_yr = fields.datetime.now().year
        values = self.env['ir.config_parameter'].sudo().get_param('smart_report.property_ids')
        product = self.env['product.product'].search([
            ('id', 'in', eval(values))
        ])
        comp = []
        for pro in product:
            comp.append(
                pro.name
            )
        filters = comp
        report = []
        lines = []
        main_line = []
        report_vals = self.get_properties(int(current))
        company = self.env['res.company'].search([(
            'id', '=', int(current)
        )])
        print('company', company)
        return {
            'name': "Smart Report",
            'type': 'ir.actions.client',
            'tag': 'smart_report_tag',
            'orders': data,
            'filters': filters,
            'report_lines': lines,
            'report_main_line': main_line,
            'report_vals': report_vals,
            'company': company.name
        }
