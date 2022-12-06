/** @odoo-module **/

    import ActionMenus from "web.ActionMenus";
    import { patch } from 'web.utils';
    patch(ActionMenus.prototype, 'xf_partner_contract/static/src/js/side_bar.js', {
        async _setPrintItems(props) {
            if (this.env.view.base_model === "account.move" || 'xf.partner.contract') {
                props.items.print = [];
            }
            return this._super(...arguments)
        }
    })
