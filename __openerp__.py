{
	'name': 'Website Reservation Form',
	'description': 'Extends website_crm Contact Form and transforms it to a hotel reservation form. Every new reservation-request is created as a lead in crm-module.',
	'author' : 'Oscar Hall',
	'depends' : ['website_crm','hotel_reservation'],
	'data' : ['views/website_reservation.xml', 
				'views/crm_lead_view.xml', 
				'views/hotel_reservation_view.xml',
				'views/hotel_reservation_workflow.xml',
				'security/ir.model.access.csv'],
}
