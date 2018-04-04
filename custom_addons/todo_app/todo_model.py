# –*– coding: utf–8 –*–
from odoo import models, fields,api

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'TO-DO Task'
    name = fields.Char('Description', required=True)
    is_done = fields.Boolean('Done')
    active = fields.Boolean('Active', default=True)

    drag_image_ids = fields.Many2many('ir.attachment')

    @api.multi
    def do_toggle_done(self):
        for task in self:
            task.is_done = not task.is_done
        return True

    @api.multi
    def print_todo_task(self):
        self.print_todo_task1()
        self.print_todo_task2()
        self.print_todo_task3()
        self.print_todo_task4()
        # result1=self.env['report'].get_pdf([self.id],"todo_app.report_todo_task_template"), 'pdf'
        # result2 =self.env['report'].get_pdf([self.id], "todo_app.report_todo_task_template2"), 'pdf'
        # result3=self.env['report'].get_pdf([self.id], "todo_app.report_todo_task_template3"), 'pdf'
        # result4 =self.env['report'].get_pdf([self.id], "todo_app.report_todo_task_template4"), 'pdf'

        # print('print_result1',result1)
        # print('print_result2', result2)
        # print('print_result3', result3)
        # print('print_result4', result4)

        att_model = self.env['ir.attachment']  # 获取附件模型
        for obj in self:
            query = [('res_model', '=', self._name), ('res_id', '=', obj.id)]  # 根据res_model和res_id查询附件
        list = att_model.search(query)  # 取得附件list

        print('print_list',len(list))
        ids=[]
        if len(list) >0:
            for i in list:
                ids.append(i.id)

        if len(list) > 0:
            for i in list:
                self.drag_image_ids =  [(6, 0, ids)]
                edoc= self.env['ir.attachment'].search([('id', '=', i.id)])
                dec_edoc_type=""

                if "箱单" in edoc.name:
                    dec_edoc_type="00000002"
                if "发票" in edoc.name:
                    dec_edoc_type="00000001"
                if "合同" in edoc.name:
                    dec_edoc_type="00000004"
                if "委托书" in edoc.name:
                    dec_edoc_type="10000001"

                self.env['ir.attachment'].search(
                    [('id', '=', i.id)]).update({'extension': 'pdf','dec_edoc_type':dec_edoc_type})

    @api.multi
    def print_todo_task1(self):
        print('print_todo_task_pdf1')
        return self.env['report'].get_pdf([self.id], "todo_app.report_todo_task_template"), 'pdf'

    @api.multi
    def print_todo_task2(self):
        print('print_todo_task_pdf2')
        return self.env['report'].get_pdf([self.id], "todo_app.report_todo_task_template2"), 'pdf'

    @api.multi
    def print_todo_task3(self):
        print('print_todo_task_pdf3')
        return self.env['report'].get_pdf([self.id], "todo_app.report_todo_task_template3"), 'pdf'

    @api.multi
    def print_todo_task4(self):
        print('print_todo_task_pdf4')
        return self.env['report'].get_pdf([self.id], "todo_app.report_todo_task_template4"), 'pdf'

