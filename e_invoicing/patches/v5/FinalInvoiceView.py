# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

def execute():
	frappe.db.sql("""
			CREATE OR REPLACE VIEW FinalInvoice as
			Select
				invoice.name as 'internalID',
				(case when invoice.is_return then 'c' else 'i' end) as 'documentType',
				invoice.posting_date as 'dateTimeIssued' ,
				invoice.issuer_name as 'issuer Name' ,
				invoice.issuer_type as 'issuer Type' ,
				invoice.issuer_id as 'issuer ID' ,
				invoice.activity_type as 'taxpayerActivityCode' ,
				invoice.issuer_branch_id as 'Issuer branchID' ,
				invoice.issuer_country_codes as 'Issuer Country' ,
				invoice.issuer_governate as 'Issuer governate' ,
				invoice.issuer_street as 'Issuer Street' ,
				invoice.issuer_building_number as 'Issuer BUILDINGNUMBER' ,
				invoice.issuer_postal_code as 'Issuer POSTALCODE' ,
				invoice.issuer_floor as 'Issuer FLOOR' ,
				invoice.issuer_room as 'Issuer ROOM' ,
				invoice.issuer_region_city as 'COMP_REGIONCITY' ,
				invoice.issuer_land_mark as 'Issuer Landmark' ,
				invoice.issuer_additional_informations as 'Issuer Additional inforamtion' ,
				invoice.receiver_id as 'Receiver ID' ,
				invoice.receiver_type as 'Receiver Type' ,
				invoice.receiver_name as 'Receiver Name' ,
				invoice.receiver_country_codes as 'Receiver Country' ,
				invoice.receiver_governate as 'Receiver Governate' ,
				invoice.region_city as 'Receiver RegionCity' ,
				invoice.receiver_street as 'Receiver Street' ,
				invoice.receiver_building_number as 'Receiver BUILDINGNUMBER' ,
				invoice.receiver_postal_code as 'Receiver POSTALCODE' ,
				invoice.receiver_floor as 'Receiver FLOOR' ,
				invoice.receiver_room as 'Receiver ROOM' ,
				invoice.receiver_land_mark as 'Receiver Landmark' ,
				invoice.receiver_additional_informations as 'Receiver Additional inforamtion' ,
				item.itemtype as 'itemType' ,
				item.itemcode as 'itemCode' ,
				item.internalcode as 'internalCode' ,
				item.description_code as 'description' ,
				item.qty as 'quantity' ,
				invoice.conversion_rate as 'currencyExchangeRate' ,
				invoice.currency as 'currencySold' ,
				item.base_rate as 'amountEGP' ,
				item.rate as 'amountSold' ,
				item.base_amount as 'salesTotal' ,
				item.base_amount as 'netTotal' ,
				item.tax_type as 'taxableItems type' ,
				item.tax_amount as 'taxableItems amount' ,
				item.tax_subtype as 'taxableItems subType' ,
				item.tax_rate as 'taxableItems rate' ,
				0 as 'discount rate' ,
				0 as 'discount amount' ,
				item.base_net_amount  as 'total' ,
				item.unittype as 'unitType'

			from `tabSales Invoice` invoice inner join `tabSales Invoice Item` item
			on item.parent = invoice.name
			where invoice.submission_status = 'Pending'
			and invoice.docstatus = 1 ;
   select 1 as '1'

			""")
	# frappe.db.commit()
	frappe.clear_cache()

