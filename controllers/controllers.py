from openerp import http, SUPERUSER_ID
from openerp.addons.website_crm.controllers.main import contactus


class website_reservation(contactus):
	#Edit contact method to route additional records to contactus-page
	@http.route(['/page/website.contactus', '/page/contactus'], type='http', auth="public", website=True)
	def contact(self, **kwargs):
		values = {}
		for field in ['description', 'partner_name', 'phone', 'contact_name', 'email_from', 'name']:
			if kwargs.get(field):
				values[field] = kwargs.pop(field)
		values.update(kwargs=kwargs.items())
		# Add res.country to routed values 
		Countries = http.request.env['res.country']
		values.update({'countries': Countries.search([])})
		# Add hotel.room.type to touted values
		Roomtypes = http.request.env['hotel.room.type']
		values.update({'roomtypes': Roomtypes.search([])})
			
		return http.request.website.render("website.contactus", values)

	#Edit create_lead method to add extra functionality
	def create_lead(self, request, values, kwargs):
		cr, context = request.cr, request.context
                # Convert country_id string-value from form to a record id
                country_id = request.registry['res.country'].search(cr, SUPERUSER_ID,[('name','=', values['country_id'] )])[0]
		values.update({'country_id': country_id})

	      	return request.registry['crm.lead'].create(cr, SUPERUSER_ID, values, context=dict(context, mail_create_nosubscribe=True))

