from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

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
        animal_sudo = animal.sudo()
        if not animal_sudo.is_published or animal_sudo.adopted:
            raise ValidationError(_("This animal cannot be adopted."))
        return self.sudo().create({
            "animal_id": animal_sudo.id,
            "name": values.get("name"),
            "email": values.get("email"),
            "phone": values.get("phone"),
            "message": values.get("message"),
        })
