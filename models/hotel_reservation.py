from openerp import models, fields

class HotelReservation(models.Model):
	_inherit = 'hotel.reservation'

	# Add field for context from crm.lead-reservation
	crm_message = fields.Text('Message')
	requested_room = fields.Char('Requested room')
	# Override checkin and checkout field to change them
	# to date-fields instead of datetime
	checkin = fields.Date('Expected-Date-Arrival', required=True,
							readonly=True, states={'draft': [('readonly',False)]})
	checkout = fields.Date('Expected-Date-Departure', required=True,
							readonly=True, states={'draft': [('readonly',False)]})