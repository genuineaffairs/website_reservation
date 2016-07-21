from openerp import models, fields

class HotelReservation(models.Model):
	_inherit = 'hotel.reservation'

	# Add field for message from crm.lead-reservation
	crm_message = fields.Text('Reservation message')
	# Override checkin and checkout field to change them
	# to date-fields instead of datetime
	checkin = fields.Date('Expected-Date-Arrival', required=True,
							readonly=True, states={'draft': [('readonly',False)]})
	checkout = fields.Date('Expected-Date-Departure', required=True,
							readonly=True, states={'draft': [('readonly',False)]})