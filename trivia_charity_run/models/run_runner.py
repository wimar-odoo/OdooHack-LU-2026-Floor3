from odoo import api, fields, models
from odoo.tools import SQL

CATEGORIES = [
    ("junior", "Junior (under 20)"),
    ("senior", "Senior (20-39)"),
    ("master", "Master (40-59)"),
    ("veteran", "Veteran (60 and over)"),
]
GENDERS = [("female", "Women"), ("male", "Men")]


class RunRunner(models.Model):
    _name = "run.runner"
    _description = "Runner"
    _order = "edition_id desc, bib"

    name = fields.Char(required=True)
    bib = fields.Integer(required=True)
    edition_id = fields.Many2one("run.edition", string="Edition", required=True, ondelete="cascade", index=True)
    category = fields.Selection(CATEGORIES, required=True)
    gender = fields.Selection(GENDERS, required=True)
    distance_km = fields.Float(string="Distance (km)", help="Distance covered by the runner.")
    disqualified = fields.Boolean()
    split_ids = fields.One2many("run.split", "runner_id", string="Split Times")
    pledge_ids = fields.One2many("run.pledge", "runner_id", string="Pledges")
    amount_raised = fields.Float(
        compute="_compute_amount_raised",
        help="Amount given by the sponsors: their pledges per km × the distance covered by the runner.",
    )

    _bib_uniq = models.Constraint("UNIQUE(edition_id, bib)", "Two runners of an edition cannot have the same bib.")

    # ----------------------------------------------------------------------------
    # TODO 2 - The amount raised
    # ----------------------------------------------------------------------------

    @api.depends("pledge_ids.amount_per_km", "distance_km")
    def _compute_amount_raised(self):
        if not self.ids:
            self.amount_raised = 0.0
            return

        # Flush pending ORM changes to the database before running raw SQL
        self.flush_model(["distance_km"])
        self.env["run.pledge"].flush_model(["runner_id", "amount_per_km"])

        self.env.cr.execute(SQL(
            """
            SELECT r.id,
                   COALESCE(SUM(p.amount_per_km), 0.0) * COALESCE(r.distance_km, 0.0)
              FROM run_runner r
              LEFT JOIN run_pledge p ON p.runner_id = r.id
             WHERE r.id IN %s
             GROUP BY r.id, r.distance_km
            """,
            tuple(self.ids),
        ))
        amounts = dict(self.env.cr.fetchall())
        for runner in self:
            runner.amount_raised = amounts.get(runner.id, 0.0)

    def action_disqualify(self):
        self.disqualified = True

    def action_requalify(self):
        self.disqualified = False

    # ----------------------------------------------------------------------------
    # TODO 3 - The results kiosk
    # ----------------------------------------------------------------------------

    @api.model
    def search_by_bib_or_name(self, term):
        """ Return the runners whose bib number is ``term``, or whose name contains ``term``. """
        self.flush_model(["bib", "name"])  # raw SQL reads the database, not the cache of the ORM
        self.env.cr.execute(SQL(
            """
            SELECT id
              FROM run_runner
             WHERE bib::text = %s
                OR name ILIKE %s
          ORDER BY edition_id DESC, bib
            """,
            str(term),
            f"%{term}%",
        ))
        return self.browse([row[0] for row in self.env.cr.fetchall()])