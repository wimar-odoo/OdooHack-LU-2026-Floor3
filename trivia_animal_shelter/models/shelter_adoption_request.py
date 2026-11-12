
from odoo import api, fields, models
from odoo.exceptions import UserError


class ShelterAdoptionRequest(models.Model):
    _name = "shelter.adoption.request"
    _description = "Adoption Request"
    _order = "create_date desc, id desc"

    animal_id = fields.Many2one("shelter.animal", string="Animal", required=True, ondelete="cascade", index=True)
    name = fields.Char(string="Applicant", required=True)
    email = fields.Char(required=True)
    phone = fields.Char()
    message = fields.Text()
    state = fields.Selection(
        [("new", "New"), ("accepted", "Accepted"), ("refused", "Refused")],
        string="Status", required=True, default="new",
    )

    def action_accept(self):
        self.state = "accepted"
        self.animal_id.adopted = True

    def action_refuse(self):
        self.state = "refused"

    # ----------------------------------------------------------------------------
    # TODO 4 - The adoption request sent from the website
    # ----------------------------------------------------------------------------

    @api.model
    def _create_from_website(self, animal, values):
        """Create an adoption request from the website."""

        if not animal or not animal.exists():
            raise UserError("Animal not found.")

        adoptable_animals = self.env["shelter.animal"]._get_adoptable_animals()

        if animal not in adoptable_animals:
            raise UserError("This animal is not available for adoption.")

        allowed_fields = ["name", "email", "phone", "message"]

        request_values = {
            field: values.get(field)
            for field in allowed_fields
        }

        request_values["animal_id"] = animal.id

        return self.sudo().create(request_values)
