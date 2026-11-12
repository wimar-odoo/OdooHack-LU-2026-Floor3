
from odoo import http
from odoo.http import request  # noqa: F401


class ShelterController(http.Controller):
    """ The pages of the website of the shelter.

    Keep the controllers thin: the business logic belongs to the models (TODO 1 and TODO 4).
    """

    # ----------------------------------------------------------------------------
    # TODO 2 - The page /adopt
    # ----------------------------------------------------------------------------

    @http.route(
        "/adopt",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def animal_list(self, species=None, **kwargs):
        animals = request.env["shelter.animal"].sudo()._get_adoptable_animals(
            species=species
        )

        return request.render(
            "trivia_animal_shelter.animal_list",
            {
                "animals": animals,
                "species": species,
            },
        )

    # ----------------------------------------------------------------------------
    # TODO 3 - The page of an animal
    # ----------------------------------------------------------------------------

    @http.route(
        "/adopt/<model('shelter.animal'):animal>",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def animal_detail(self, animal, **kwargs):

        if not animal.is_published or animal.adopted:
            return request.not_found()

        return request.render(
            "trivia_animal_shelter.animal_detail",
            {
                "animal": animal,
            },
        )

    # ----------------------------------------------------------------------------
    # TODO 4 - The adoption request
    # ----------------------------------------------------------------------------

    @http.route(
        "/adopt/<model('shelter.animal'):animal>/request",
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
        csrf=True,
    )
    def adoption_request(self, animal, **post):

        adoption_request = request.env[
            "shelter.adoption.request"
        ]._create_from_website(animal, post)

        return request.render(
            "trivia_animal_shelter.adoption_thanks",
            {
                "animal": animal,
                "adoption_request": adoption_request,
            },
        )
