# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import time
from datetime import timedelta

from odoo import _, api, exceptions, fields, models

_logger = logging.getLogger(__name__)


class HrPublicHolidays(models.Model):
    _inherit = 'hr.holidays.public'

    @api.model
    def _compute_date(self, date_from, date_to, employee=None):
        employee_id = employee and employee.id or False
        public_holidays = []
        annual_leaves = []
        weekends = []
        if not date_from or not date_to:
            return {
                'public_holidays': public_holidays,
                'annual_leaves': annual_leaves,
                'weekends': weekends
            }
        if date_from > date_to:
            raise exceptions.Warning(
                _('The start date must be anterior to the end date.')
            )
        date_first = fields.Datetime.from_string(date_from)
        date_last = fields.Datetime.from_string(date_to)
        date_next = date_first
        while date_next <= date_last:
            if self.is_public_holiday(date_next, employee_id):
                public_holidays.append(date_next)
            elif self.is_weekend(date_next):
                weekends.append(date_next)
            else:
                annual_leaves.append(date_next)
            date_next = date_next + timedelta(days=1)
        return {
            'public_holidays': public_holidays,
            'annual_leaves': annual_leaves,
            'weekends': weekends
        }

    @api.model
    def is_weekend(self, date):
        # TODO refactor to the SERVER DATETIME format
        if time.strptime(
                date.strftime("%Y-%m-%d"), '%Y-%m-%d'
        ).tm_wday in (5, 6):
            return True
        return False
