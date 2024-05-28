from __future__ import unicode_literals
from os import name
import dateutil
import frappe
from frappe import _
import json
from frappe.utils.data import get_link_to_form
import requests
import urllib.request
from datetime import datetime
from base64 import b64encode
from e_invoicing.e_invoicing.doctype.invoice_status.invoice_status import update_job
@frappe.whitelist()
def validate(doc,fun=''):
    for row in getattr(doc,'items',[]):
        row.tax_rate = row.tax_rate or 0
        row.tax_amount = 0
        if row.taxable and row.tax_type and row.item_code :
            row.tax_amount = (row.amount or 0) * (row.tax_rate / 100)
        
        row.net_after_tax = (row.amount or 0) + row.tax_amount


@frappe.whitelist()
def submit_invoice_status(names,status):
    # frappe.msgprint(f"""
    #                 update `tabSales Invoice` set submission_status = 'Pending' where name = '{doc}'
    #                 """)
    names = json.loads(names)
    if len(names) >0: 
        # names.append(0)
        names = ','.join([f"'{x}'" for x in names ])
        try :
            frappe.db.sql("""
                        update `tabSales Invoice` set submission_status = '{status}' where name in ({names})
                        """.format(status=status,names=names))
            frappe.db.commit()
            frappe.msgprint(_(f"Submission Status is Updated to {status}"))
        except Exception as e:
            frappe.msgprint(str(e),indicator='red')
        


def get_token (clientID , clientSecret , base_url):
    # base_url = "https://id.preprod.eta.gov.eg"
    method = "/connect/token"
    str_byte = bytes(f"{clientID}:{clientSecret}", 'utf-8')
    auth = b64encode(str_byte).decode("ascii")
    # headers =  {'Authorization': 'application/octet-stream'}
    headers = { 'Authorization' : f'Basic {auth}',
				 'Content-Type': 'application/x-www-form-urlencoded'}
    body = {"grant_type":"client_credentials"}
    response = requests.post(base_url+method,headers=headers,data=body)
    # frappe.msgprint(str(auth))
    # frappe.msgprint(str(response.json()))
    return response.json().get('access_token')


@frappe.whitelist()
def get_settings ():
    settings = frappe.get_single("E Invoice Setting")
    ApiKey = settings.api_key
    ApiSecret = settings.api_secret
    base_url = settings.server_url
    # x= """
    # http://207.180.207.46/api/method/e_envoice_master.auth.getCustomerInfo
    # token 1718d7dbe233c03:c7925c1bb5c3e4c
    # """
    
    if not (ApiKey and ApiSecret and base_url) :
        frappe.throw(_("Please Set E Invoice Setting"))
    token = f"{ApiKey}:{ApiSecret}"
    method = "api/method/e_envoice_master.auth.getCustomerInfo"
    headers = {'content-type': 'application/json' ,
               "Authorization" : f"token {token}"}
    response = requests.get(base_url+method,headers=headers)
    # frappe.msgprint(base_url+method)
    # frappe.msgprint(str(headers))
    data = response.json()
    if response.status_code != 200 :
        
        # if response.status_code == 400 :
        #     frappe.msgprint(_(data.get('message')))
        # if response.status_code in  (403 , 401) :
        #     frappe.msgprint(_(data.get('_server_messages')))
        frappe.throw(_(str(data.get('message') or data.get('_server_messages')))) 
        # frappe.throw(_("Invalid Auth Please Contact the Support"))
    return data.get("Data")
    
