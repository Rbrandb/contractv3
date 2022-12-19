# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import csv
import io
from datetime import datetime
from odoo import api, models, fields


class MassReportWizard(models.TransientModel):
    _name = "mass_report.wizard"
    _description = "Exports Mass Report data to a CSV file."

    type = fields.Selection([
        ('certified', 'Certified'),
        ('non_certified', 'Non Certified')
    ], string='Type', required=True, default='certified')

    generated_csv_file = fields.Binary(
        "Generated file",
        help="Technical field used to temporarily hold the generated CSV file before it's downloaded."
    )

    def _generate_row(self, line):
        """ Generates a single row in the output CSV. Will attribute the total to the box specified on the partner. """
        contract_id = line.contract_id
        invoice_ids = contract_id.invoice_ids

        container_name = ''
        container_name_list = []
        bill = ''
        bill_list = []
        co = ''
        co_list = []
        transaction_date = ''
        transaction_date_list = []
        for invoice in invoice_ids:
            if invoice.name:
                bill_list.append(invoice.name)
            if invoice.country_origin_id:
                co_list.append(invoice.country_origin_id.name)
            if invoice.invoice_date:
                us_format = "%m-%d-%Y"
                transaction_date_list.append(invoice.invoice_date.strftime(us_format))
            for inv_line in invoice.invoice_line_ids:
                if inv_line.container_no:
                    container_name_list.append(inv_line.container_no)

        if bill_list:
            bill = ','.join(bill_list)
        if transaction_date_list:
            transaction_date = ','.join(transaction_date_list)
        if container_name_list:
            container_name = ','.join(container_name_list)
        if co_list:
            co = ','.join(co_list)

        purchase_contract = ''
        company = ''
        product = line.product_id.display_name
        if contract_id.type == 'purchase':
            purchase_contract = contract_id.purchase_order_ids.mapped('name')
            company = contract_id.partner_id and line.contract_id.partner_id.display_name or ''


        row = [
            line.contract_id.ref,
            line.contract_id.ref,
            line.contract_id.name,
            line.contract_id.partner_id and line.contract_id.partner_id.display_name or '',
            container_name,
            '',                 # Weight DN-Out
            purchase_contract,  # Purchase contract
            company,            # company
            product,            # product
            co,                # coo
            '',                 # dn in
            '',                 # Weight DN-In
            transaction_date,
            bill, #bill
        ]
        return row

    def action_generate(self):
        """ Called from UI. Generates the CSV file in memory and writes it to the generated_csv_file
        field. Then returns an action for the client to download it. """
        self.ensure_one()
        header = [
            "Name",
            "Invoice",
            "Sales Contract",
            "Company",
            "Containers",
            "Weight DN-Out",
            "Purchase contract",
            "Company",
            "Product",
            "C.O.O.",
            "DN IN",
            "Weight DN-In",
            "Transaction date",
            "Bill",
        ]
        xf_contract_ids = self.env["xf.partner.contract"].search([])

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(header)

        if self.type == 'certified':
            line_ids = xf_contract_ids.line_ids.filtered(lambda line:line.specification_id and line.specification_id.name.lower() == 'certified')
        else:
            line_ids = xf_contract_ids.line_ids.filtered(lambda line:line.specification_id and line.specification_id.name.lower() != 'certified')

        for line in line_ids:
            new_row = self._generate_row(line,)
            writer.writerow(new_row)

        self.generated_csv_file = base64.b64encode(output.getvalue().encode())

        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": "/web/content?model=mass_report.wizard&download=true&field=generated_csv_file&filename=Mass Report {}.csv&id={}".format(
                datetime.now(), self.id
            ),
        }
