from odoo import http
from odoo.http import request


class ShelterController(http.Controller):

    @http.route('/adopt', type='http', auth='public', website=True)
    def adopt_list(self, species=None, **kwargs):
        Animal = request.env['shelter.animal']
        animals = Animal._get_adoptable_animals(species=species)
        species_selection = Animal._fields['species'].selection
        return request.render('trivia_animal_shelter.animal_list', {
            'animals': animals,
            'current_species': species,
            'species_selection': species_selection,
        })

    @http.route('/adopt/<model("shelter.animal"):animal>', type='http', auth='public', website=True)
    def adopt_detail(self, animal, **kwargs):
        if not animal.is_published or animal.adopted:
            raise request.not_found()
        return request.render('trivia_animal_shelter.animal_detail', {
            'animal': animal,
            'submitted': kwargs.get('submitted'),
        })

    @http.route('/adopt/<model("shelter.animal"):animal>/request', type='http', auth='public', methods=['POST'], website=True)
    def adopt_request(self, animal, **post):
        request.env['shelter.adoption.request']._create_from_website(animal, post)
        return request.redirect(f"{animal.website_url}?submitted=1")