from openerp import models, fields

class HotelReservation(models.Model):
	_inherit = 'hotel.reservation'

	# Add field for context from crm.lead-reservation
	crm_message = fields.Text('Message')
	requested_room = fields.Char('Requested room')