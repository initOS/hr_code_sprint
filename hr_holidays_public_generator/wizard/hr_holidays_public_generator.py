# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class HrHolidaysPublicGenerator(models.TransientModel):
    _name = 'hr.holidays.public.generator'

    year = fields.Integer('Year', required=True, default=(lambda self: datetime.today().year))
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', string='State')
    template_id = fields.Many2one('public.holidays.public', string='From Template')

    @api.multi
    def action_run(self):
        return
