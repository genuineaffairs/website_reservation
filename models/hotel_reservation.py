from openerp import models, fields

class HotelReservation(models.Model):
	_inherit = 'hotel.reservation'

	# Add field for message from crm.lead-reservation
	crm_message = fields.Text('Reservation message')
