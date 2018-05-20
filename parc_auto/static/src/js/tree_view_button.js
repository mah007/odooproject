odoo.define('tree_menu.tree_view_button', function (require){
"use strict";


var core = require('web.core');
var ListView = require('web.ListView');
var QWeb = core.qweb;


ListView.include({

        render_buttons: function($node) {
                var self = this;
                this._super($node);
                    this.$buttons.find('#cvrp').click(this.proxy('main'));
        },

        main: function () {


            this.do_action({
                    type: "ir.actions.act_window",
                    name: "ordremission",
                    res_model: "parcauto.ordremission",
                    views: [[false,'form']],
                    target: 'current',
                    view_type : 'form',
                    view_mode : 'form',
                    flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
            });
        }

});

});