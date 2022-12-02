odoo.define("smart_report.smart_dynamic_report", function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var ajax = require('web.ajax');
    var web_client = require('web.web_client');
    var _t = core._t;
    var framework = require('web.framework');
    var session = require('web.session');
    var operation_types;
    var current_company;
    var result_3;
    var SmartDynamic = AbstractAction.extend({
        contentTemplate: 'smart_dynamic',
        events: {
            'change #company_selection': 'onclick_company_selection',
            'click #pdf': 'print_pdf',
        },

        init: function(parent, action) {
			this._super(parent, action);
			this.report_lines = action.report_lines;
			this.wizard_id = action.context.wizard | null;

		},

        willStart: function(){
        var self = this;
//        this.login_employee = {};
        return this._super()
        .then(function() {
            var def0 =  self._rpc({
                    model: 'accounting.smart.report',
                    method: 'get_properties'
            }).then(function(result) {
                self.properties =  result[0];
                self.curr_turn_over = result[1];
                self.last_yr_turnover = result[2];
                self.open_invoice = result[3];
                self.open_bills = result[4];
                self.cost_current_yr = result[5];
                self.cost_last_yr = result[6];
                self.current_yr_margin = result[7];
                self.last_yr_margin = result[8];
                self.total_amount = result[9];
            });
        return $.when(def0);
        });
    },

        start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                self.render_company_options();
                self.$el.parent().addClass('oe_background_grey');
            });
        },

        print_pdf: function(e) {
            e.preventDefault();
			var self = this;
			var action_title = self._title;
			console.log('self.wizard_id', self.wizard_id)
			self._rpc({
				model: 'accounting.smart.report',
				method: 'smart_pdf_report',
				args: [
					[this.wizard_id], current_company
				],
			}).then(function(data) {
				var action = {
					'type': 'ir.actions.report',
					'report_type': 'qweb-pdf',
					'report_name': 'smart_report.smart_report',
					'report_file': 'smart_report.smart_report',
					'data': {
						'report_data': data
					},
					'context': {
						'active_model': 'accounting.smart.report',
						'landscape': 1,
						'smart_report': true

					},
					'display_name': 'Smart Report',
				};
				return self.do_action(action);
			});

		},

		onclick_company_selection: async function(e) {
			e.preventDefault();
			var option = $(e.target).val();
			console.log('kkkkkkkk', option)
			var self = this;
			current_company = option
			await self._rpc({
				model: 'accounting.smart.report',
				method: 'get_properties',
				args: [
					option
				],
			}).then(function(result) {
			    self.properties =  result[0];
                self.curr_turn_over = result[1];
                self.last_yr_turnover = result[2];
                self.open_invoice = result[3];
                self.open_bills = result[4];
                self.cost_current_yr = result[5];
                self.cost_last_yr = result[6];
                self.current_yr_margin = result[7];
                self.last_yr_margin = result[8];
                self.total_amount = result[9];
			    $('.smart-table').remove();
			    console.log('result', result)
                for (var c in self.properties) {
                console.log('ccccccccccccccc', c)
                $('.table_smart').append('<table class="smart-table" style="margin-top:50px; width:100%; margin-left:20px;">
                    <thead style="display: table-row-group; background-color:#8DB2D7; border: 0.3rem solid #8DB2D7;
                        border-bottom: none;">
                        <tr>
                            <th class="" style="width: 30%; color: white;" scope="col">
                                '+self.properties[c]+'
                            </th>
                            <th class="" style="width: 20%; color: white;" scope="col">
                                Amount
                            </th>
                            <th class="" style="width: 30%; color: white;" scope="col">
                            </th>
                            <th class="" style="width: 20%; color: white;" scope="col">
                                Amount
                            </th>
                        </tr>
                    </thead>
                    <body>
                         <tr>
                             <td style="border: 0.3rem solid black; border-right: none; border-top: none;">
                                 Open invoices
                             </td>
                             <td style="border: 0.3rem solid black; border-left: none; border-top: none;">
                                 '+self.open_invoice[c]+'
                             </td>
                             <td style="border: 0.3rem solid black; border-right: none; border-top: none;">
                                 Costs current year

                             </td>
                             <td style="border: 0.3rem solid black; border-left: none; border-top: none;">
                                 '+self.cost_current_yr[c]+'
                             </td>
                         </tr>
                         <tr>
                             <td style="border: 0.3rem solid black; border-right: none; border-top: none;">
                                 Turnover current year
                             </td>
                             <td style="border: 0.3rem solid black; border-left: none; border-top: none;">
                                 '+self.curr_turn_over[c]+'
                             </td>
                             <td style="border: 0.3rem solid black; border-right: none; border-top: none;">
                                 Costs last year
                             </td>
                             <td style="border: 0.3rem solid black; border-left: none; border-top: none;">
                                 '+self.cost_last_yr[c]+'
                             </td>
                         </tr>
                         <tr>
                             <td style="border: 0.3rem solid black; border-right: none; border-top: none;">
                                 Turnover last year
                             </td>
                             <td style="border: 0.3rem solid black; border-left: none; border-top: none;">
                                 '+self.last_yr_turnover[c]+'
                             </td>
                             <td style="border: 0.3rem solid black; border-right: none; border-top: none;">
                                 Margin current year

                             </td>
                             <td style="border: 0.3rem solid black; border-left: none; border-top: none;">
                                 '+self.current_yr_margin[c]+'
                             </td>
                         </tr>
                         <tr>
                             <td style="border: 0.3rem solid black; border-right: none; border-top: none;">
                                 Costs invoices open
                             </td>
                             <td style="border: 0.3rem solid black; border-left: none; border-top: none;">
                                 '+self.open_bills[c]+'
                             </td>
                             <td style="border: 0.3rem solid black; border-right: none; border-top: none;">
                                 Margin last year

                             </td>
                             <td style="border: 0.3rem solid black; border-left: none; border-top: none;">
                                 '+self.last_yr_margin[c]+'
                             </td>
                         </tr>
                          <tr>
                             <td>
                             </td>
                              <td>
                              </td>
                              <td>
                              </td>
                              <td>
                                Total :
                                  '+self.total_amount[c]+'
                                <hr style="border-top: 2px solid #00000024; margin-top: .2rem; margin-bottom: 0rem;"/>
                             </td>
                          </tr>
                    </body>
              </table>
                ')
                }
			});
		},

         render_company_options:  function() {
            var self = this;

            var def1 =  this._rpc({
                model: 'accounting.smart.report',
                method: 'get_company'
            }).then(function(result) {
                console.log('result', result)
                var com = result[0]
                for (var c in result[0]) {
                    if (com[c].id === result[1]){
                    console.log('good');
                    current_company = com[c].id
                    $('#company_selection').append('<option id="'+com[c].id+'" value="'+com[c].id+'" selected="">'+String(com[c].name)+'</option>')
                    }
                    else{
                        $('#company_selection').append('<option id="'+com[c].id+'" value="'+com[c].id+'">'+String(com[c].name)+'</option>')
                    };
                    };
                });
        },
    });
    core.action_registry.add('smart_report_tag', SmartDynamic);
    return;
});
