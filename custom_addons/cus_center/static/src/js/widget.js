odoo.define('customs_center', function (require) {
    var core = require('web.core');
    var FormWidget = require('web.form_widgets');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    var result_goods_model = '';//规格型号录入结果
    var modal_id = '';//bootstrap模态框id
    var element_names=[];
    QWeb.add_template('/customs_center/static/src/xml/declare_element_modal.xml');

    var FieldDeclareElement = FormWidget.FieldChar.extend({

        init: function () {
            this._super.apply(this, arguments);
            this.set({'tariff': false});
            var tariff_field = this.options && this.options.tariff;
            if (tariff_field) {
                this.field_manager.on("field_changed:" + tariff_field, this, function () {
                    this.set({'tariff': this.field_manager.get_field_value('' + tariff_field)})
                })
            }
            this.on('change:tariff', this, this.get_element_name);
            element_names = [];

        },

        events: {
            'focus': 'show_ele_modal'
        },

        renderElement: function () {
            this._super();
            var self = this;
            this.modal_id = _.uniqueId("dec-modal-");

            modal_id = this.modal_id;

            var temp = $(QWeb.render("declare_element_modal"));
            temp.prop('id', this.modal_id);
            setTimeout(function () {
                $('body').append(temp);
                $('#' + modal_id + ' button.oe_highlight').on('click', self, self.submit);//点击确定时，根据窗口中各申报要素录入结果，计算出规格型号，填到规格型号文本框中
            }, 1000);

        },

        destroy: function () {
            console.log("destroy");

        },

        show_ele_modal: function () {
            $('#' + modal_id).modal();
            var display_board = $('#' + modal_id + ' #declare-element-names');
            display_board.empty();
            var self = this;
            var input_tags = [];

            _.each(element_names, function (element_name) {
                var ele_name = element_name[1];
                var sequence = element_name[0];

                var input_tag;
                // 要素名为品牌类型、出口享惠情况时，比较特殊，需要用下拉框选择，其他要素可以直接用文本框
                if (ele_name == "品牌类型") {
                    var select_brand = '<select class="col-md-6" id="select_dec_ele_0" onchange="$(\'#dec-ele-0\').val(this.value)">' +
                        '<option value="0">0-无品牌</option>' +
                        '<option value="1">1-境内自主品牌</option>' +
                        '<option value="2">2-境内收购品牌</option>' +
                        '<option value="3">3-境外品牌(贴牌生产)</option>' +
                        '<option value="4">4-境外品牌(其他)</option>' +
                        '</select>';

                    input_tag = $('<div class="row" style="padding-bottom: 20px">'
                        + '<div class="col-md-2"><label for="' + 'dec-ele-' + sequence + '">' + ele_name + '</label></div>'
                        + '<div class="col-md-8"><input  class="col-md-1" value="0" readonly="true"  id="' + 'dec-ele-' + sequence + '"/>' + select_brand + '</div>'
                        + '</div>');
                } else if (ele_name == "出口享惠情况") {
                    var select_out = '<select class="col-md-6" id="select_dec_ele_1" onchange="$(\'#dec-ele-1\').val(this.value)">' +
                        '<option value="0">0-出口货物在最终目的国（地区）不享受优惠关税</option>' +
                        '<option value="1">1-出口货物在最终目的国（地区）享受优惠关税</option>' +
                        '<option value="2">2-出口货物不能确定在最终目的国（地区）享受优惠关税</option>' +
                        '<option value="3">3-不适用于进口报关单</option>' +
                        '</select>';

                    input_tag = $('<div class="row" style="padding-bottom: 20px">'
                        + '<div class="col-md-2"><label for="' + 'dec-ele-' + sequence + '">' + ele_name + '</label></div>'
                        + '<div class="col-md-8"><input  class="col-md-1" value="0" readonly="true"  id="' + 'dec-ele-' + sequence + '"/>' + select_out + '</div>'
                        + '</div>');
                } else {
                    input_tag = $('<div class="row" style="padding-bottom: 20px">'
                        + '<div class="col-md-2"><label for="' + 'dec-ele-' + sequence + '">' + ele_name + '</label></div>'
                        + '<div class="col-md-8"><input class="col-md-7" class="o_form_label" id="' + 'dec-ele-' + sequence + '"/></div>'
                        + '</div>');
                }

                display_board.append(input_tag);
                input_tags.push(input_tag)
            });

            var input_vals = self.$input.val();
            if (input_vals) {
                var vals = input_vals.split('|');
                $.each(input_tags, function (idx, obj) {
                    if (idx == 0) {
                        $("#select_dec_ele_0").val(vals[idx]);
                    } else if (idx == 1) {
                        $("#select_dec_ele_1").val(vals[idx]);
                    } else {
                        obj.find('input').val(vals[idx])
                    }

                })
            }

            $('#declare-element-names input').on('change', self, self.generate_goods_model_preview);
            $('#declare-element-names select').on('change', self, self.generate_goods_model_preview);

            self.generate_goods_model_preview();
        },

        remove_field: function () {
            var display_board = $('#declare-element-names');
            display_board.empty();

        },

        get_element_name: function () {
            if (this.get('tariff')) {
                var goods_tariffModel = new Model('cus_args.goods_tariff');
                var goods = '';
                var goods_hs_code = '';
                // 先根据税则id从税则库查出hscode
                goods = goods_tariffModel.query(['code_ts']).filter([['id', '=', this.get('tariff')]])
                    .first()
                    .then(function (goods) {
                        goods_hs_code = goods["code_ts"];

                        var DeclareElement = new Model('cus_args.goods_declare_element');
                        var self = this;
                        if (self.$input)
                            self.$input.val('');
                        element_names = [];

                        //根据hscode从申报要素表查出相应申报要素（集合）
                        DeclareElement.query(['name_cn', 'sequence']).filter([['goods_tariff_hs_code', '=', goods_hs_code]])
                            .order_by('sequence')
                            .all()
                            .then(function (elements) {
                                _.each(elements, function (element) {
                                    element_names.push([element.sequence, element.name_cn])
                                });
                                element_names.push([5, '其他']);
                                console.log(element_names)


                            })

                    });

            }
        },

        submit: function (event) {
            console.log(event);
            var self = event.data;
            self.$input.val(result_goods_model);
            $('#' + modal_id).modal('hide');

            //点击确定时，将焦点移动到下一控件
            var inputs = $("input"); // 获取表单中的所有输入框
            var idx = inputs.index(self.$input);
            if (idx < inputs.length - 1) {
                inputs[idx + 1].focus();
            }

            self.destroy();
        },
        generate_goods_model_preview: function (event) {
            var inputs = $('#' + modal_id + ' #declare-element-names input');//避免获取到上一次录入的数据
            //console.log(inputs);
            //console.log(modal_id);

            var values = [];
            inputs.each(function () {
                values.push($(this).val());
            });

            result_goods_model = _.reduce(values, function (meno, value, index) {
                //console.log(index,value)
                if (index == 0) {
                    return value;
                } else {
                    return meno + '|' + value;
                }

            }, '');

            $("p[name='goods_model_preview']").text(result_goods_model);
            $("p[name='goods_model_preview_count']").text(result_goods_model.length + '/255');

            //超出255个字符时标红提醒
            if (result_goods_model.length > 255) {
                $("p[name='goods_model_preview']").css('color', 'red');
                $("p[name='goods_model_preview_count']").css('color', 'red');
            } else {
                $("p[name='goods_model_preview']").css('color', 'black');
                $("p[name='goods_model_preview_count']").css('color', 'black');
            }
        }
    });

    core.form_widget_registry.add('declare_element', FieldDeclareElement)
});