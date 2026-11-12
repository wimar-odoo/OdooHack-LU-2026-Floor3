from odoo import fields, models


class GardenMembershipFee(models.Model):
    _name = "garden.membership.fee"
    _description = "Garden Membership Fee"
    _order = "year desc, id desc"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Member",
        required=True,
        ondelete="cascade",
    )
    year = fields.Integer(
        string="Year",
        required=True,
        default=lambda self: fields.Date.today().year,
    )
    amount = fields.Float(string="Amount", default=0.0)
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("paid", "Paid"),
        ],
        string="Status",
        default="draft",
        required=True,
    )
    payment_date = fields.Date(string="Payment Date")

    _unique_member_year = models.Constraint(
        "UNIQUE(partner_id, year)",
        "A member can pay at most one fee per year.",
    )

    def action_mark_paid(self):
        self.write({
            "state": "paid",
            "payment_date": fields.Date.today(),
        })