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
          var self = this;
          this.modal_id = _.uniqueId("dec-modal-");
          var temp = $(QWeb.render("declare_element_modal"));
          temp.prop('id', this.modal_id);
          setTimeout(function () {
              $('body').append(temp);
              $('#'+self.modal_id+' button.oe_highlight').on('click', self, self.generate_string)
          }, 1000);
        },

        destroy: function () {
            $('#'+this.modal_id).remove();
            this._super.apply(this, arguments)
        },

        show_ele_modal: function () {
            $('#' + this.modal_id).modal();
            var self = this;
            var display_board = $('#'+self.modal_id+' #declare-element-names');
            display_board.empty();
            var input_tags = [];
            console.log(self.element_names);
            _.each(self.element_names, function (element_name) {
                var ele_name = element_name[1];
                var sequence = element_name[0];
                var temp = _.template(self.input_temp);
                var field = temp({field_id: 'dec-ele-'+sequence, name: ele_name});
                var input_tag = $(field);
                display_board.append(input_tag);
                input_tags.push(input_tag)
            });
            var input_vals = self.$input.val();
            if(input_vals)
            {
                var vals = input_vals.split('|');
                $.each(input_tags, function (idx, obj) {
                    obj.find('input').val(vals[idx+1])
                })
            }
             console.log(display_board.html());
        },

        remove_field: function () {
            var display_board = $('#declare-element-names');
            display_board.empty()
        },

        get_element_name: function () {
            if (this.get('tariff')){
                var DeclareElement = new Model('declare_element');
                var self = this;
                if(self.$input)
                    self.$input.val('');
                self.element_names = [];
                DeclareElement.query(['name', 'sequence']).filter([['cus_goods_tariff_id', '=', self.get('tariff')]])
                    .order_by('sequence')
                    .all()
                    .then(function (elements) {
                        _.each(elements, function (element) {
                            self.element_names.push([element.sequence, element.name])
                        });
                    })
            }
        },

        generate_string: function (event) {
            var self = event.data;
            var inputs = $('#declare-element-names input');
            var values = [];
            inputs.each(function () {
               values.push($(this).val());
            });
            console.log(values);
            var target_string = _.reduce(values, function (meno, value) {
                return meno + '|' + value;
            }, '');
            if (target_string){
                target_string += '|';
            }
            self.$input.val(target_string);
            $('#'+self.modal_id).modal('hide');
        }
    });

    core.form_widget_registry.add('declare_element', FieldDeclareElement)
});