import json

import frappe
import frappe.utils
from frappe import _
from frappe.contacts.doctype.address.address import get_company_address
from frappe.desk.notifications import clear_doctype_notifications
from frappe.model.mapper import get_mapped_doc
from frappe.model.utils import get_fetch_values
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html

from erpnext.accounts.doctype.sales_invoice.sales_invoice import (
	unlink_inter_company_doc,
	update_linked_doc,
	validate_inter_company_party,
)
from erpnext.accounts.party import get_party_account
from erpnext.controllers.selling_controller import SellingController
from erpnext.manufacturing.doctype.production_plan.production_plan import (
	get_items_for_material_requests,
)
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.get_item_details import get_default_bom
from erpnext.stock.stock_balance import get_reserved_qty, update_bin_qty

@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		set_missing_values(source, target)
		# Get the advance paid Journal Entries in Sales Invoice Advance
		if target.get("allocate_advances_automatically"):
			target.set_advances()

	def set_missing_values(source, target):
		target.flags.ignore_permissions = True
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		if source.company_address:
			target.update({"company_address": source.company_address})
		else:
			# set company address
			target.update(get_company_address(target.company))

		if target.company_address:
			target.update(get_fetch_values("Sales Invoice", "company_address", target.company_address))

		# set the redeem loyalty points if provided via shopping cart
		if source.loyalty_points and source.order_type == "Shopping Cart":
			target.redeem_loyalty_points = 1

		target.debit_to = get_party_account("Customer", source.customer, source.company)

	def update_item(source, target, source_parent):
		target.amount = flt(source.amount) - flt(source.billed_amt)
		target.base_amount = target.amount * flt(source_parent.conversion_rate)
		target.qty = (
			target.amount / flt(source.rate)
			if (source.rate and source.billed_amt)
			else source.qty - source.returned_qty
		)
        

		if source_parent.project:
			target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center")
		if target.item_code:
			item = get_item_defaults(target.item_code, source_parent.company)
			item_group = get_item_group_defaults(target.item_code, source_parent.company)
			cost_center = item.get("selling_cost_center") or item_group.get("selling_cost_center")

			if cost_center:
				target.cost_center = cost_center

	doclist = get_mapped_doc(
		"Sales Order",
		source_name,
		{
			"Sales Order": {
				"doctype": "Sales Invoice",
				"field_map": {
					"party_account_currency": "party_account_currency",
					"payment_terms_template": "payment_terms_template",
				},
				"field_no_map": ["payment_terms_template"],
				"validation": {"docstatus": ["=", 1]},
			},
			"Sales Order Item": {
				"doctype": "Sales Invoice Item",
				"field_map": {
					"name": "so_detail",
					"parent": "sales_order",
				},
				"postprocess": update_item,
				"condition": lambda doc: doc.qty
				and (doc.base_amount == 0 or abs(doc.billed_amt) < abs(doc.amount)),
			},
			"Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
			"Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
		},
		target_doc,
		postprocess,
		ignore_permissions=ignore_permissions,
	)

	automatically_fetch_payment_terms = cint(
		frappe.db.get_single_value("Accounts Settings", "automatically_fetch_payment_terms")
	)
	if automatically_fetch_payment_terms:
		doclist.set_payment_schedule()

	doclist.set_onload("ignore_price_list", True)

	source_doc = frappe.get_doc("Sales Order", source_name)
	
	receiver_details =frappe.get_list('Customer', 
		    filters={'customer_name': source_doc.customer},
		    fields=['receiver_id', 'receiver_type', 'receiver_name','governate',
	        'country_codes','region_city','receiver_postal_code','floor','receiver_room',
	        'street','building_number','postal_code',
	        'floor','room','landmark','additionalinformation'],
	        )
	
            
	issuer_details = frappe.get_list('Company', 
		    filters={'company_name': source_doc.company},
		    fields=['issuer_id', 'issuer_type', 'issuer_name','branchid',
	        'governate','country_codes','region_city','street','building_number',
	        'postal_code','floor','room','landmark',
	        'additionalinformation'],
	        )
	
	
	if issuer_details:
		doclist.issuer_land_mark,doclist.issuer_id,doclist.issuer_type,doclist.issuer_name,doclist.issuer_branch_id,doclist.issuer_country_codes,doclist.issuer_region_city,doclist.issuer_governate,doclist.issuer_street,doclist.issuer_building_number,doclist.issuer_postal_code,doclist.issuer_floor,doclist.issuer_room,doclist.issuer_additional_informations  = issuer_details[0].landmark,issuer_details[0].issuer_id,issuer_details[0].issuer_type,issuer_details[0].issuer_name,issuer_details[0].branchid,issuer_details[0].country_codes,issuer_details[0].region_city,issuer_details[0].governate,issuer_details[0].street,issuer_details[0].building_number,issuer_details[0].postal_code,issuer_details[0].floor,issuer_details[0].room,issuer_details[0].additionalinformation


	if receiver_details:
		doclist.receiver_id,doclist.receiver_type,doclist.receiver_name,doclist.receiver_country_codes,doclist.receiver_governate,doclist.receiver_street,doclist.region_city,doclist.receiver_building_number,doclist.receiver_postal_code,doclist.receiver_floor,doclist.receiver_room,doclist.receiver_land_mark,doclist.receiver_additional_informations = receiver_details[0].receiver_id,receiver_details[0].receiver_type,receiver_details[0].receiver_name,receiver_details[0].country_codes,receiver_details[0].governate,receiver_details[0].street,receiver_details[0].region_city,receiver_details[0].building_number,receiver_details[0].postal_code,receiver_details[0].floor,receiver_details[0].room,receiver_details[0].receiver_land_mark,receiver_details[0].additionalinformation
  
    
	return doclist
