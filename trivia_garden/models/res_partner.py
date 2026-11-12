from odoo import api, models, fields


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
        [('individual', 'Individual'),
        ('family', 'Family'),
        ('patron', 'Patron')],
        string='Membership Type',
    )
    member_since = fields.Date(string='Member Since')
    fee_ids = fields.One2many(
        'garden.membership.fee', 'partner_id',
        string='Membership Fees'
    )
    last_paid_year = fields.Integer(
        string='Last Paid Year',
        compute='_compute_last_paid_year',
        store=True
    )

    @api.depends('fee_ids.year', 'fee_ids.state')
    def _compute_last_paid_year(self):
        for record in self:
            paid_fees = record.fee_ids.filtered(lambda f: f.state == 'paid')
            record.last_paid_year = max(paid_fees.mapped('year')) if paid_fees else 0