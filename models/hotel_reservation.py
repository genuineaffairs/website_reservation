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
		# Set checkin/out times greater than 00:00:00 UTC to display the correct dates with timezone
		# Checkin time needs to be greater than checkout time so one night is less then 24hours to create folio correctly
		temp_checkin = fields.Datetime.from_string(vals['checkin'])
		temp_checkout = fields.Datetime.from_string(vals['checkout'])
		temp_checkin = temp_checkin.replace(temp_checkin.year,temp_checkin.month,temp_checkin.day,17,00,00)
		temp_checkout = temp_checkout.replace(temp_checkout.year,temp_checkout.month,temp_checkout.day,15,00,00)
		vals['checkin'] = temp_checkin
		vals['checkout'] = temp_checkout

		return super(HotelReservation, self).create(vals)
		
	# Change state of lead if reservation was generated from a lead
	# Function is called from hotel.reservation workflow activity
	@api.multi
	def change_lead_state(self):
		if(self.lead_id):
			won_id = self.env['crm.case.stage'].search([('name','=','Won')]).id
			lead = self.env['crm.lead'].search([('id','=',self.lead_id)])
			lead.stage_id = won_id
					"""		
class RoomReservaionSummary(models.Model):
	_inherit = 'room.reservation.summary'
	
	# Override get_room_summary to make the reservation-summary work properly with dates not in UTC
	@api.onchange('date_from', 'date_to')
	def get_room_summary(self):
		'''
		@param self: object pointer
		 '''
		res = {}
		all_detail = []
		room_obj = self.env['hotel.room']
		reservation_line_obj = self.env['hotel.room.reservation.line']
		folio_room_line_obj = self.env['folio.room.line']
		date_range_list = []
		main_header = []
		summary_header_list = ['Rooms']
		if self.date_from and self.date_to:
			if self.date_from > self.date_to:
				raise except_orm(_('User Error!'),
								 _('Please Check Time period Date \
								 From can\'t be greater than Date To !'))
			# Add a time at the end of the day to make reservation-summary functionality work
			# properly with timezone and show the correct dates as reserved/free
			temp_from = fields.Datetime.from_string(self.date_from)
			d_frm_obj = temp_from.replace(temp_from.year,temp_from.month,temp_from.day,23,00,00)
			temp_to = fields.Datetime.from_string(self.date_to)
			d_to_obj = temp_to.replace(temp_to.year,temp_to.month,temp_to.day,23,00,00)
			
			temp_date = d_frm_obj
			while(temp_date <= d_to_obj):
				val = ''
				val = (str(temp_date.strftime("%a")) + ' ' +
					   str(temp_date.strftime("%b")) + ' ' +
					   str(temp_date.strftime("%d")))
				summary_header_list.append(val)
				date_range_list.append(temp_date.strftime
									   (DEFAULT_SERVER_DATETIME_FORMAT))
				temp_date = temp_date + datetime.timedelta(days=1)
			all_detail.append(summary_header_list)
			room_ids = room_obj.search([])
			all_room_detail = []
			for room in room_ids:
				room_detail = {}
				room_list_stats = []
				room_detail.update({'name': room.name or ''})
				if not room.room_reservation_line_ids and \
				   not room.room_line_ids:
					for chk_date in date_range_list:
						room_list_stats.append({'state': 'Free',
												'date': chk_date})
				else:
					for chk_date in date_range_list:
						reserline_ids = room.room_reservation_line_ids.ids
						reservline_ids = (reservation_line_obj.search
										  ([('id', 'in', reserline_ids),
											('check_in', '<=', chk_date),
											('check_out', '>=', chk_date),
											('status', '!=', 'cancel')
											]))
						fol_room_line_ids = room.room_line_ids.ids
						chk_state = ['draft', 'cancel']
						folio_resrv_ids = (folio_room_line_obj.search
										   ([('id', 'in', fol_room_line_ids),
											 ('check_in', '<=', chk_date),
											 ('check_out', '>=', chk_date),
											 ('status', 'not in', chk_state)
											 ]))
						if reservline_ids or folio_resrv_ids:
							room_list_stats.append({'state': 'Reserved',
													'date': chk_date,
													'room_id': room.id,
													'is_draft': 'No',
													'data_model': '',
													'data_id': 0})
						else:
							room_list_stats.append({'state': 'Free',
													'date': chk_date,
													'room_id': room.id})

				room_detail.update({'value': room_list_stats})
				all_room_detail.append(room_detail)
			main_header.append({'header': summary_header_list})
			self.summary_header = str(main_header)
			self.room_summary = str(all_room_detail)
		return res
		"""