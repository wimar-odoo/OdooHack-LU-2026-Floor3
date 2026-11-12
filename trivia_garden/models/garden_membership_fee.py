# ----------------------------------------------------------------------------
# TODO 1 - The membership fees
#
# Create the model garden.membership.fee ("Membership Fee"), with the fields:
#   * partner_id     Many2one to res.partner, required     "Member"
#   * year           Integer, required                      "Year"
#   * amount         Float (or Monetary)                    "Amount"
#   * state          Selection draft / paid, required,      "Status"
#                    "draft" by default
#   * payment_date   Date                                   "Payment Date"
#
# A member pays at most one fee per year: add a constraint.
# Add the method action_mark_paid(), which marks the fees as paid today.
# ----------------------------------------------------------------------------

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GardenMembershipFee(models.Model):
    _name = "garden.membership.fee"
    _description = "Membership Fee"

    partner_id = fields.Many2one("res.partner", string="Member", required=True)
    year = fields.Integer(string="Year", required=True)
    amount = fields.Float(string="Amount")
    state = fields.Selection(
        [("draft", "Draft"), ("paid", "Paid")],
        string="Status",
        required=True,
        default="draft",
    )
    payment_date = fields.Date(string="Payment Date")

    @api.constrains("partner_id", "year")
    def _check_one_fee_per_year(self):
       for fee in self:
           if self.search_count([
               ("partner_id", "=", fee.partner_id.id),
               ("year", "=", fee.year),
               ("id", "!=", fee.id),
           ]):
               raise ValidationError("A member can only pay one fee per year.")

    def action_mark_paid(self):
        self.write({
            "state": "paid",
            "payment_date": fields.Date.context_today(self),
        })