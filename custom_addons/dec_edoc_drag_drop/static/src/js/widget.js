odoo.define('dec_edoc_drag_drop.form_widgets', function (require) {
    "use strict";

    var core = require('web.core');
    var form_common = require('web.form_common');
    var Many2ManyBinary = core.form_widget_registry.get('many2many_binary');
    var _t = core._t;
    var QWeb = core.qweb;
    var Model = require('web.DataModel');

    var upload_images = [];
    var immagini = [];
    var reload = true;
    var onenter = false;
    var last_sort_number = 0;

    var res_model_id = 0;
    var res_model_name = "ir.attachment";

    var PreviewDialog = require('muk_preview.PreviewDialog');
    var utils = require('web.utils');

    var multidragndrop_edoc = Many2ManyBinary.extend({
        template: "dragndropmulti_edoc_template",
        read_name_values: function () {

            var self = this;
            // don't reset know values
            var ids = this.get('value');
            var _value = ids;
            // send request for get_name
            if (_value.length) {
                return this.ds_file.call('read', [_value, ['id', 'name', 'datas_fname', 'extension', 'description', 'sortable', 'dec_edoc_type']]).then(function (datas) {
                    _.each(datas, function (data) {
                        data.no_unlink = true;
                        data.url = self.session.url('/web/image', {
                            model: 'ir.attachment',
                            field: 'datas',
                            filename_field: 'datas_fname',
                            id: data.id
                        });
                        self.data[data.id] = data;
                    });


                    function compare(a, b) {
                        if (a.sortable < b.sortable)
                            return -1;
                        if (a.sortable > b.sortable)
                            return 1;
                        return 0;
                    }

                    datas = $(datas).sort(compare);

                    var ids_sorted = [];

                    for (var i = 0; i < datas.length; i++) {
                        ids_sorted.push(datas[i].id);
                        last_sort_number = datas[i].sortable;
                    }

                    return ids_sorted;

                });
            } else {
                return $.when(ids);
            }
        },
        render_value: function () {
            var model_id_filed_name = this.options && this.options.res_model_id;
            if (model_id_filed_name) {
                //这里可能会提示错误 Uncaught TypeError: Cannot read property 'get_value' of undefined)，使用该控件时必须用options="{'res_model_id':'id','res_model_name':'customs_center.customs_dec'}"options="{'res_model_id':'id','res_model_name':'options="{'res_model_id':'id','res_model_name':'customs_center.customs_dec'}"'}"
                res_model_id = this.field_manager.get_field_value(model_id_filed_name);
            }

            res_model_name = this.options && this.options.res_model_name;

            var self = this;
            this.read_name_values().then(function (ids) {

                var render = $(QWeb.render('dragndropmulti_edoc_template.images', {'widget': self, 'values': ids}));
                render.on('click', '.oe_delete', _.bind(self.on_file_delete, self));
                self.$('.oe_placeholder_files, .oe_attachments').replaceWith(render);

                var fancy_size = $('.image_gallery').size();
                if (fancy_size > 0) {
                    $('.image_gallery').magnificPopup({
                        delegate: 'a', // child items selector, by clicking on it popup will open
                        type: 'image',
                        gallery: {enabled: true},
                        image: {
                            markup: '<div class="mfp-figure">' +
                            '<div class="mfp-close"></div>' +
                            '<div class="mfp-img"></div>' +
                            '<div class="mfp-bottom-bar">' +
                            '<div class="mfp-title"></div>' +
                            '<div class="mfp-counter"></div>' +
                            '</div>' +
                            '</div>',

                            titleSrc: function (item) {
                                return item.el.attr('title') +
                                    '<div style="margin-top: -45px;"><a style="padding:5px; color:black; background-color:white; text-align:center;" href="' + item.src + '" >Download</a></div>';
                            },
                            tError: "<a href='%url%'><img src='/dec_edoc_drag_drop/static/src/img/down.png' style='margin-top:-100px;' width='200' /><br/><p>Download File</p></a>"
                        }
                    });


                }

                // reinit input type file
                var $input = self.$('input.oe_form_binary_file');
                $input.after($input.clone(true)).remove();
                self.$(".oe_fileupload").show();

                $('.oe_form_button_save').click(function (e) {
                    self.on_button_save(e, self);
                });

                $('.o_binary_preview').click(function () {
                    var value = '';
                    var filename = $(this).attr('filename');

                    PreviewDialog.createPreviewDialog(self, '/web/content?' + $.param({
                            'model': "ir.attachment",
                            'id': $(this).attr('id'),
                            'field': 'datas',
                            'filename_field': 'datas_fname',
                            'filename': filename,
                            'download': true,
                            'data': utils.is_bin_size(value) ? null : value,
                        }), false, filename ? filename.split('.').pop() : false, filename);
                })


                $('.sortable').sortable({
                    stop: function (event, ui) {
                        /*Salvo l'ordine di sort degli attachment*/
                        var attachments_sort = [];

                        $(this).find('li').each(function () {
                            var id_attachments = $(this).attr('id');
                            attachments_sort.push(id_attachments);
                        });

                        /*eseguo la chiamata al model per aggiornare il sortable*/
                        var model = new Model("ir.attachment");
                        model.call("update_sort_attachment", [], {attachments_ids: attachments_sort}).then(function (result_id) {

                            //aggiorno la grafica
                            console.log('aggiornato sort nel database');

                        });
                    }
                });

                var overlay = self.$el.find('.dragndrop-overlay');
                var dragndrop_input = self.$el.find('.dragndrop-input');
                var dropfileshere = self.$el.find('.dropfileshere');

                $(overlay).on(
                    'dragover',
                    function (e) {
                        e.preventDefault();
                        e.stopPropagation();
                    });

                $(overlay).on(
                    'dragleave',
                    function (e) {
                        e.preventDefault();
                        e.stopPropagation();
                        $(dropfileshere).css('display', 'initial');
                        $(overlay).css('display', 'none');
                    });

                $(overlay).on(
                    'dragenter',
                    function (e) {
                        e.preventDefault();
                        e.stopPropagation();
                    });

                $(dragndrop_input).on(
                    'dragover',
                    function (e) {
                        e.preventDefault();
                        e.stopPropagation();
                        $(dropfileshere).css('display', 'none');
                        self.show_upload_overlay($(overlay));
                    })

                $(overlay).on('drop', function (e) {
                    if (e.originalEvent.dataTransfer) {
                        if (e.originalEvent.dataTransfer.files.length) {
                            e.preventDefault();
                            e.stopPropagation();
                            /*UPLOAD FILES HERE*/
                            var files = e.originalEvent.dataTransfer.files;
                            for (var i = 0; i < files.length; i++) {
                                if (jQuery.inArray(files[i].name, immagini) == -1) {
                                    immagini.push(files[i].name);
                                    self.base64_image(files[i]);
                                }
                            }
                        }
                        $(overlay).css('display', 'none');

                    }
                });


                $('.dragndropdescription').on('change', function () {
                    var id_attachment = $(this).attr('id');
                    var description_value = $(this).val();
                    console.log('update: ' + id_attachment + " con: " + description_value);
                    var model = new Model("ir.attachment");
                    model.call("attachment_update_description", [], {
                        id: id_attachment,
                        description: description_value
                    }).then(function (result_id) {

                        //aggiorno la grafica
                        self.render_value();

                    });


                });

                $('.dragndrop_dec_edoc_type').on('change', function () {
                    var id_attachment = $(this).attr('id');
                    var dec_edoc_type = $(this).val();
                    console.log('update: ' + id_attachment + " con: " + dec_edoc_type);
                    var model = new Model("ir.attachment");
                    model.call("attachment_update_dec_edoc_type", [], {
                        id: id_attachment,
                        dec_edoc_type: dec_edoc_type
                    }).then(function (result_id) {

                        //aggiorno la grafica
                        //self.render_value();

                    });
                });

            });
        },
        on_button_save: function (e, self) {
            self.render_value();
        },
        base64_image: function (file) {
            var self = this;

            var name = file.name;
            var reader = new FileReader();

            reader.onload = function (e) {
                var srcData = e.target.result;
                var base64_image = srcData.substring(srcData.lastIndexOf(",") + 1, srcData.length);
                // Attach file Size
                var attach_file_size = base64_image.length;
                // 将随附单据base64 转换成文件流大小fileLength
                var fileLength = parseInt(attach_file_size - (attach_file_size / 8) * 2);
                var extension_file = "";
                var extension = name.split('.').pop();

                console.log(extension);

                // https://bugzilla.mozilla.org/show_bug.cgi?id=453805
                if (extension == 'pdf') {
                    //File SIZE
                    if (fileLength >= 4190000) {
                        alert("单据附件大小不能超过4M,请重新上传!");
                        return false;
                    } else {
                        //File PDF
                        extension_file = "pdf";
                        var model = new Model("ir.attachment");
                        model.call("upload_dragndrop_dec_edoc", [], {
                            res_model_id: res_model_id,
                            res_model_name: res_model_name,
                            name: file.name,
                            base64: base64_image,
                            extension: extension_file,
                            sortable: last_sort_number + 1
                        }).then(function (result_id) {
                            console.log(result_id);
                            var values = _.clone(self.get('value'));
                            values.push(parseInt(result_id));
                            upload_images[file.name] = parseInt(result_id);
                            console.log('file non presente, lo carico');
                            self.set({'value': values});
                        });
                    }
                } else {
                    alert("单据附件只支持.pdf类型文件！请重新上传！");
                    return false;
                }
            }
            reader.readAsDataURL(file);

        },

        on_file_delete: function (event) {
            event.stopPropagation();
            var file_id = $(event.target).data("id");
            for (var key in upload_images) {

                if (upload_images[key] == file_id) {
                    delete upload_images[key];
                    var indice = immagini.indexOf(key);
                    delete immagini[indice];
                    console.log("eliminato");
                }

            }

            if (file_id) {
                var files = _.filter(this.get('value'), function (id) {
                    return id != file_id;
                });
                if (!this.data[file_id].no_unlink) {
                    this.ds_file.unlink([file_id]);
                }
                this.set({'value': files});
            }
        },
        show_upload_overlay: function (overlay) {
            $(overlay).css('display', 'initial');
            var width = $(overlay).prev().width();
            var height = $(overlay).prev().height();
            $(overlay).css('width', width + 4 + "px");
            $(overlay).css('height', height + 5 + 'px');
            //$(overlay).css('background-color','#5C5B80');
            //$(overlay).css('margin-top',-(height+8)+"px");
            $(overlay).css('margin-left', "20px");
            $(overlay).css('position', 'absolute');
            $(overlay).css('background-color', '#5C5B80');
            $(overlay).css('text-align', 'center');
            $(overlay).css('line-height', height + 'px');
            $(overlay).html('<a style="color:white; font-weight:bolder; -webkit-margin:0px; font-size: 25px;">UPLOAD</a>')
            if ($.browser.mozilla) {
                //fix issue 205
                $(overlay).css('right', '50%');
                $(overlay).css('margin-right', -((width + 4) / 2) + "px");
            }
        },

    });


    core.form_widget_registry.add('multidragndrop_edoc', multidragndrop_edoc);

});