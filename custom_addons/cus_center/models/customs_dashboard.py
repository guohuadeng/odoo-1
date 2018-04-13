# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime, timedelta
import calendar
from pytz import timezone
import pytz
import logging
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class CustomsCenterDashboard(models.Model):
    """ 关务仪表板 注意 这里只统计申报之后的报关单 不统计清单 及报关草单"""
    _name = 'customs_center.dashboard'

    @api.model
    def get_all_projects(self):
        # projects = self.env['project.project'].search_read(['|', ('active', '=', False), ('active', '=', True)],
        #                                                    ['id', 'name'])
        # return projects
        pass

    @api.model
    def get_projects_dashboard_data(self, project_id,cus_or_sync):
        cus_or_sync = '报关单'
        total_clients = self.get_total_clients(project_id)
        total_employees = self.get_total_employees(project_id)
        total_projects = self.get_total_projects(project_id)
        total_paid_invoice = self.get_total_paid_invoice(project_id)
        #total_hour_logged = self.get_total_hour_logged(project_id)
        #total_pending_tasks = self.get_total_pending_tasks(project_id)
        #total_complete_tasks = self.get_total_complete_tasks(project_id)
        #total_overdue_tasks = self.get_total_overdue_tasks(project_id)
        #total_resolved_issues = self.get_total_resolved_issues(project_id)
        #total_unresolved_issues = self.get_total_unresolved_issues(project_id)
        #overdue_tasks = self.get_overdue_tasks(project_id)
        #pending_issues = self.get_pending_issues(project_id)
        #project_messages = self.get_project_messages(project_id)
        #user_activity_timeline = self.get_user_activity_timeline(project_id)
        # chart_employee_timesheet = self.get_chart_employee_timesheet(project_id)
        chart_employee_tasks = self.get_chart_employee_tasks(project_id)
        chart_employee_tasks_2 = self.get_chart_employee_tasks_2(project_id, cus_or_sync)
        chart_employee_tasks_3 = self.get_chart_employee_tasks_3(project_id, cus_or_sync)
        #chart_employee_issues = self.get_chart_employee_issues(project_id)

        return {
            'total_clients': total_clients,
            'total_employees': total_employees,
            'total_projects': total_projects,
            'total_paid_invoice': total_paid_invoice,
           # 'total_hour_logged': total_hour_logged,
           # 'total_pending_tasks': total_pending_tasks,
            #'total_complete_tasks': total_complete_tasks,
            #'total_overdue_tasks': total_overdue_tasks,
           # 'total_resolved_issues': total_resolved_issues,
           # 'total_unresolved_issues': total_unresolved_issues,
           # 'overdue_tasks': overdue_tasks,
           #  'pending_issues': pending_issues,
           #  'project_messages': project_messages,
           #  'user_activity_timeline': user_activity_timeline,
           #  'chart_employee_timesheet': chart_employee_timesheet,
            'chart_employee_tasks': chart_employee_tasks,
            'chart_employee_tasks_2': chart_employee_tasks_2,
            'chart_employee_tasks_3': chart_employee_tasks_3,
           # 'chart_employee_issues': chart_employee_issues,
        }

    @api.model
    def get_total_clients(self, project_id):
        """ 发送申报数量 """
        # self.env.cr.execute(
        #     "select count(distinct partner_id) FROM project_project join account_analytic_account on account_analytic_account.id = analytic_account_id")
        # result = self.env.cr.fetchone()
        result = self.env['cus_center.customs_dec'].search_count(
            [('cus_dec_sent_way', 'in', ('single', 'QP'))])
        return result

    @api.model
    def get_total_employees(self, project_id):
        projects = self.env['cus_center.customs_dec'].search_count(
            [('cus_dec_rec_state', '=', '上载成功'), ('cus_dec_sent_way', '=', True)])
        return projects

    @api.model
    def get_total_projects(self, project_id):
        """ 申报成功 """
        projects = self.env['cus_center.customs_dec'].search_count(
            [('cus_dec_rec_state', '=', '申报成功'), ('cus_dec_sent_way', '=', True)])
        return projects

    @api.model
    def get_total_paid_invoice(self, project_id):
        """ 申报异常"""
        result = self.env['cus_center.customs_dec'].search_count(
            [('cus_dec_rec_state', 'in', ('上载失败', '导入失败','不被受理','退回修改','申报失败')),
             ('cus_dec_sent_way', '=', True)])
        return result

    @api.model
    def get_cus_send_count(self):
        customs_declaration_obj = self.env['cus_center.customs_dec']

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'cus_center.customs_dec',
            'target': 'new',
        }
        # return {
        #     'name': u"已申报列表",
        #     'type': "ir.actions.act_window",
        #     'view_type': 'tree',
        #     'view_mode': 'tree',
        #     'res_model': 'cus_center.customs_dec',
        #     'views': [[False, 'tree']],
        #     'res_id': customs_declaration_obj.ids,
        #     "domain": [['cus_dec_sent_way', 'in', ('single', 'QP')]],
        #     'target': 'new'
        # }

        # determine domain for selecting translations
        # record = self.env[model].with_context(lang=main_lang).browse(id)
        # domain = ['&', ('res_id', '=', id), ('name', '=like', model + ',%')]
        #
        # def make_domain(fld, rec):
        #     name = "%s,%s" % (fld.model_name, fld.name)
        #     return ['&', ('res_id', '=', rec.id), ('name', '=', name)]
        #
        # # insert missing translations, and extend domain for related fields
        # action = {
        #     'name': 'Translate',
        #     'res_model': 'ir.translation',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'tree',
        #     'view_id': self.env.ref('base.view_translation_dialog_tree').id,
        #     'target': 'current',
        #     'flags': {'search_view': True, 'action_buttons': True},
        #     'domain': domain,
        # }
        # if field:
        #     fld = record._fields[field]
        #     if not fld.related:
        #         action['context'] = {
        #             'search_default_name': "%s,%s" % (fld.model_name, fld.name),
        #         }
        # return action


    @api.model
    def get_total_hour_logged(self, project_id):

        timesheets = 10
        return timesheets

        # project_id = int(project_id)
        # domain = [] if project_id == -1 else [('project_id', '=', project_id)]
        # timesheets = sum(timesheet.unit_amount for timesheet in self.env['account.analytic.line'].search(domain))
        # return timesheets

    @api.model
    def get_total_pending_tasks(self, project_id):
        # done_stage = self.env.ref('project.project_stage_2')
        # cancelled_stage = self.env.ref('project.project_stage_3')
        #
        # project_id = int(project_id)
        # domain = [('stage_id', '!=', done_stage.id), ('stage_id', '!=', cancelled_stage.id)] if project_id == -1 else [
        #     ('stage_id', '!=', done_stage.id), ('stage_id', '!=', cancelled_stage.id), ('project_id', '=', project_id)]
        #
        # tasks = self.env['project.task'].search_count(domain)
        # return tasks
        pass

    @api.model
    def get_total_complete_tasks(self, project_id):
        # done_stage = self.env.ref('project.project_stage_2')
        #
        # project_id = int(project_id)
        # domain = [('stage_id', '=', done_stage.id)] if project_id == -1 else [('stage_id', '=', done_stage.id),
        #                                                                       ('project_id', '=', project_id)]
        #
        # tasks = self.env['project.task'].search_count(domain)
        # return tasks
        pass

    @api.model
    def get_total_overdue_tasks(self, project_id):
        pass

        # cancelled_stage = self.env.ref('project.project_stage_3')
        # project_id = int(project_id)
        # domain = [('date_deadline', '<', fields.Datetime.now()),
        #           ('stage_id', '!=', cancelled_stage.id)] if project_id == -1 else [
        #     ('date_deadline', '<', fields.Datetime.now()), ('project_id', '=', project_id),
        #     ('stage_id', '!=', cancelled_stage.id)]
        #
        # tasks = self.env['project.task'].search_count(domain)
        # return tasks

    @api.model
    def get_overdue_tasks(self, project_id):
        pass

        #
        # project_id = int(project_id)
        # domain = [('date_deadline', '<', fields.Datetime.now())] if project_id == -1 else [
        #     ('date_deadline', '<', fields.Datetime.now()), ('project_id', '=', project_id)]
        #
        # tasks = self.env['project.task'].search_read(domain, ['id', 'name', 'date_deadline', 'project_id'])
        # return tasks

    @api.model
    def get_total_resolved_issues(self, project_id):
        pass
        # done_stage = self.env.ref('project.project_stage_2')
        #
        # project_id = int(project_id)
        # domain = [('stage_id', '=', done_stage.id)] if project_id == -1 else [('stage_id', '=', done_stage.id),
        #                                                                       ('project_id', '=', project_id)]
        #
        # issues = self.env['project.issue'].search_count(domain)
        # return issues

    @api.model
    def get_total_unresolved_issues(self, project_id):
        pass
        #
        # done_stage = self.env.ref('project.project_stage_2')
        # cancelled_stage = self.env.ref('project.project_stage_3')
        #
        # project_id = int(project_id)
        # domain = [('stage_id', '!=', done_stage.id), ('stage_id', '!=', cancelled_stage.id)] if project_id == -1 else [
        #     ('stage_id', '!=', done_stage.id), ('stage_id', '!=', cancelled_stage.id), ('project_id', '=', project_id)]
        #
        # issues = self.env['project.issue'].search_count(domain)
        # return issues

    @api.model
    def get_pending_issues(self, project_id):
        pass

        # done_stage = self.env.ref('project.project_stage_2')
        # cancelled_stage = self.env.ref('project.project_stage_3')
        #
        # project_id = int(project_id)
        # domain = [('stage_id', '!=', done_stage.id), ('stage_id', '!=', cancelled_stage.id)] if project_id == -1 else [
        #     ('stage_id', '!=', done_stage.id), ('stage_id', '!=', cancelled_stage.id), ('project_id', '=', project_id)]
        #
        # issues = self.env['project.issue'].search_read(domain, ['id', 'name', 'project_id'])
        # return issues

    @api.model
    def get_project_messages(self, project_id):
        pass

        # project_id = int(project_id)
        #
        # messages = self.env['mail.message'].search_read(
        #     [('model', 'in', ('project.issue', 'project.task')), ('body', '!=', '')],
        #     ['res_id', 'model', 'body', 'date'], limit=30, order="id desc")
        # data = []
        # for message in messages:
        #     now_utc = datetime.utcnow()
        #     record_date_utc = datetime.strptime(message['date'], "%Y-%m-%d %H:%M:%S")
        #     d = now_utc - record_date_utc
        #     hours = d.seconds / 3600
        #     if d.days == 0 and hours < 1:
        #         date = 'from ' + str(d.seconds / 60) + ' minutes ago'
        #     elif d.days == 0 and hours < 24:
        #         date = 'from ' + str(hours) + ' hours ago'
        #     else:
        #         date = 'from ' + str(d.days) + ' days ago'
        #
        #     project_data = self.env[message['model']].browse(message['res_id'])
        #     if project_id == -1 or project_data.project_id.id == project_id:
        #         data.append({
        #             'body': message['body'],
        #             'date': str(date),
        #             'project': project_data.project_id.name if project_data.project_id else '' + ' | ' + project_data.name if project_data else '',
        #         })
        # return data

    @api.model
    def get_user_activity_timeline(self, project_id):
        pass

        # messages = self.env['mail.message'].search_read(
        #     [('body', '!=', ''), ('model', 'in', ('project.task', 'project.issue'))],
        #     ['res_id', 'model', 'create_uid', 'body', 'date'], limit=30, order="id desc")
        # data = []
        # for message in messages:
        #     now_utc = datetime.utcnow()
        #     record_date_utc = datetime.strptime(message['date'], "%Y-%m-%d %H:%M:%S")
        #     d = now_utc - record_date_utc
        #     hours = d.seconds / 3600
        #     if d.days == 0 and hours < 1:
        #         date = 'from ' + str(d.seconds / 60) + ' minutes ago'
        #     elif d.days == 0 and hours < 24:
        #         date = 'from ' + str(hours) + ' hours ago'
        #     else:
        #         date = 'from ' + str(d.days) + ' days ago'
        #
        #     user = self.env['res.users'].browse(message['create_uid'][0])
        #
        #     data.append({
        #         'user_name': user.name,
        #         'user_image': '/web/image?model=res.users&field=image_small&id=' + str(user.id),
        #         'body': message['body'],
        #         'date': str(date),
        #         'project': self.env[message['model']].browse(message['res_id']).name,
        #     })
        # return data

    @api.model
    def get_chart_employee_issues(self, project_id):
        pass

        # done_stage = self.env.ref('project.project_stage_2')
        # cancelled_stage = self.env.ref('project.project_stage_3')
        #
        # project_id = int(project_id)
        # domain = [('stage_id', '!=', cancelled_stage.id)] if project_id == -1 else [
        #     ('stage_id', '!=', cancelled_stage.id), ('project_id', '=', project_id)]
        #
        # users = []
        # resolved = []
        # unresolved = []
        # issues = self.env['project.issue'].search_read(domain, ['user_id', 'stage_id'])
        # for issue in issues:
        #     if issue['user_id'] not in users:
        #         users.append(issue['user_id'])
        #
        # for user in users:
        #     resolved_val = 0
        #     unresolved_val = 0
        #     for issue in issues:
        #         user_issue_id = issue['user_id'][0] if issue['user_id'] else False
        #         current_user = user[0] if user else False
        #         if issue['stage_id'][0] == done_stage.id and user_issue_id == current_user:
        #             resolved_val += 1
        #         elif user_issue_id == current_user:
        #             unresolved_val += 1
        #     resolved.append(resolved_val)
        #     unresolved.append(unresolved_val)
        #
        # return {
        #     'employee': [user[1] if user else 'Undefined' for user in users],
        #     'resolved': resolved,
        #     'unresolved': unresolved
        # }

    @api.model
    def get_chart_project_issues(self, project_id):
        # done_stage = self.env.ref('project.project_stage_2')
        # cancelled_stage = self.env.ref('project.project_stage_3')
        #
        # project_id = int(project_id)
        # domain = [('stage_id', '!=', cancelled_stage.id)] if project_id == -1 else [
        #     ('stage_id', '!=', cancelled_stage.id), ('project_id', '=', project_id)]
        #
        # projects = []
        # resolved = []
        # unresolved = []
        # issues = self.env['project.issue'].search_read(domain, ['stage_id', 'project_id'])
        # for issue in issues:
        #     if issue['project_id'] not in projects:
        #         projects.append(issue['project_id'])
        #
        # for project in projects:
        #     resolved_val = 0
        #     unresolved_val = 0
        #     for issue in issues:
        #         project_issue_id = issue['project_id'][0] if issue['project_id'] else False
        #         current_project = project[0] if project else False
        #         if issue['stage_id'][0] == done_stage.id and project_issue_id == current_project:
        #             resolved_val += 1
        #         elif project_issue_id == current_project:
        #             unresolved_val += 1
        #     resolved.append(resolved_val)
        #     unresolved.append(unresolved_val)
        #
        # return {
        #     'employee': [project[1] if project else 'Undefined' for project in projects],
        #     'resolved': resolved,
        #     'unresolved': unresolved
        # }
        pass


    @api.model
    def get_chart_employee_timesheet(self, project_id):
        project_id = int(project_id)
        domain = [] if project_id == -1 else [('project_id', '=', project_id)]
        timesheets = self.env['account.analytic.line'].search(domain)

        users = []
        timesheet_data = []
        for timesheet in timesheets:
            if timesheet.user_id not in users:
                users.append(timesheet.user_id)

        for user in users:
            timesheet_val = 0
            for timesheet in timesheets:
                if timesheet.user_id.id == user.id:
                    timesheet_val += timesheet['unit_amount']

            timesheet_data.append(timesheet_val)

        return {
            'employee': [user.name for user in users],
            'timesheet': timesheet_data,
        }

    @api.model
    def get_chart_project_timesheet(self, project_id):
        project_id = int(project_id)
        domain = [] if project_id == -1 else [('project_id', '=', project_id)]
        timesheets = self.env['account.analytic.line'].search(domain)

        projects = []
        timesheet_data = []
        for timesheet in timesheets:
            if timesheet.project_id not in projects:
                projects.append(timesheet.project_id)

        for project in projects:
            timesheet_val = 0
            for timesheet in timesheets:
                if timesheet.project_id.id == project.id:
                    timesheet_val += timesheet['unit_amount']

            timesheet_data.append(timesheet_val)

        return {
            'employee': [project.name for project in projects],
            'timesheet': timesheet_data,
        }

    # @api.model
    # def get_chart_employee_tasks(self, project_id):
    #     done_stage = self.env.ref('project.project_stage_2')
    #     cancelled_stage = self.env.ref('project.project_stage_3')
    #
    #     project_id = int(project_id)
    #     domain = [('stage_id', '!=', cancelled_stage.id)] if project_id == -1 else [
    #         ('stage_id', '!=', cancelled_stage.id), ('project_id', '=', project_id)]
    #     users = []
    #     resolved = []
    #     unresolved = []
    #     overdue = []
    #     tasks = self.env['project.task'].search_read(domain, ['user_id', 'stage_id', 'date_deadline'])
    #     for task in tasks:
    #         if task['user_id'] not in users:
    #             users.append(task['user_id'])
    #
    #     for user in users:
    #         resolved_val = 0
    #         unresolved_val = 0
    #         overdue_val = 0
    #         for task in tasks:
    #             user_task_id = task['user_id'][0] if task['user_id'] else False
    #             current_user = user[0] if user else False
    #             if task['stage_id'][0] == done_stage.id and user_task_id == current_user:
    #                 resolved_val += 1
    #             elif user_task_id == current_user:
    #                 unresolved_val += 1
    #
    #             if task['date_deadline']:
    #                 date_deadline = datetime.strptime(task['date_deadline'], '%Y-%m-%d')
    #                 date_now = datetime.now()
    #                 date_now = date_now.date()
    #                 if date_deadline.date() < date_now and user_task_id == current_user:
    #                     overdue_val += 1
    #         resolved.append(resolved_val)
    #         unresolved.append(unresolved_val)
    #         overdue.append(overdue_val)
    #
    #     return {
    #         'employee': [user[1] if user else 'Undefined' for user in users],
    #         'resolved': resolved,
    #         'unresolved': unresolved,
    #         'overdue': overdue
    #     }

    @api.model
    def get_chart_employee_tasks(self, project_id):
        cus_send_success = []
        cus_save_success = []
        cus_dec_success = []
        cus_dec_abnor = []

        # 发送申报
        cus_send_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '=', False), ('cus_dec_sent_way', 'in', ('single', 'QP'))])
        sync_send_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '!=', False), ('cus_dec_sent_way', 'in', ('single', 'QP'))])
        cus_send_success.append(int(cus_send_count))
        cus_send_success.append(int(sync_send_count))

        # 暂存成功
        cus_save_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '=', False), ('cus_dec_rec_state', '=', '上载成功'), ('cus_dec_sent_way', '=', True)])
        sync_save_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '!=', False), ('cus_dec_rec_state', '=', '上载成功'), ('cus_dec_sent_way', '=', True)])
        cus_save_success.append(int(cus_save_count))
        cus_save_success.append(int(sync_save_count))

        # 报关单申报成功数
        cus_projects = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '=', False), ('cus_dec_rec_state', '=', '申报成功'), ('cus_dec_sent_way', '=', True)])
        # 协同报关单申报成功数
        sync_projects = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '!=', False),('cus_dec_rec_state', '=', '申报成功'), ('cus_dec_sent_way', '=', True)])
        cus_dec_success.append(int(cus_projects))
        cus_dec_success.append(int(sync_projects))

        # 申报异常
        cus_abnor_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '=', False), ('cus_dec_rec_state', 'in', ('上载失败', '导入失败','不被受理','退回修改','申报失败'))
             , ('cus_dec_sent_way', '=', True)])
        sync_abnor_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '!=', False), ('cus_dec_rec_state', 'in', ('上载失败', '导入失败','不被受理','退回修改','申报失败'))
             , ('cus_dec_sent_way', '=', True)])
        cus_dec_abnor.append(int(cus_abnor_count))
        cus_dec_abnor.append(int(sync_abnor_count))


        # done_stage = self.env.ref('project.project_stage_2')
        # cancelled_stage = self.env.ref('project.project_stage_3')
        #
        # project_id = int(project_id)
        # domain = [('stage_id', '!=', cancelled_stage.id)] if project_id == -1 else [
        #     ('stage_id', '!=', cancelled_stage.id), ('project_id', '=', project_id)]
        # users = []
        # resolved = []
        # unresolved = []
        # overdue = []
        # tasks = self.env['project.task'].search_read(domain, ['user_id', 'stage_id', 'date_deadline'])
        # for task in tasks:
        #     if task['user_id'] not in users:
        #         users.append(task['user_id'])
        #
        # for user in users:
        #     resolved_val = 0
        #     unresolved_val = 0
        #     overdue_val = 0
        #     for task in tasks:
        #         user_task_id = task['user_id'][0] if task['user_id'] else False
        #         current_user = user[0] if user else False
        #         if task['stage_id'][0] == done_stage.id and user_task_id == current_user:
        #             resolved_val += 1
        #         elif user_task_id == current_user:
        #             unresolved_val += 1
        #
        #         if task['date_deadline']:
        #             date_deadline = datetime.strptime(task['date_deadline'], '%Y-%m-%d')
        #             date_now = datetime.now()
        #             date_now = date_now.date()
        #             if date_deadline.date() < date_now and user_task_id == current_user:
        #                 overdue_val += 1
        #     resolved.append(resolved_val)
        #     unresolved.append(unresolved_val)
        #     overdue.append(overdue_val)

        return {
            'employee': '',
            'resolved': cus_send_success,
            'overdue':  cus_save_success,
            'unresolved': cus_dec_success,
            'decabnor': cus_dec_abnor
        }

    @api.model
    def get_chart_project_tasks(self, project_id):
        cus_send_success = []
        cus_save_success = []
        cus_dec_success = []
        cus_dec_abnor = []

        # 发送申报
        cus_send_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '=', False), ('cus_dec_sent_way', 'in', ('single', 'QP'))])
        sync_send_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '!=', False), ('cus_dec_sent_way', 'in', ('single', 'QP'))])
        cus_send_success.append(int(cus_send_count))
        cus_send_success.append(int(sync_send_count))

        # 暂存成功
        cus_save_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '=', False), ('cus_dec_rec_state', '=', '上载成功'), ('cus_dec_sent_way', '=', True)])
        sync_save_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '!=', False), ('cus_dec_rec_state', '=', '上载成功'), ('cus_dec_sent_way', '=', True)])
        cus_save_success.append(int(cus_save_count))
        cus_save_success.append(int(sync_save_count))

        # 报关单申报成功数
        cus_projects = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '=', False), ('cus_dec_rec_state', '=', '申报成功'), ('cus_dec_sent_way', '=', True)])
        # 协同报关单申报成功数
        sync_projects = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '!=', False), ('cus_dec_rec_state', '=', '申报成功'), ('cus_dec_sent_way', '=', True)])
        cus_dec_success.append(int(cus_projects))
        cus_dec_success.append(int(sync_projects))

        # 申报异常
        cus_abnor_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '=', False), ('cus_dec_rec_state', 'in', ('上载失败', '导入失败', '不被受理', '退回修改', '申报失败'))
             , ('cus_dec_sent_way', '=', True)])
        sync_abnor_count = self.env['cus_center.customs_dec'].search_count(
            [('synergism_seq_no', '!=', False), ('cus_dec_rec_state', 'in', ('上载失败', '导入失败', '不被受理', '退回修改', '申报失败'))
             , ('cus_dec_sent_way', '=', True)])
        cus_dec_abnor.append(int(cus_abnor_count))
        cus_dec_abnor.append(int(sync_abnor_count))

        return {
            'employee': '',
            'resolved': cus_send_success,
            'overdue': cus_save_success,
            'unresolved': cus_dec_success,
            'decabnor': cus_dec_abnor
        }

    @api.model
    def get_chart_employee_tasks_2(self, project_id,cus_or_sync):
        """ 进出口类型 饼状图 """
        cus_or_sync = cus_or_sync

        if cus_or_sync == '报关单':
            # 报关单 进口数量
            cus_send_import = self.env['cus_center.customs_dec'].search_count(
                [('synergism_seq_no', '=', False), ('inout', '=', 'I'), ('cus_dec_sent_way', '=', True)])
            # 报关单 出口数量
            cus_send_export = self.env['cus_center.customs_dec'].search_count(
                [('synergism_seq_no', '=', False), ('inout', '=', 'E'), ('cus_dec_sent_way', '=', True)])

            # sum_count = cus_send_import+cus_send_export
            # cus_send_import_rate = cus_send_import / sum_count
            # cus_send_export_rate = cus_send_export / sum_count

            return {
                'employee': '',
                'import_count': cus_send_import,
                'export_count': cus_send_export,
            }
        elif cus_or_sync == '协同报关单':
            # 协同单 进口数量
            sync_send_import = self.env['cus_center.customs_dec'].search_count(
                [('synergism_seq_no', '!=', False), ('inout', '=', 'I'), ('cus_dec_sent_way', '=', True)])
            # 协同单 出口数量
            sync_send_export = self.env['cus_center.customs_dec'].search_count(
                [('synergism_seq_no', '!=', False), ('inout', '=', 'E'), ('cus_dec_sent_way', '=', True)])

            return {
                'employee': '',
                'import_count': sync_send_import,
                'export_count': sync_send_export,
            }

    @api.model
    def get_chart_employee_tasks_3(self, project_id, cus_or_sync):
        """ 通关率 饼状图 """
        cus_or_sync = cus_or_sync

        if cus_or_sync == '报关单':
            # 报关单 异常数量
            cus_abnor_count = self.env['cus_center.customs_dec'].search_count(
                [('synergism_seq_no', '=', False), ('cus_dec_rec_state', 'in', ('上载失败', '导入失败', '不被受理', '退回修改', '申报失败'))
                 , ('cus_dec_sent_way', '=', True)])
            cus_dec_abnor = int(cus_abnor_count)

            # 报关单 申报成功数量
            cus_projects = self.env['cus_center.customs_dec'].search_count(
                [('synergism_seq_no', '=', False), ('cus_dec_rec_state', '=', '申报成功'), ('cus_dec_sent_way', '=', True)])
            cus_dec_success = int(cus_projects)

            return {
                'employee': '',
                'dec_abnor_count': cus_dec_abnor,
                'dec_success_count': cus_dec_success,
            }
        elif cus_or_sync == '协同报关单':
            # 协同单 异常数量
            sync_abnor_count = self.env['cus_center.customs_dec'].search_count(
                [('synergism_seq_no', '!=', False),
                 ('cus_dec_rec_state', 'in', ('上载失败', '导入失败', '不被受理', '退回修改', '申报失败'))
                 , ('cus_dec_sent_way', '=', True)])
            sync_dec_abnor = int(sync_abnor_count)
            # 协同报关单申报成功数
            sync_projects = self.env['cus_center.customs_dec'].search_count(
                [('synergism_seq_no', '!=', False), ('cus_dec_rec_state', '=', '申报成功'), ('cus_dec_sent_way', '=', True)])
            sync_dec_success = int(sync_projects)

            return {
                'employee': '',
                'dec_abnor_count': sync_dec_abnor,
                'dec_success_count': sync_dec_success,
            }

    # @api.model
    # def get_chart_project_tasks(self, project_id):
    #     done_stage = self.env.ref('project.project_stage_2')
    #     cancelled_stage = self.env.ref('project.project_stage_3')
    #
    #     project_id = int(project_id)
    #     domain = [('stage_id', '!=', cancelled_stage.id)] if project_id == -1 else [
    #         ('stage_id', '!=', cancelled_stage.id), ('project_id', '=', project_id)]
    #
    #     projects = []
    #     resolved = []
    #     unresolved = []
    #     overdue = []
    #     tasks = self.env['project.task'].search_read(domain, ['date_deadline', 'stage_id', 'project_id'])
    #     for task in tasks:
    #         if task['project_id'] not in projects:
    #             projects.append(task['project_id'])
    #
    #     for project in projects:
    #         resolved_val = 0
    #         unresolved_val = 0
    #         overdue_val = 0
    #         for task in tasks:
    #             project_task_id = task['project_id'][0] if task['project_id'] else False
    #             current_project = project[0] if project else False
    #             if task['stage_id'][0] == done_stage.id and project_task_id == current_project:
    #                 resolved_val += 1
    #             elif project_task_id == current_project:
    #                 unresolved_val += 1
    #             if task['date_deadline']:
    #                 date_deadline = datetime.strptime(task['date_deadline'], '%Y-%m-%d')
    #                 date_now = datetime.now()
    #                 date_now = date_now.date()
    #                 if date_deadline.date() < date_now and project_task_id == current_project:
    #                     overdue_val += 1
    #         resolved.append(resolved_val)
    #         unresolved.append(unresolved_val)
    #         overdue.append(overdue_val)
    #
    #     return {
    #         'employee': [project[1] if project else 'Undefined' for project in projects],
    #         'resolved': resolved,
    #         'unresolved': unresolved,
    #         'overdue': overdue
    #     }

