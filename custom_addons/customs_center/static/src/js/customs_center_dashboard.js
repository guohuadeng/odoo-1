odoo.define("customs_center.customs_center_dashboard", function(require) {
    "use strict";
     
    var core = require("web.core");
    var dataset = require("web.data");
    var Widget = require("web.Widget");
    var Model = require("web.Model");
    var _t = core._t;
    var QWeb = core.qweb;
    
    var customs_dashboard = Widget.extend({
        template: 'Prjects_dashboard',
        events:{
            'change #projects_selectbox': 'projects_selectbox_onchange',
            'click #get_cus_send_count':'get_cus_send_count',
            'click #get_chart_employee_timesheet':'get_chart_employee_timesheet',
            'click #get_chart_project_timesheet':'get_chart_project_timesheet',
            'click #get_chart_employee_task' : 'get_chart_employee_task',
            'click #get_chart_project_task' : 'get_chart_project_task',
            'click #get_chart_employee_task_2' : 'get_chart_employee_task_2',
            'click #get_chart_employee_task_2_sync' : 'get_chart_employee_task_2_sync',
            'click #get_chart_employee_task_3' : 'get_chart_employee_task_3',
            'click #get_chart_employee_task_3_sync' : 'get_chart_employee_task_3_sync',
            'click #get_chart_employee_issue' : 'get_chart_employee_issue',
            'click #get_chart_project_issue' : 'get_chart_project_issue',
        },
        //Filter by project
        projects_selectbox_onchange:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            if (current_val == -1) {
                $(".first-client-block").show();
                $(".user-activities-timeline").show();
            }else{
                $(".first-client-block").hide();
                $(".user-activities-timeline").hide();
            }
            self.fetchblocks(current_val);
        },
        
        //Timesheet charts
        get_chart_employee_timesheet:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-timesheet-link").removeClass('active');
            $(e.currentTarget).addClass('active');
 
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            customs_center_dashboard.call('get_chart_employee_timesheet',[project_id,]).then(function(data){
                self.drawChart_employee_timesheet(data,'User / Timesheet');
            });
        },
        get_chart_project_timesheet:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-timesheet-link").removeClass('active');
            $(e.currentTarget).addClass('active');
 
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            customs_center_dashboard.call('get_chart_project_timesheet',[project_id,]).then(function(data){
                self.drawChart_employee_timesheet(data,'Project / Timesheet');
            });
        },

        // 仪表板 头部各按钮获取相关数据，跳转到相应列表视图
        get_cus_send_count:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-tasks-link").removeClass('active');
            $(e.currentTarget).addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            customs_center_dashboard.call('get_cus_send_count',[project_id,])
        },
        
        //Tasks charts
        get_chart_employee_task:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-tasks-link").removeClass('active');
            $(e.currentTarget).addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            customs_center_dashboard.call('get_chart_employee_tasks',[project_id,]).then(function(data){
                self.drawChart_employee_task(data,'Employee / Task');
            });
        },
        get_chart_employee_task_2:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-tasks-link").removeClass('active');
            $(e.currentTarget).addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            var cus_or_sync = $("#get_chart_employee_task_2").text();
            customs_center_dashboard.call('get_chart_employee_tasks_2',[project_id,cus_or_sync]).then(function(data){
                self.drawChart_employee_task_2(data,'Employee / Task');
            });
        },

        get_chart_employee_task_2_sync:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-tasks-link").removeClass('active');
            $(e.currentTarget).addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            var cus_or_sync = $("#get_chart_employee_task_2_sync").text();
            customs_center_dashboard.call('get_chart_employee_tasks_2',[project_id,cus_or_sync]).then(function(data){
                self.drawChart_employee_task_2(data,'Employee / Task');
            });
        },

        get_chart_employee_task_3:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-tasks-link").removeClass('active');
            $(e.currentTarget).addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            var cus_or_sync = $("#get_chart_employee_task_3").text();
            customs_center_dashboard.call('get_chart_employee_tasks_3',[project_id,cus_or_sync]).then(function(data){
                self.drawChart_employee_task_3(data,'Employee / Task');
            });
        },

        get_chart_employee_task_3_sync:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-tasks-link").removeClass('active');
            $(e.currentTarget).addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            var cus_or_sync = $("#get_chart_employee_task_3_sync").text();
            customs_center_dashboard.call('get_chart_employee_tasks_3',[project_id,cus_or_sync]).then(function(data){
                self.drawChart_employee_task_3(data,'Employee / Task');
            });
        },

        get_chart_project_task:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-tasks-link").removeClass('active');
            $(e.currentTarget).addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            customs_center_dashboard.call('get_chart_project_tasks',[project_id,]).then(function(data){
                self.drawChart_employee_task(data,'Project / Task');
            });
        },
        //Issues charts
        get_chart_employee_issue:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-issues-link").removeClass('active');
            $(e.currentTarget).addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            customs_center_dashboard.call('get_chart_employee_issues',[project_id,]).then(function(chart_employee_issues){
                self.drawChart_employee_issue(chart_employee_issues,'Employee / Issue');
            });
        },
        get_chart_project_issue:function(e){
            var self = this;
            var current_val = $(e.currentTarget).val();
            $(".chart-issues-link").removeClass('active');
            $(e.currentTarget).addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var project_id = $("#projects_selectbox").val();
            customs_center_dashboard.call('get_chart_project_issues',[project_id,]).then(function(chart_project_issues){
                self.drawChart_employee_issue(chart_project_issues,'Project / Issue');
            });
        },
        start: function(){
            var self = this;
            var customs_center_dashboard = new Model('customs_center.dashboard');
            customs_center_dashboard.call('get_all_projects',[[]]).done(function(projects){
                _.each(projects,function(project){
                    $('.projects-container select').append('<option value="' + project.id + '">'+ project.name  +'</option>') 
                });
            });
            self.fetchblocks(-1)
        },
        fetchblocks : function(project_id){
            var self = this;
            $(".chart-timesheet-link").removeClass('active');
            $(".chart-issues-link").removeClass('active');
            $(".chart-tasks-link").removeClass('active');
            $(".chart-timesheet-link-1").addClass('active');
            $(".chart-issues-link-1").addClass('active');
            $(".chart-tasks-link-1").addClass('active');
            var customs_center_dashboard = new Model('customs_center.dashboard');
            var cus_or_sync = $("#get_chart_employee_task_2").text();
            customs_center_dashboard.call('get_projects_dashboard_data',[project_id,cus_or_sync]).then(function(projects){
                $(".total_clients").html(projects.total_clients);
                $(".total_employees").html(projects.total_employees);
                $(".total_projects").html(projects.total_projects);
                $(".total_paid_invoice").html(projects.total_paid_invoice);
                $(".total_hour_logged").html(parseFloat((projects.total_hour_logged.toFixed(2))));
                $(".total_pending_tasks").html(projects.total_pending_tasks);
                $(".total_complete_tasks").html(projects.total_complete_tasks);
                $(".total_overdue_tasks").html(projects.total_overdue_tasks);
                $(".total_resolved_issues").html(projects.total_resolved_issues);
                $(".total_unresolved_issues").html(projects.total_unresolved_issues);
                $(".overdue-tasks-container").html(QWeb.render("overdue_tasks_template",{overdue_tasks: projects.overdue_tasks}));
                $(".pending-issue-container").html(QWeb.render("pending_issue_template",{pending_issues: projects.pending_issues}));
                $(".project-time-activity-container").html(QWeb.render("project_time_activity",{project_messages: projects.project_messages}));
                $(".user-activity-timeline-container").html(QWeb.render("user_activity_timeline",{user_activity_timeline: projects.user_activity_timeline}));
                // self.drawChart_employee_timesheet(projects.chart_employee_timesheet,'Employee / Timesheet');
                self.drawChart_employee_task(projects.chart_employee_tasks,'Employee / Task');
                // alert(projects.chart_employee_tasks);
                self.drawChart_employee_task_2(projects.chart_employee_tasks_2,'Employee / Task');
                self.drawChart_employee_task_3(projects.chart_employee_tasks_3,'Employee / Task');
                // self.drawChart_employee_issue(projects.chart_employee_issues,'Employee / Issue');
            });
        },
        drawChart_employee_timesheet: function(projects,title){
            var chart = Highcharts.chart('chart_timesheet', {
                chart: {
                    type: 'column'
                },
            
                title: {
                    text: ''
                },
            
                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical'
                },
            
                xAxis: {
                    // categories: projects.employee,
                },
            
                yAxis: {
                    title: {
                        text: 'Hours'
                    }
                },
            
                series: [{
                    name: 'Total hours logged',
                    data: projects.timesheet
                }],
            
                responsive: {
                    rules: [{
                        condition: {
                            maxWidth: 500
                        },
                        chartOptions: {
                            legend: {
                                align: 'center',
                                verticalAlign: 'bottom',
                                layout: 'horizontal'
                            },
                            yAxis: {
                                labels: {
                                    align: 'left',
                                    x: 0,
                                    y: -5
                                },
                                title: {
                                    text: null
                                }
                            },
                            subtitle: {
                                text: null
                            },
                            credits: {
                                enabled: false
                            }
                        }
                    }]
                }
            });
        },
        drawChart_employee_task : function(projects,title){
            var chart = Highcharts.chart('chart_employee_tasks', {
                chart: {
                    type: 'column'
                },

                title: {
                    text:"申报记录"
                },

                //
                colors: ['#a7875d','#8c8d96','#5fa479', '#ce534b'],

                xAxis: {
                    categories: ['报关单', '协同报关单']
                },
                credits: {
                    enabled: false   //右下角不显示LOGO
                },
                series: [{
                    name: '已申报',
                    data: projects.resolved
                }, {
                    name: '暂存成功',
                    data: projects.overdue
                }, {
                    name: '申报成功',
                    data: projects.unresolved
                }, {
                    name: '状态异常',
                    data: projects.decabnor
                }],
                // series: [{
                //     name: '已申报',
                //     data: [260, 320]
                // }, {
                //     name: '暂存成功',
                //     data: [180, 280]
                // }, {
                //     name: '申报成功',
                //     data: [175, 260]
                // }, {
                //     name: '状态异常',
                //     data: [15, 20]
                // }],
                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical'
                },
                yAxis: {
                    title: {
                        text: 'count of dec'
                    }
                }
                // responsive: {
                //     rules: [{
                //         condition: {
                //             maxWidth: 500
                //         },
                //         chartOptions: {
                //             legend: {
                //                 align: 'center',
                //                 verticalAlign: 'bottom',
                //                 layout: 'horizontal'
                //             },
                //             yAxis: {
                //                 labels: {
                //                     align: 'left',
                //                     x: 0,
                //                     y: -5
                //                 },
                //                 title: {
                //                     text: null
                //                 }
                //             },
                //             subtitle: {
                //                 text: null
                //             },
                //             credits: {
                //                 enabled: false
                //             }
                //         }
                //     }]
                // }
            });
        },



        drawChart_employee_task_2 : function(projects,title){
            var chart = Highcharts.chart('chart_employee_tasks_2', {
                chart: {
                    //plotBorderWidth: 1,
                    defaultSeriesType:"pie"
                },
                colors: [ '#8d8fcd', '#cab58f'],
                title: {
                    text:"进出口类型统计"
                },
                xAxis: {
                    categories: ['进口', '出口']
                },
                credits: {
                    enabled: false   //右下角不显示LOGO
                },
                series: [{
                        data: [
                         ['进口',  projects.import_count],
                         {
                            name: '出口',
                            y: projects.export_count,
                            sliced: true,
                            selected: true
                         }
                      ]
                }]
            });
        },


        drawChart_employee_task_3 : function(projects,title){
            var chart = Highcharts.chart('chart_employee_tasks_3', {
                chart: {
                    //plotBorderWidth: 1,
                    defaultSeriesType:"pie"
                },
                colors: [ '#38c5a7', '#d74839'],
                title: {
                    text:"通关率"
                },
                xAxis: {
                    categories: ['申报成功', '申报异常']
                },
                credits: {
                    enabled: false   //右下角不显示LOGO
                },
                series: [{
                    data: [
                             ['申报成功',   projects.dec_success_count],
                             {
                                name: '申报异常',
                                y: projects.dec_abnor_count,
                                sliced: true,
                                selected: true
                             }
                          ]
                }]

            });
        },


        drawChart_employee_issue : function(projects,title){
            var chart = Highcharts.chart('chart_employee_issues', {
                chart: {
                    type: 'column'
                },
            
                title: {
                    text: ''
                },
            
                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical'
                },
            
                xAxis: {
                    categories: projects.employee,
                },
            
                yAxis: {
                    title: {
                        text: 'Number of issues'
                    }
                },
            
                series: [{
                    name: 'Resloved',
                    data: projects.resolved
                }, {
                    name: 'Unresolved',
                    data: projects.unresolved
                }],
            
                responsive: {
                    rules: [{
                        condition: {
                            maxWidth: 500
                        },
                        chartOptions: {
                            legend: {
                                align: 'center',
                                verticalAlign: 'bottom',
                                layout: 'horizontal'
                            },
                            yAxis: {
                                labels: {
                                    align: 'left',
                                    x: 0,
                                    y: -5
                                },
                                title: {
                                    text: null
                                }
                            },
                            subtitle: {
                                text: null
                            },
                            credits: {
                                enabled: false
                            }
                        }
                    }]
                }
            });
        },
    });
    core.action_registry.add("dashboard_customs.dashboard", customs_dashboard);
});
