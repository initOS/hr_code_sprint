# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, exceptions, _

_logger = logging.getLogger(__name__)


class ElegoHolidays(models.Model):

    _inherit = 'hr.holidays'

    approvers = fields.Char(compute='_get_approvers', readonly=True)

    def _get_approvers(self):
        group_h_manager = self.env.ref('hr_holidays.group_hr_holidays_manager')
        approver_ids = []
        for recipient in group_h_manager.users:
            approver_ids.append(str(recipient.partner_id.id))
        for holiday in self:
            self.approvers = ','.join(approver_ids)

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

    @api.model
    def create(self, values):
        holiday = super(ElegoHolidays, self.with_context(mail_create_nolog=True, mail_create_nosubscribe=True)).create(values)
        self.notify_approvers(holiday.id)
        return holiday

    @api.multi
    def write(self, values):
        result = super(ElegoHolidays, self).write(values)
        for holiday in self:
            if holiday.state == "confirm" and 'message_follower_ids' not in values:
                self.notify_approvers(holiday.id)
        return result

    @api.model
    def notify_approvers(self, holiday_id):
        serverAction = self.env.ref('hr_holidays_public_germany.action_email_new_leave_notif')
        ctx = {'active_model': self._name, 'active_id': holiday_id}
        serverAction.with_context(ctx).run()
        return True
