from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner" 

    # ----------------------------------------------------------------------------
    # TODO 4 - The members
    #
    # Add the fields of the members to the contacts:
    #   * membership_type   Selection individual / family / patron      "Membership Type"
    #   * member_since      Date                                         "Member Since"
    #   * fee_ids           One2many to garden.membership.fee            "Membership Fees"
    #   * last_paid_year    Integer, computed and STORED                 "Last Paid Year"
    #                       the most recent year of a PAID fee, 0 if none
    #
    # last_paid_year must always be up to date: when a fee is paid, when its year
    # changes, when a fee is added or deleted.
    # ----------------------------------------------------------------------------
    membership_type = fields.Selection(
        [("individual", "Individual"), ("family", "Family"), ("patron", "Patron")],
        string="Membership Type")
    member_since = fields.Date()
    fee_ids = fields.One2many("garden.membership.fee", "partner_id", string="Membership Fees")
    last_paid_year = fields.Integer(compute="_compute_last_paid_year", store=True)
    fee_count = fields.Integer(compute="_compute_fee_count")

    @api.depends("fee_ids.state", "fee_ids.year")
    def _compute_last_paid_year(self):
        for partner in self:
            paid = partner.fee_ids.filtered(lambda f: f.state == "paid")
            partner.last_paid_year = max(paid.mapped("year"), default=0)

    @api.depends("fee_ids")
    def _compute_fee_count(self):
        for partner in self:
            partner.fee_count = len(partner.fee_ids)

    def action_view_fees(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Membership Fees",
            "res_model": "garden.membership.fee",
            "view_mode": "list,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }
