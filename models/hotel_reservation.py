from openerp import models, fields, api
#Imports for date_order field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import datetime
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
	
	@api.model
	def create(self, vals):	
		if not vals:
			vals = {}
		if self._context is None:
			self._context = {}
		vals['reservation_no'] = self.env['ir.sequence'].get('hotel.reservation')
		print vals['reservation_no']
		# Set checkin/out times greater than 00:00:00 UTC to display the correct dates with timezone
		# Checkin time needs to be greater than checkout time so one night is less then 24hours to create folio correctly
		temp_checkin = fields.Datetime.from_string(vals['checkin'])
		temp_checkout = fields.Datetime.from_string(vals['checkout'])
		temp_checkin = temp_checkin.replace(temp_checkin.year,temp_checkin.month,temp_checkin.day,17,00,00)
		temp_checkout = temp_checkout.replace(temp_checkout.year,temp_checkout.month,temp_checkout.day,15,00,00)
		vals['checkin'] = temp_checkin
		vals['checkout'] = temp_checkout
		print vals['reservation_no']
		"""return super(HotelReservation, self).create(vals)"""
		
	# Change state of lead if reservation was generated from a lead
	# Function is called from hotel.reservation workflow activity
	@api.multi
	def change_lead_state(self):
		if(self.lead_id):
			won_id = self.env['crm.case.stage'].search([('name','=','Won')]).id
			lead = self.env['crm.lead'].search([('id','=',self.lead_id)])
			lead.stage_id = won_id