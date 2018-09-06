# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions, _

import logging
_logger = logging.getLogger(__name__)

class AddHolidays(models.TransientModel):

    _name = 'add.holidays'

    category_id = fields.Many2one(comodel_name='hr.employee.category', string='Category')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employees')
    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('category', 'By Employee Tag')
    ], string='Type', required=True, default='employee',
        help='By Employee: Holidays for individual Employee, By Employee Tag: Holidays for group of employees in category')

    @api.multi
    def action_add_holidays(self):
        self.ensure_one()
        if not self.category_id and not self.employee_id:
            raise exceptions.Warning(_('You must select at least one employee or one category of employees.'))
        holiday_status = self.env.ref('hr_holidays_public_germany.holiday_status_public_holidays')
        public_holiday_id = self.env.context.get('active_id', False)
        if not public_holiday_id:
            raise exceptions.Warning(_('No found active_id in context.'))
        public_holiday = self.env['hr.holidays.public'].browse(public_holiday_id)
        if self.holiday_type == 'employee':
            self.create_allocation_and_leaves(self.employee_id, holiday_status, public_holiday)
        else:
            for employee in self.category_id.employee_ids:
                self.create_allocation_and_leaves(employee, holiday_status, public_holiday)
        
    @api.model
    def create_allocation_and_leaves(self, employee, holiday_status, public_holiday):
        hr_holiday_obj = self.env['hr.holidays']
        hr_public_holiday_obj = self.env['hr.holidays.public']
        employee_public_holidays = hr_public_holiday_obj.get_holidays_list(public_holiday.year, employee.id)
        if len(employee_public_holidays) <= 0:
            return
        add_leave = hr_holiday_obj.create({
            'name': _('Public Holidays') + " (%d, %s)" %(public_holiday.year, public_holiday.country_id.name),
            'employee_id': employee.id,
            'holiday_status_id': holiday_status.id,
            'number_of_days_temp': len(employee_public_holidays),
            'type': 'add',
            'holiday_type': 'employee',
            'employee_id': employee.id,
            'public_holidays_id': public_holiday.id,
        })
        add_leave.action_approve()
        public_holiday.write({'allocation_id': add_leave.id})
        remove_leave_ids = []
        for line in employee_public_holidays:
            date = line.date
            datetime_from = date+" 07:00:00"
            datetime_to = date+" 19:00:00"
            remove_leave_ids.append(hr_holiday_obj.create({
                'name': line.name,
                'date_from': datetime_from,
                'date_to': datetime_to,
                'employee_id': employee.id,
                'holiday_status_id': holiday_status.id,
                'number_of_days_temp': 1,
                'type': 'remove',
                'holiday_type': 'employee',
                'employee_id': employee.id,
                'public_holidays_line_id': line.id,
            }).id)
        remove_leaves = hr_holiday_obj.browse(remove_leave_ids)
        remove_leaves.action_approve()
