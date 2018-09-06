# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

COUNTRY_GENERATORS = []


class HrHolidaysPublicGenerator(models.TransientModel):
    _name = 'hr.holidays.public.generator'

    year = fields.Integer('Year', required=True, default=(lambda self: datetime.today().year))
    country_id = fields.Many2one('res.country', string='Country', required=True, domain=[('code', 'in', COUNTRY_GENERATORS)])
    state_id = fields.Many2one('res.country.state', string='State')
    template_id = fields.Many2one('hr.holidays.public', string='From Template')

    @api.multi
    def generate_function_copy_name(self):
        function_name = 'action_copy_%s_holidays' % self.country_id.code.lower()
        return function_name

    @api.multi
    def generate_function_generate_name(self):
        function_name = 'action_generate_%s_holidays' % self.country_id.code.lower()
        return function_name

    @api.multi
    def action_run(self):
        self.ensure_one()
        if self.template_id:
            function_name = self.generate_function_copy_name()
            if not function_name:
                raise UserError(_(
                    """There is no copy function defined for this county or
                    the function name does not fit the requirement - action_copy_%s_holidays
                    where %s id the county code."""
                 ))
            getattr(self, function_name)()
        else:
            function_name = self.generate_function_generate_name()
            if not function_name:
                raise UserError(_(
                    """There is no copy function defined for this county or
                    the function name does not fit the requirement - action_generate_%s_holidays
                    where %s is the county code."""
                 ))
            getattr(self, function_name)()
