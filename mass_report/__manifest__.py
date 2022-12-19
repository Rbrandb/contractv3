# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Mass Report',
    'version': '1.0',
    'summary': 'Mass Reports',
    'sequence': 10,
    'description': """""",
    'category': 'Accounting/Accounting',
    'website': '',
    'depends': ['account', 'account_reports', 'xf_partner_contract'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/mass_report_wizard.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'assets': {
    },
    'license': 'LGPL-3',
}
