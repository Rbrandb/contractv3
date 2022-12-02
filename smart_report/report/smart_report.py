# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import api, models,fields , _


class SmartReport(models.AbstractModel):
    _name = 'report.smart_report.smart_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('ffffffffffffffffff')
        if self.env.context.get('smart_report'):
            print('kkkkkkkkkkkkkkkkkkkkkkgggggggggggg')

            if data.get('report_data'):
                print('data', data.get('report_data')['company'])
                data.update({'report_main_line_data': data.get('report_data')['report_lines'],
                             'Filters': data.get('report_data')['filters'],
                             'company_name': data.get('report_data')['company'],
                             'crnt_turnover': data.get('report_data')['report_vals'][1],
                             'last_turnover': data.get('report_data')['report_vals'][2],
                             'open_invoice': data.get('report_data')['report_vals'][3],
                             'open_bills': data.get('report_data')['report_vals'][4],
                             'current_cost': data.get('report_data')['report_vals'][5],
                             'last_cost': data.get('report_data')['report_vals'][6],
                             'current_margin': data.get('report_data')['report_vals'][7],
                             'last_margin': data.get('report_data')['report_vals'][8],
                             'total': data.get('report_data')['report_vals'][9],
                            'date': fields.Datetime.now()
                             })
            return data
