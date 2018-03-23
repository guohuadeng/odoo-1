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
                '<div class="col-md-2"><label for="<%= field_id %>"><%= name %></label></div>' +
                '<div class="col-md-6"><input class="o_form_label" id="<%= field_id %>"/></div>' +
                +'</div>'

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
            //console.log(self.element_names);
            _.each(self.element_names, function (element_name) {
                var ele_name = element_name[1];
                var sequence = element_name[0];
                var temp = _.template(self.input_temp);
                var field = temp({field_id: 'dec-ele-'+sequence, name: ele_name});
                //var input_tag = $(field);


                var input_tag;
                if(ele_name=="品牌类型"){
                    var select_pingpai='<select class="col-md-6" id="select_dec_ele_0" onchange="$(\'#dec-ele-0\').val(this.value)">' +
                    '<option value="0">0-无品牌</option>' +
                        '<option value="1">1-境内自主品牌</option>' +
                        '<option value="2">2-境内收购品牌</option>' +
                        '<option value="3">3-境外品牌(贴牌生产)</option>' +
                        '<option value="4">4-境外品牌(其他)</option>' +
                    '</select>';

                    input_tag=$('<div class="row" style="padding-bottom: 20px">'
                    +'<div class="col-md-2"><label for="'+'dec-ele-'+sequence+'">'+ele_name+'</label></div>'
                    +'<div class="col-md-8"><input class="col-md-1" value="0" readonly="true"  id="'+'dec-ele-'+sequence+'"/>'+select_pingpai+'</div>'
                    +'</div>');
                }else if(ele_name=="出口享惠情况"){
                    var select_chukou='<select class="col-md-6" id="select_dec_ele_1" onchange="$(\'#dec-ele-1\').val(this.value)">' +
                    '<option value="0">0-出口货物在最终目的国（地区）不享受优惠关税</option>' +
                        '<option value="1">1-出口货物在最终目的国（地区）享受优惠关税</option>' +
                        '<option value="2">2-出口货物不能确定在最终目的国（地区）享受优惠关税</option>' +
                        '<option value="3">3-不适用于进口报关单</option>'+
                    '</select>';

                    input_tag=$('<div class="row" style="padding-bottom: 20px">'
                    +'<div class="col-md-2"><label for="'+'dec-ele-'+sequence+'">'+ele_name+'</label></div>'
                    +'<div class="col-md-8"><input class="col-md-1" value="0" readonly="true"  id="'+'dec-ele-'+sequence+'"/>' +select_chukou+'</div>'
                    +'</div>');
                }else{
                    input_tag=$('<div class="row" style="padding-bottom: 20px">'
                    +'<div class="col-md-2"><label for="'+'dec-ele-'+sequence+'">'+ele_name+'</label></div>'
                    +'<div class="col-md-8"><input class="col-md-7" class="o_form_label" id="'+'dec-ele-'+sequence+'"/></div>'
                    +'</div>');
                }

                display_board.append(input_tag);
                input_tags.push(input_tag)
            });
            var input_vals = self.$input.val();
            if(input_vals)
            {
                var vals = input_vals.split('|');
                $.each(input_tags, function (idx, obj) {
                    obj.find('input').val(vals[idx])

                    if(idx==0){
                        $("#select_dec_ele_0").val(vals[idx]);
                    }else if(idx==1){
                        $("#select_dec_ele_1").val(vals[idx]);
                    }
                })
            }
            // console.log(display_board.html());
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
            var target_string = _.reduce(values, function (meno, value,index) {
               return meno + '|' + value;

            }, '');

            if (target_string.substr(0,1)=='|'){
                target_string=target_string.substr(1);
            }
            // if (target_string){
            //     target_string += '|';
            // }
            self.$input.val(target_string);
            $('#'+self.modal_id).modal('hide');

            //点击确定时，将焦点移动到下一控件
            var inputs = $("input"); // 获取表单中的所有输入框
            var idx = inputs.index(self.$input);
            if(idx<inputs.length-1){
                inputs[idx+1].focus();
            }
        }
    });

    core.form_widget_registry.add('declare_element', FieldDeclareElement)
});