# Copyright (c) 2013, Peter maged and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns(filters)
	return columns, data


def get_columns(filters):
    columns = [
		{
			"fieldname":"internalID" ,
			"label":_("internalID"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"documentType" ,
			"label":_("documentType"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"dateTimeIssued" ,
			"label":_("dateTimeIssued"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"issuer Name" ,
			"label":_("issuer Name"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"issuer Type" ,
			"label":_("issuer Type"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"issuer ID" ,
			"label":_("issuer ID"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"taxpayerActivityCode" ,
			"label":_("taxpayerActivityCode"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer branchID" ,
			"label":_("Issuer branchID"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer Country" ,
			"label":_("Issuer Country"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer governate" ,
			"label":_("Issuer governate"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer Street" ,
			"label":_("Issuer Street"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer BUILDINGNUMBER" ,
			"label":_("Issuer BUILDINGNUMBER"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer POSTALCODE" ,
			"label":_("Issuer POSTALCODE"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer FLOOR" ,
			"label":_("Issuer FLOOR"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer ROOM" ,
			"label":_("Issuer ROOM"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"COMP_REGIONCITY" ,
			"label":_("COMP_REGIONCITY"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer Landmark" ,
			"label":_("Issuer Landmark"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Issuer Additional inforamtion" ,
			"label":_("Issuer Additional inforamtion"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver ID" ,
			"label":_("Receiver ID"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver Type" ,
			"label":_("Receiver Type"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver Name" ,
			"label":_("Receiver Name"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver Country" ,
			"label":_("Receiver Country"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver Governate" ,
			"label":_("Receiver Governate"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver RegionCity" ,
			"label":_("Receiver RegionCity"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver Street" ,
			"label":_("Receiver Street"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver BUILDINGNUMBER" ,
			"label":_("Receiver BUILDINGNUMBER"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver POSTALCODE" ,
			"label":_("Receiver POSTALCODE"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver FLOOR" ,
			"label":_("Receiver FLOOR"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver ROOM" ,
			"label":_("Receiver ROOM"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver Landmark" ,
			"label":_("Receiver Landmark"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"Receiver Additional inforamtion" ,
			"label":_("Receiver Additional inforamtion"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"itemType" ,
			"label":_("itemType"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"itemCode" ,
			"label":_("itemCode"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"internalCode" ,
			"label":_("internalCode"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"description" ,
			"label":_("description"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"quantity" ,
			"label":_("quantity"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"currencyExchangeRate" ,
			"label":_("currencyExchangeRate"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"currencySold" ,
			"label":_("currencySold"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"amountEGP" ,
			"label":_("amountEGP"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"amountSold" ,
			"label":_("amountSold"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"salesTotal" ,
			"label":_("salesTotal"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"netTotal" ,
			"label":_("netTotal"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"taxableItems type" ,
			"label":_("taxableItems type"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"taxableItems amount" ,
			"label":_("taxableItems amount"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"taxableItems subType" ,
			"label":_("taxableItems subType"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"taxableItems rate" ,
			"label":_("taxableItems rate"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"discount rate" ,
			"label":_("discount rate"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"discount amount" ,
			"label":_("discount amount"),
			"fieldtype":"Data",
			'width':150
		},
  
  
		{
			"fieldname":"total" ,
			"label":_("total"),
			"fieldtype":"Data",
			'width':150
		},
		{
			"fieldname":"unitType" ,
			"label":_("unitType"),
			"fieldtype":"Data",
			'width':150
		},
	]
    return columns
def get_data (filters):
	result = frappe.db.sql ("""
                         
		select * from FinalInvoice ;

							""",as_dict = 1)
	return result