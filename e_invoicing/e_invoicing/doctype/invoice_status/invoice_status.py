# -*- coding: utf-8 -*-
# Copyright (c) 2021, Peter maged and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
class InvoiceStatus(Document):
	pass


@frappe.whitelist()
def update_job ():
    
	log_names = []
	logs = frappe.db.sql ("""
							select * from `tabInvoice Status` order by  invinternalid asc, creation asc
							""",as_dict=1) or []
	for log in logs :
		frappe.db.sql(f"""
                update `tabSales Invoice` set
					submission_status = 'Submitted' ,
					submission_id = '{log.submissionid}' ,
					invstatuscode = '{log.invstatuscode}' ,
					transdate = '{log.transdate}' ,
					invstatus = '{log.invstatus}' ,
					erroemessage = '{log.erroemessage}' ,
					errordetailsmessage = '{log.errordetailsmessage}' ,
					hash_key = '{log.hashkey}' ,
					long_id = '{log.longid}' ,
					error_code = '{log.errorcode}' ,
					error_message = '{log.erroemessage}' ,
					uuid='{log.invuuid}'
					

					where name = '{log.invinternalid}'
                """)
		log_names.append(f"'{log.name}'")
	if len(log_names) > 0 :
		frappe.db.sql("""
						update `tabInvoice Status` set seen = 1 ,docstatus = 1 , sales_invoice = invinternalid where name in ({})
						""".format(','.join(log_names)))
	frappe.db.commit()
 
 
