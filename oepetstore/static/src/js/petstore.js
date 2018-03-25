odoo.oepetstore = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;


   local.ColorInputWidget = instance.Widget.extend({
         template: "ColorInputWidget",
         events: {
             'change input': 'input_changed',
         },
         init: function(parent){
             this._super(parent);
         },
         start: function() {
             this.input_changed();
             return this._super();
         },
         input_changed: function(){
             var color = [
                 "#",
                 this.$(".oe_color_red").val(),
                 this.$(".oe_color_green").val(),
                 this.$(".oe_color_blue").val()
             ].join('');
             this.set("color", color);
             this.$(".oe_color_div").css("background-color", this.get("color"));
//             this.$el.append("<font color="+this.get("color")+">Enfin :</font>");
         },
    });


//    HomePage first adds its own content to its DOM root
//    HomePage then instantiates GreetingsWidget
//    Finally it tells GreetingsWidget where to insert itself, delegating part of its $el to the GreetingsWidget.

    local.HomePage = instance.Widget.extend({
         template: "HomePage",
         start: function() {
             this.colorInput = new local.ColorInputWidget(this);
//             this.$el.append("<div>apres l instanciation de color input</div>");
//             this.$el.append(this.get("color"));
////             this.$el.append(colorInput.get("color"));
//             this.$el.append("<div>apres l instanciation de color input</div>");
             this.colorInput.on("change: color", this, this.color_changed);
             return this.colorInput.appendTo(this.$el);
//             this.$el.append("<div>this is start function in HomePage</div>");
         },
         color_changed: function() {
             this.$(".oe_color_div").css("background-color", this.colorInput.get("color"));
//             this.$el.append("<div>Hello Nassima this is color_changed function</div>");
         },
//         template: "HomePageTemplate",
//         className: 'oe_petstore_homepage',
//         init: function(parent){
//             this._super(parent);
//             this.name = "Mordecai";
//         },

//         start: function() {
//             var products = new local.ProductsWidget(
//                 this, ["cpu", "mouse", "keyboard", "graphic card", "screen"], "#00FF00");
//             products.appendTo(this.$el);
//
//////             this.$el.append(QWeb.render("HomePageTemplate", {name: "Nassima"}));
////             console.log("pet store home page loaded");
////             this.$el.append("<div>Hello Nassima</div>")
//////           this est une instance du widget HomePage, pour dire au nouveau widget
//////           quel est son parent
////             var greeting = new local.GreentingsWidget(this);
////             return greeting.appendTo(this.$el);
//         },
    });



//    local.ProductsWidget = instance.Widget.extend({
//          template: "ProductsWidget",
//          init: function(parent, products, color){
//              this._super(parent);
//              this.products = products;
//              this.color = color;
//          },
//    });


    instance.web.client_actions.add('petstore.homepage', 'instance.oepetstore.HomePage');


}
