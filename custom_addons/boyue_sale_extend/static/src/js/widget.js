odoo.define('sale_extend', function (require) {
    var core = require('web.core');
    var form_relational = require('web.form_relational');

    var FieldMany2ManyTagsRows = form_relational.FieldMany2ManyTags.extend({
           tag_template: "FieldMany2ManyTagRows"
       });

    core.form_widget_registry.add('many2many_tags_rows', FieldMany2ManyTagsRows)
});