@frappe.whitelist()
def download_pdf(doc):
    # uuid = "77odOdg5i3mdJ4uqXC+iDKmNsdZVVn5PNFE5hSTMBaM="
    token = None
    # settings = frappe.get_single("E Invoice Setting")
    settings = get_settings()
    # frappe.msgprint(str(settings))
    if not settings :
        frappe.throw(_("Invalid E invoice Settings"))
    
    if str(settings.get("EnvironmentType" , "0")) == "0" :
        clientID = settings.get("clintid_prep")
        clientSecret = settings.get("clintsecret1_prep") or settings.get("clintsecret2_prep")
        base_url = "https://api.preprod.invoicing.eta.gov.eg"
        login_url = "https://id.preprod.eta.gov.eg"
    elif str(settings.get("EnvironmentType")) == "1" :
        clientID = settings.get("clintid_prod")
        clientSecret = settings.get("clintsecret1_prod") or settings.get("clintsecret2_prod")
        base_url = "https://api.invoicing.eta.gov.eg"
        login_url = "https://id.eta.gov.eg"
        
    # clientID = settings.client_id
    # clientSecret = settings.client_secret_1
    if not clientID or not clientSecret :
        frappe.throw(_("Please set Client Id and Client Secret in E Invoice Setting"))
    # login_url = settings.login_url or "https://id.preprod.eta.gov.eg"
    # base_url = settings.api_url or "https://api.preprod.invoicing.eta.gov.eg"
    try :
        token = get_token(clientID,clientSecret,login_url)
    except :
        frappe.throw(_("Invalid Token"))
    if not token :
        frappe.throw(_("Invalid Token"))

    doc = frappe.get_doc("Sales Invoice" , doc)
    # if not doc.invstatus or (doc.invstatus or "").lower() != "valid" :
    #     frappe.msgprint(_("Invoice is not valid"),indicator='red')
    uuid = doc.uuid # or doc.long_id
    
    if not uuid :
        frappe.throw(_("Submission Id is Empty"))
    method = f"""/api/v1.0/documents/{uuid}/pdf"""
    headers = {'content-type': 'application/octet-stream' ,
               "Authorization" : f"Bearer {token}"}
    response = requests.get(base_url+method,headers=headers)
    if response.status_code != 200 :
        # frappe.msgprint(str(response.status_code))
        frappe.throw(str(response.json()))
    
    # filepath = "/private/files/"
    # now_time = str(datetime.now())
    # file_name = f"{uuid}_{now_time}.pdf"
    # file_fullname = filepath + file_name
    # with open(file_name, 'wb') as f:
    #     f.write(response.content)
    # # urllib.request.urlretrieve(base_url+method, file_fullname)
    
    # with open("test.pdf", 'rb') as f:
    #     filedata = f.read()
        # frappe.msgprint('str(filedata)')
    frappe.local.response.filename = f'{doc.name}-{uuid}.pdf'
    frappe.local.response.filecontent = response.content
    frappe.local.response.type = "download"
    



@frappe.whitelist()
def cancel_invoice (doc,reason):
    # uuid = "77odOdg5i3mdJ4uqXC+iDKmNsdZVVn5PNFE5hSTMBaM="
    token = None
    # settings = frappe.get_single("E Invoice Setting")
    settings = get_settings()
    # frappe.msgprint(str(settings))
    if not settings :
        frappe.throw(_("Invalid E invoice Settings"))
    
    if str(settings.get("EnvironmentType" , "0")) == "0" :
        clientID = settings.get("clintid_prep")
        clientSecret = settings.get("clintsecret1_prep") or settings.get("clintsecret2_prep")
        base_url = "https://api.preprod.invoicing.eta.gov.eg"
        login_url = "https://id.preprod.eta.gov.eg"
    elif str(settings.get("EnvironmentType")) == "1" :
        clientID = settings.get("clintid_prod")
        clientSecret = settings.get("clintsecret1_prod") or settings.get("clintsecret2_prod")
        base_url = "https://api.invoicing.eta.gov.eg"
        login_url = "https://id.eta.gov.eg"
        
    # clientID = settings.client_id
    # clientSecret = settings.client_secret_1
    if not clientID or not clientSecret :
        frappe.throw(_("Please set Client Id and Client Secret in E Invoice Setting"))
    # login_url = settings.login_url or "https://id.preprod.eta.gov.eg"
    # base_url = settings.api_url or "https://api.preprod.invoicing.eta.gov.eg"
    try :
        token = get_token(clientID,clientSecret,login_url)
    except :
        frappe.throw(_("Invalid Token"))
    if not token :
        frappe.throw(_("Invalid Token"))

    doc = frappe.get_doc("Sales Invoice" , doc)
    # if not doc.invstatus or (doc.invstatus or "").lower() != "valid" :
    #     frappe.msgprint(_("Invoice is not valid"),indicator='red')
    uuid = doc.uuid # or doc.long_id
    if not uuid :
        frappe.throw(_("Submission Id is Empty"))
    
    
    
    data = {
        "status":"cancelled",
        "reason" : reason
    }
    
    method = f"""/api/v1.0/documents/state/{uuid}/state"""
    headers = {'content-type': 'application/json' ,
               "Authorization" : f"Bearer {token}"}
    # frappe.msgprint(base_url+method)
    # frappe.msgprint(f"Bearer {token}")
    # frappe.msgprint(str(data))
    response = requests.put(base_url+method,headers=headers,json=data)
    result = ""
    try : 
        result = response.json()
    except :
        pass
    if response.status_code != 200 :
        frappe.msgprint(str(response.status_code))
        frappe.throw(str(result))
    else :
        frappe.msgprint("Done")





