# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from .selection import UseContract


class Company(models.Model):
    _inherit = 'res.company'

    contract_approval = fields.Selection(
        string='Use Contract Approval Workflow',
        selection=UseContract.list,
        default=UseContract.default,
    )
    use_contract = fields.Selection(
        string='Use Contract for Invoices',
        selection=UseContract.list,
        default=UseContract.default,
    )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    contract_approval = fields.Selection(
        string='Use Contract Approval Workflow',
        related='company_id.contract_approval',
        readonly=False,
    )
    use_contract = fields.Selection(
        string='Use Contract for Invoices',
        related='company_id.use_contract',
        readonly=False,
    )
    use_contract_amount_type = fields.Selection([
        ('no', 'No'),
        ('optional', 'Optional'),
        ('require', 'Required'),
    ], string='Use Contract amount type', config_parameter='xf_partner_contract.use_contract_amount_type', default='no'
    )
    contract_currency_ids = fields.Many2many(
        string='Currencies for contracts',
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id,
    )

    contract_uom_ids = fields.Many2many(
        string='Uom for contracts',
        comodel_name='uom.uom',
    )


    def action_view_currency(self):
        return {
            'name': _('Currencies'),
            'res_model': 'res.currency',
            'type': 'ir.actions.act_window',
            # 'views': [(False, 'kanban')],
            'view_mode': 'tree',
        }

    def action_view_uom(self):
        return {
            'name': _('Units of Measures'),
            'res_model': 'uom.uom',
            'type': 'ir.actions.act_window',
            # 'views': [(False, 'kanban')],
            'view_mode': 'tree',
        }

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'xf_partner_contract.contract_currency_ids', self.contract_currency_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param(
            'xf_partner_contract.contract_uom_ids', self.contract_uom_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        com_currency = with_user.get_param('xf_partner_contract.contract_currency_ids', default='')
        com_uom = with_user.get_param('xf_partner_contract.contract_uom_ids', default='')
        res.update(contract_currency_ids=[(6, 0, eval(com_currency))
                                     ] if com_currency else False, )
        res.update(contract_uom_ids=[(6, 0, eval(com_uom))
                                     ] if com_uom else False, )
        return res
