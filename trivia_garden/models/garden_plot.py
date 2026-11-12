from odoo import _,fields, models, api
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
    @api.constrains("tenant_id")
    def _check_tenant(self):
        this_year = fields.Date.context_today(self).year
        for plot in self:
            tenant = plot.tenant_id
            if not tenant:
                continue
            if tenant.last_paid_year != this_year:
                raise ValidationError(_("%s has not paid this year's fee and cannot rent a plot.", tenant.name))
            if self.env["garden.plot"].search_count([("tenant_id", "=", tenant.id), ("id", "!=", plot.id)]):
                raise ValidationError(_("%s already rents a plot.", tenant.name))
