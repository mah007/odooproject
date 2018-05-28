odoo.define('tree_menu.tree_view_button', function (require){
"use strict";


var core = require('web.core');
var ListView = require('web.ListView');
var QWeb = core.qweb;
var Model = require('web.Model');


ListView.include({

        render_buttons: function($node) {
                var self = this;
                this._super($node);
                    this.$buttons.find('#cvrp').click(this.proxy('callmain'));
        },

        callmain: function () {
            new Model('parcauto.demande').call('main',[[]]).then(function(result)
              {
                console.log("hello world, I am working");
              }
            );
        }

});

});