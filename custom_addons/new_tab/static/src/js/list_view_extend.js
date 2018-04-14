
odoo.define('new_tab.ListViewExtend', function (require) {
"use strict";


//console.log("list view callleddddddddddddddddddddddddddddddddddddddddddddd")
var ControlPanel = require('web.ControlPanel');
var core = require('web.core');
var data = require('web.data');
var Dialog = require('web.Dialog');
var common = require('web.form_common');
var ListView = require('web.ListView');
var Model = require('web.DataModel');
var session = require('web.session');
var utils = require('web.utils');
var ViewManager = require('web.ViewManager');

var Class = core.Class;
var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;
var list_widget_registry = core.list_widget_registry;

// ListView Inlcuded new_tab features
var ListViewExtend = ListView.include({
	//console.log("ListViewExtend view callleddddddddddddddddddddddddddddddddddddddddddddd")
    defaults: _.extend({}, ListView.prototype.defaults, {
        // records can be selected one by one
        
        selectable: true,
        //self modify
        'new_tab': true,
        // list rows can be deleted
        deletable: false,
        // whether the column headers should be displayed
        header: true,
        // display addition button, with that label
        addable: _lt("Create"),
        // whether the list view can be sorted, note that once a view has been
        // sorted it can not be reordered anymore
        sortable: true,
        // whether the view rows can be reordered (via vertical drag & drop)
        reorderable: true,
        action_buttons: true,
        //whether the editable property of the view has to be disabled
        disable_editable_mode: false,
    }),
    
 });   
    

// ListView.List Inlcuded new_tab in List view    
var ListViewInherit = ListView.List.include({
    
	init: function(group, opts) {
	        var self = this;
        //console.log("**************************************self",self,group, opts)
		this._super(group, opts);
		//this.options = {};
        
        
		this.$current = $('<tbody>')
		
		 .delegate('input[readonly=readonly]', 'click', function (e) {
                /*
                    Against all logic and sense, as of right now @readonly
                    apparently does nothing on checkbox and radio inputs, so
                    the trick of using @readonly to have, well, readonly
                    checkboxes (which still let clicks go through) does not
                    work out of the box. We *still* need to preventDefault()
                    on the event, otherwise the checkbox's state *will* toggle
                    on click
                 */
                e.preventDefault();
            })
            .delegate('td.o_list_record_selector', 'click', function (e) {
                e.stopPropagation();
                var selection = self.get_selection();
                var checked = $(e.currentTarget).find('input').prop('checked');
                $(self).trigger(
                        'selected', [selection.ids, selection.records, ! checked]);
            })
            .delegate('td.o_list_record_delete', 'click', function (e) {
                e.stopPropagation();
                var $row = $(e.target).closest('tr');
                $(self).trigger('deleted', [[self.row_id($row)]]);
                // IE Edge go crazy when we use confirm dialog and remove the focused element
                if(document.hasFocus && !document.hasFocus()) {
                    $('<input />').appendTo('body').focus().remove();
                }
            })
            .delegate('td button', 'click', function (e) {
                e.stopPropagation();
                var $target = $(e.currentTarget),
                      field = $target.closest('td').data('field'),
                       $row = $target.closest('tr'),
                  record_id = self.row_id($row);
                
                if ($target.attr('disabled')) {
                    return;
                }
                $target.attr('disabled', 'disabled');

                // note: $.data converts data to number if it's composed only
                // of digits, nice when storing actual numbers, not nice when
                // storing strings composed only of digits. Force the action
                // name to be a string
                $(self).trigger('action', [field.toString(), record_id, function (id) {
                    $target.removeAttr('disabled');
                    return self.reload_record(self.records.get(id));
                }]);
            })
            .delegate('a', 'click', function (e) {
                e.stopPropagation();
            })
           
            //self modification
            .delegate('a.new_tab', 'click', function (e) {
                e.stopPropagation();
	        var row_id = self.row_id(e.currentTarget);
                //console.log("in click a***====>>>>",self.options.action);
			if(self.options.action)
                          {		
              			var url = "/web#id="+row_id+"&view_type=form&model="+self.dataset.model+"&menu_id="+self.options.action["menu_id"]+"&action="+self.options.action["id"]
              			//console.log("urllllllllllllllllllllllllllllllllllllllllllllllll",url)
                                window.open(url,'_blank');
				stop();
		          }
                        else{
                                alert("sry not available here")
                             }
				//var url = "/id="+row_id+"&view_type=form&model="+self.dataset.model+"&menu_id="+self.options.action["menu_id"]+"&action="+self.options.action["id"]
				
					
            })
            
            .delegate('tr', 'click', function (e) {
                var row_id = self.row_id(e.currentTarget);
                if (row_id) {
                    e.stopPropagation();
                    if (!self.dataset.select_id(row_id)) {
                        throw new Error(_t("Could not find id in dataset"));
                    }
                    self.row_clicked(e);
                }
            });
            

    },
        
 
});



});
