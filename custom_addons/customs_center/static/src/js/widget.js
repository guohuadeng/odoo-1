odoo.define('customs_center', function (require) {
    var core = require('web.core');
    var FormWidget = require('web.form_widgets');
    var QWeb = core.qweb;

    QWeb.add_template('/customs_center/static/src/xml/declare_element_modal.xml');

    var FieldDeclareElement = FormWidget.FieldChar.extend({
        events: {
            'focus': 'show_ele_modal'
        },

        renderElement: function () {
          this._super();
          this.modal_id = _.uniqueId("dec-ele-");
          var temp = $(QWeb.render("declare_element_modal"));
          temp.prop('id', this.modal_id);
          setTimeout(function () {
              $('body').delay(1000).append(temp);
          });

        },

        show_ele_modal: function () {
            $('#' + this.modal_id).modal();
        }
    });

    core.form_widget_registry.add('declare_element', FieldDeclareElement)
});