# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class DocumentsDocument(models.Model):
    _inherit = "documents.document"

    contract_id = fields.Many2one('xf.partner.contract',
        string='Contract',
    )


