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

from odoo import fields, models


class GardenMembershipFee(models.Model):
    _name = "garden.membership.fee"
    _description = "Membership Fee"
    _order = "year desc, id"

    partner_id = fields.Many2one("res.partner", string="Member", required=True, ondelete="cascade")
    year = fields.Integer(required=True)
    amount = fields.Float()
    state = fields.Selection([("draft", "Draft"), ("paid", "Paid")], required=True, default="draft")
    payment_date = fields.Date()

    _unique_fee = models.Constraint(
        "UNIQUE(partner_id, year)",
        "A member can only have one fee per year.",
    )

    def action_mark_paid(self):
        self.write({
            "state": "paid",
            "payment_date": fields.Date.today(),
        })
