# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    property_ids = fields.Many2many(
        string='Properties for smart report',
        comodel_name='product.product',
    )


    def action_view_property(self):
        return {
            'name': _('Properties'),
            'res_model': 'product.product',
            'type': 'ir.actions.act_window',
            # 'views': [(False, 'kanban')],
            'view_mode': 'tree',
        }

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'smart_report.property_ids', self.property_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        com_uom = with_user.get_param('smart_report.property_ids', default='')
        res.update(property_ids=[(6, 0, eval(com_uom))
                                     ] if com_uom else False, )
        return res
