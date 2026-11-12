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

class MembershipFee(models.Model):
	_name = "garden.membership.fee"
	_description = "Membership Fee"

	partner_id = fields.Many2one('res.partner', required=True, string="Member")
	year = fields.Integer(required=True, string="Year")
	amount = fields.Float(string="Amount")
	state = fields.Selection([('draft', 'Draft'), ('paid', 'Paid')], required=True, default=lambda self: 'draft', string="Status")
	payment_date = fields.Date(string="Payment Date")

	_unique_fee_per_year = models.Constraint(
		'UNIQUE(partner_id, year)',
    'A member can only have one membership fee per year!')

	def action_mark_paid(self):
		for record in self:
			record.state = 'paid'
			record.payment_date = fields.Date.context_today(self)