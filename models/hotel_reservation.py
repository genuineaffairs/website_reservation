from openerp import models, fields, api
#Imports for date_order field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import time

class HotelReservation(models.Model):
	_inherit = 'hotel.reservation'

	# Add field for context from crm.lead-reservation
	crm_message = fields.Text('Message')
	requested_room = fields.Char('Requested room')
	lead_id = fields.Integer('Lead ID')
	# Override date_order to make it a date-field instead of datetime
	date_order = fields.Date('Date Ordered',required=True,readonly=True,
							states={'draft':[('readonly',False)]}, 
							default=(lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
	
	# Change state of lead if reservation was generated from a lead
	# Function is called from hotel.reservation workflow activity
	@api.multi
	def change_lead_state(self):
		if(self.lead_id):
			won_id = self.env['crm.case.stage'].search([('name','=','Won')]).id
			lead = self.env['crm.lead'].search([('id','=',self.lead_id)])
			lead.stage_id = won_id
							