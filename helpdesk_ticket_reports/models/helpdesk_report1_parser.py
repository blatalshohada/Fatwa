# -*- coding: utf-8 -*-
import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HelpdeskReport1(models.AbstractModel):
    _name = 'report.helpdesk_ticket_reports.print_report_pdf_helpdesk1'

    def _get_helpdesk_report(self,  date_from, date_to, question_type_id,question_status_id,user_id,priority):
        data = []

        # if required fields entried only
        if date_from and date_to and question_type_id and not question_status_id and not user_id and not  priority:
            checks = self.env['helpdesk.ticket'].search([('date', '>=', date_from), ('date', '<=', date_to) ,('ticket_type_id', '=', question_type_id[0]) ])
            for rec in checks:
                    values = {'subject': rec.name,
                              'date': rec.date,
                              'question_status_id': rec.question_status_id.name,
                              'question_type_id': rec.ticket_type_id.name,
                              'user_id': rec.user_id.name,
                              'priority': rec.priority_value,
                              }

                    data.append(values)

        #         if required entried and qustion type only
        if date_from and date_to and question_type_id and  question_status_id and not user_id and not  priority :
            checks = self.env['helpdesk.ticket'].search([('date', '>=', date_from), ('date', '<=', date_to) ,('ticket_type_id', '=', question_type_id[0]),('question_status_id', '=', question_status_id[0]) ])
            for rec in checks:
                    values = {'subject': rec.name,
                              'date': rec.date,
                              'question_status_id': rec.question_status_id.name,
                              'question_type_id': rec.ticket_type_id.name,
                              'user_id': rec.user_id.name,
                              'priority': rec.priority_value,
                              }

                    data.append(values)

        if date_from and date_to and question_type_id and question_status_id and  user_id and not priority:
            checks = self.env['helpdesk.ticket'].search( [('date', '>=', date_from), ('date', '<=', date_to),('ticket_type_id', '=', question_type_id[0]),('user_id', '=', user_id[0]),
                 ('question_status_id', '=', question_status_id[0])])
            for rec in checks:
                values = {'subject': rec.name,
                          'date': rec.date,
                          'question_status_id': rec.question_status_id.name,
                          'question_type_id': rec.ticket_type_id.name,
                          'user_id': rec.user_id.name,
                          'priority': rec.priority_value,
                          }

                data.append(values)

        if date_from and date_to and question_type_id and question_status_id and not user_id and  priority:
            checks = self.env['helpdesk.ticket'].search( [('date', '>=', date_from), ('date', '<=', date_to),('ticket_type_id', '=', question_type_id[0]),('priority', '=', priority),
                 ('question_status_id', '=', question_status_id[0])])
            for rec in checks:
                values = {'subject': rec.name,
                          'date': rec.date,
                          'question_status_id': rec.question_status_id.name,
                          'question_type_id': rec.ticket_type_id.name,
                          'user_id': rec.user_id.name,
                          'priority': rec.priority_value,
                          }

                data.append(values)


        if date_from and date_to and question_type_id and not question_status_id and  user_id and  priority:
            checks = self.env['helpdesk.ticket'].search( [('date', '>=', date_from), ('date', '<=', date_to),('ticket_type_id', '=', question_type_id[0]),('user_id', '=', user_id[0]),('priority', '=', priority),
            ])
            for rec in checks:
                values = {'subject': rec.name,
                          'date': rec.date,
                          'question_status_id': rec.question_status_id.name,
                          'question_type_id': rec.ticket_type_id.name,
                          'user_id': rec.user_id.name,
                          'priority': rec.priority_value,
                          }

                data.append(values)

        if date_from and date_to and question_type_id and not question_status_id and user_id and not priority:
            checks = self.env['helpdesk.ticket'].search(
                [('date', '>=', date_from), ('date', '<=', date_to), ('ticket_type_id', '=', question_type_id[0]),
                 ('user_id', '=', user_id[0]),
                 ])
            for rec in checks:
                values = {'subject': rec.name,
                          'date': rec.date,
                          'question_status_id': rec.question_status_id.name,
                          'question_type_id': rec.ticket_type_id.name,
                          'user_id': rec.user_id.name,
                          'priority': rec.priority_value,
                          }

                data.append(values)

        if date_from and date_to and question_type_id and not question_status_id and not user_id and  priority:
            checks = self.env['helpdesk.ticket'].search(
                [('date', '>=', date_from), ('date', '<=', date_to), ('ticket_type_id', '=', question_type_id[0]),
                 ('priority', '=', priority),
                 ])
            for rec in checks:
                values = {'subject': rec.name,
                          'date': rec.date,
                          'question_status_id': rec.question_status_id.name,
                          'question_type_id': rec.ticket_type_id.name,
                          'user_id': rec.user_id.name,
                          'priority': rec.priority_value,

                          }

                data.append(values)



        if date_from and date_to and question_type_id and question_status_id and  user_id and  priority:
            checks = self.env['helpdesk.ticket'].search( [('date', '>=', date_from), ('date', '<=', date_to),('ticket_type_id', '=', question_type_id[0]),('user_id', '=', user_id[0]),('priority', '=', priority),
                 ('question_status_id', '=', question_status_id[0])])
            for rec in checks:
                values = {'subject': rec.name,
                          'date': rec.date,
                          'question_status_id': rec.question_status_id.name,
                          'question_type_id': rec.ticket_type_id.name,
                          'user_id': rec.user_id.name,
                          'priority': rec.priority_value,
                          }

                data.append(values)



        return data

    def _get_question_status_id(self, data):
        question_status_id = ' '
        if data['question_status_id']:
            question_status_id = self.env['question.status'].browse(data['question_status_id'][0]).name
        return question_status_id



    # def _get_sender_id(self, data):
    #     sender_id = ' '
    #     if data['sender_id']:
    #         sender_id = self.env['sender.type'].browse(data['sender_id'][0]).sender
    #     return sender_id

    def _get_priority_id(self,data):
        # priority= dict(self._fields['priority'].selection).get(data['priority'])
        priority=self.env['helpdesk.ticket'].search([('priority','=',data['priority'])],limit=1)

        return priority.priority_value

    def _get_assign_to_id(self, data):
        user_id = ' '
        if data['user_id']:
            user_id = self.env['res.users'].browse(data['user_id'][0]).name
        return user_id


    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))

        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'date_from': data['form']['date_from'],
            'date_to': data['form']['date_to'],
            'question_type_id': data['form']['question_type_id'],
            # '_get_priority_id': data['form']['priority'],
            '_get_question_status_id': self._get_question_status_id(data['form']),
            '_get_assign_to_id': self._get_assign_to_id(data['form']),
            '_get_priority_id': self._get_priority_id(data['form']),

            '_get_helpdesk_report': self._get_helpdesk_report( data['form']['date_from'], data['form']['date_to'],data['form']['question_type_id'],
                                                               data['form']['question_status_id'],data['form']['user_id'],
                                                               data['form']['priority'] ),

        }
