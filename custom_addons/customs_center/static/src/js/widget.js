odoo.define('customs_center', function (require) {
    var core = require('web.core');
    var FormWidget = require('web.form_widgets');
    var QWeb = core.qweb;
    var Model = require('web.Model');

    QWeb.add_template('/customs_center/static/src/xml/declare_element_modal.xml');

    var FieldDeclareElement = FormWidget.FieldChar.extend({

        init: function () {
            this._super.apply(this, arguments);
            this.set({'tariff': false});
            var tariff_field = this.options && this.options.tariff;
            if (tariff_field) {
                this.field_manager.on("field_changed:"+tariff_field, this, function () {
                    this.set({'tariff': this.field_manager.get_field_value(''+tariff_field)})
                })
            }
            this.on('change:tariff', this, this.get_element_name);
            this.element_names = [];
            this.input_temp = '<div class="row" style="padding-bottom: 20px">' +
                '<div class="col-md-4"><label for="<%= field_id %>"><%= name %></label></div>' +
                '<div class="col-md-6"><input class="o_form_label" id="<%= field_id %>"/></div>' +
                '</div>'
        },

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
            var self = this;
            var display_board = $('#declare-element-names');
            display_board.empty();
            _.each(self.element_names, function (element_name) {
                var ele_name = element_name[1];
                var sequence = element_name[0];
                var temp = _.template(self.input_temp);
                console.log(temp);
                var field = temp({field_id: 'dec-ele-'+sequence, name: ele_name});
                display_board.append($(field))
            })
        },

        remove_field: function () {
            var display_board = $('#declare-element-names');
            display_board.empty()
        },

        get_element_name: function () {
            if (this.get('tariff')){
                var DeclareElement = new Model('declare_element');
                var self = this;
                DeclareElement.query(['name', 'sequence']).filter([['cus_goods_tariff_id', '=', self.get('tariff')]])
                    .order_by('sequence')
                    .all()
                    .then(function (elements) {
                        _.each(elements, function (element) {
                            self.element_names.push([element.sequence, element.name])
                        });
                        console.log(self.element_names);
                    })
            }
        },
        
        generate_string: function () {
            var names = this.element_names;
            var target_string = _.reduce($.find('#declare-element-names input'), function (meno, input) {
                meno += '|';
                meno += input.val();
            }, '');
            if (target_string){
                target_string += '|';
            }
            this.$el.val(target_string)
        }
    });

    core.form_widget_registry.add('declare_element', FieldDeclareElement)
});