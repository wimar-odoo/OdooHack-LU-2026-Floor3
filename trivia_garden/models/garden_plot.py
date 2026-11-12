from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GardenPlot(models.Model):
    _name = "garden.plot"
    _description = "Garden Plot"

    name = fields.Char(string="Plot", required=True)
    site_id = fields.Many2one("garden.site", string="Site", required=True)
    area = fields.Float(string="Area (m²)")
    tenant_id = fields.Many2one("res.partner", string="Tenant")

    _unique_plot_tenant = models.Constraint(
        "UNIQUE(tenant_id)",
        "A member can rent at most one plot.",
    )

    @api.constrains("tenant_id")
    def _check_tenant_paid_current_year(self):
        current_year = fields.Date.today().year
        for plot in self:
            if plot.tenant_id and plot.tenant_id.last_paid_year != current_year:
                raise ValidationError(
                    "Only a member who paid the membership fee for the current year can rent a plot."
                )