@frappe.whitelist()
def get_document_status (doc,execute_update = 1):
    # uuid = "77odOdg5i3mdJ4uqXC+iDKmNsdZVVn5PNFE5hSTMBaM="
    token = None
    # settings = frappe.get_single("E Invoice Setting")
    settings = get_settings()
    # frappe.msgprint(str(settings))
    if not settings :
        frappe.throw(_("Invalid E invoice Settings"))
    
    if str(settings.get("EnvironmentType" , "0")) == "0" :
        clientID = settings.get("clintid_prep")
        clientSecret = settings.get("clintsecret1_prep") or settings.get("clintsecret2_prep")
        base_url = "https://api.preprod.invoicing.eta.gov.eg"
        login_url = "https://id.preprod.eta.gov.eg"
    elif str(settings.get("EnvironmentType")) == "1" :
        clientID = settings.get("clintid_prod")
        clientSecret = settings.get("clintsecret1_prod") or settings.get("clintsecret2_prod")
        base_url = "https://api.invoicing.eta.gov.eg"
        login_url = "https://id.eta.gov.eg"
        
    # clientID = settings.client_id
    # clientSecret = settings.client_secret_1
    if not clientID or not clientSecret :
        frappe.throw(_("Please set Client Id and Client Secret in E Invoice Setting"))
    # login_url = settings.login_url or "https://id.preprod.eta.gov.eg"
    # base_url = settings.api_url or "https://api.preprod.invoicing.eta.gov.eg"
    try :
        token = get_token(clientID,clientSecret,login_url)
    except :
        frappe.throw(_("Invalid Token"))
    if not token :
        frappe.throw(_("Invalid Token"))

    doc = frappe.get_doc("Sales Invoice" , doc)
    # if not doc.invstatus or (doc.invstatus or "").lower() != "valid" :
    #     frappe.msgprint(_("Invoice is not valid"),indicator='red')
    uuid = doc.uuid # or doc.long_id
    # uuid = "SRM09Y8D8WGFJAEMCMEJDGNF10"
    if not uuid :
        frappe.throw(_("Submission Id is Empty"))
    
    
   
    
    method = f"""/api/v1.0/documents/{uuid}/raw"""
    headers = {'content-type': 'application/x-www-form-urlencoded' ,
               "Authorization" : f"Bearer {token}"}
    # frappe.msgprint(base_url+method)
    # frappe.msgprint(f"Bearer {token}")
    response = requests.get(base_url+method,headers=headers)
    # frappe.msgprint(str(response.status_code))
    # frappe.msgprint(str(response.json()))
    result = response.json()
    if response.status_code != 200 :
        # frappe.msgprint(str(response.status_code))
        frappe.throw(str(response.json()))
    else :
        exist = frappe.db.sql(f"""
                              select name from `tabInvoice Status` where sales_invoice = '{doc.name}' or invinternalid = '{doc.name}' 
                              """,as_dict=1)
        if not exist :
            inv_status = frappe.new_doc("Invoice Status")
        else :
            inv_status = frappe.get_doc("Invoice Status",exist[0].name)
        
        inv_status.sales_invoice = doc.name
        inv_status.invinternalid =   doc.name or result.get("internalId")
        inv_status.invstatus = result.get("status")
        inv_status.longid = result.get("longId")
        inv_status.invuuid = result.get("uuid")
        inv_status.submissionid = result.get("submissionUUID")
        # inv_status.seen = 0
        # inv_status.transdate = dateutil.parser.parse(str(result.get("dateTimeIssued") or  datetime.now()))
        inv_status.save()
        if execute_update :
            update_job()
            frappe.msgprint("Done")




@frappe.whitelist()
def get_documents_status_bulk (names):
	# docs = frappe.db.sql_list(f"""
                           
    #                        select name from `tabSales Invoice` 
    #                        where docstatus = 1 and 
    #                        submission_status = 'Submitted'
    #                        and MONTH(curdate()) = MONTH(date(posting_date))
	# 						""")
    docs = json.loads(str(names))
    for doc in docs :
        try :
                get_document_status(doc,0)
        except :
            pass
    update_job()
    frappe.msgprint(_("Done"))     



@frappe.whitelist()
def get_documents_status_job ():
	docs = frappe.db.sql_list(f"""
                           
                           select name from `tabSales Invoice` 
                           where docstatus = 1 and 
                           submission_status = 'Submitted'
                           and MONTH(curdate()) = MONTH(date(posting_date))
							""")
	for doc in docs :
		try :
				get_document_status(doc,0)
		except :
			pass
	update_job()