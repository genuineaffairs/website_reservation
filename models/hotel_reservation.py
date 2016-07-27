from openerp import models, fields
#Imports for date_order field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import time

class HotelReservation(models.Model):
	_inherit = 'hotel.reservation'

	# Add field for context from crm.lead-reservation
	crm_message = fields.Text('Message')
	requested_room = fields.Char('Requested room')
	# Override date_order to make it a date-field instead of datetime
	date_order = fields.Date('Date Ordered',required=True,readonly=True,
							states={'draft':[('readonly',False)]}, 
							default=(lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
							
class RoomReservationSummary(models.Model):
	_inherit = 'room.reservation.summary'
	date_from = fields.Date('Date From')
	date_to = fields.Date('Date To')