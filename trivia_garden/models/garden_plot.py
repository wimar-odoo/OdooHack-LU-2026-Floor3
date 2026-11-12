from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GardenPlot(models.Model):
    _name = "garden.plot"
    _description = "Garden Plot"
    _order = "site_id, name"

    name = fields.Char(required=True)
    site_id = fields.Many2one("garden.site", string="Site", required=True, ondelete="cascade")
    area = fields.Float(string="Area (m²)")
    tenant_id = fields.Many2one("res.partner", string="Tenant", index=True)

    # ----------------------------------------------------------------------------
    # TODO 6 - The rules of the plots
    #
    # A plot can only be rented (tenant_id) by a member who paid the fee of the
    # current year (see last_paid_year, TODO 4), and a member rents one plot at most.
    # Refuse the other cases with a clear message.
    # ----------------------------------------------------------------------------


    _tenant_unique = models.Constraint("UNIQUE(tenant_id)", "A member can rent at most one plot.")

    @api.constrains("tenant_id")
    def _check_tenant_id(self):
        today = fields.Date.context_today(self)
        for plot in self:
            if not plot.tenant_id:
                continue
            if plot.tenant_id.last_paid_year != today.year:
                raise ValidationError(
                    "The tenant must have paid the membership fee for the current year to rent a plot."
                )