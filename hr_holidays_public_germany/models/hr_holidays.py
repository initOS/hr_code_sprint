# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, exceptions, _

_logger = logging.getLogger(__name__)


class HrHolidays(models.Model):

    _inherit = 'hr.holidays'

    #(override) Model: hr.holidays, Function: _check_date()
    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        holiday_status_ph_id = self.env.ref('hr_holidays_public_germany.holiday_status_public_holidays').id
        for holiday in self:
            domain = [
                ('date_from', '<=', holiday.date_to),
                ('date_to', '>=', holiday.date_from),
                ('employee_id', '=', holiday.employee_id.id),
                ('id', '!=', holiday.id),
                ('state', 'not in', ['cancel', 'refuse']),
            ]
            if holiday.holiday_status_id.id != holiday_status_ph_id:
                domain.append(('holiday_status_id', '!=', holiday_status_ph_id))
            else:
                domain.append(('holiday_status_id', '=', holiday_status_ph_id))
            nholidays = self.search_count(domain)
            if nholidays:
                dholiday = self.search(domain)
                raise exceptions.ValidationError(_('You can not have 2 leaves that overlaps on same day! \n %s: H1 from %s to %s and H2 from %s to %s') %(holiday.employee_id.name, holiday.date_from, holiday.date_to, dholiday[0].date_from, dholiday[0].date_to))

    public_holidays_id = fields.Many2one(comodel_name='hr.holidays.public', string="Public Holidays", index=True, ondelete="cascade")
    public_holidays_line_id = fields.Many2one(comodel_name='hr.holidays.public.line', string="Public Holidays line", index=True, ondelete="cascade")

    _sql_constraints = [
        ('employee_public_holidays_uniq', 'unique(employee_id, public_holidays_id)',
         'The Employee can only have one allocation for the public holidays.'),
        ('employee_public_holidays_line_uniq', 'unique(employee_id, public_holidays_line_id)',
         'The Employee can only have one leave for the public holidays line'),
    ]

    @api.onchange('date_from', 'employee_id')
    def _onchange_date_from(self):
        super(ElegoHolidays, self)._onchange_date_from()
        self.number_of_days_temp = len(self.env['hr.holidays.public']._compute_date(self.date_from, self.date_to, self.employee_id)['annual_leaves'])


    @api.onchange('date_to', 'employee_id')
    def _onchange_date_to(self):
        super(ElegoHolidays, self)._onchange_date_to()
        self.number_of_days_temp = len(self.env['hr.holidays.public']._compute_date(self.date_from, self.date_to, self.employee_id)['annual_leaves'])

