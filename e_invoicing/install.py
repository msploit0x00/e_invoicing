from __future__ import unicode_literals
import frappe
import json
from e_invoicing.patches.v5.FinalInvoiceView import execute
Master_Data = "../apps/e_invoicing/e_invoicing/Master Data/"

@frappe.whitelist()
def after_install():
    install_Activity_Types_Data()
    install_Country_Codes_Data ()
    install_Unit_Types_Data()
    install_Taxable_Types_Data()
    install_NON_Taxable_Types_Data()
    install_Tax_Subtypes_Data()
    try : 
        execute()
        print ("Final invoice installed")
    except  Exception as e:
        print ("Final invoice Error " , str(e))
@frappe.whitelist()
def install_Activity_Types_Data ():
    filename = Master_Data+'Activity_types.json'
    try :
        with open(filename) as json_file:
                data = json.load(json_file)
                for p in data:
                    try :
                        # print('Code: ' + p['code'])
                        # print('Desc_en: ' + p['Desc_en'])
                        # print('Desc_ar: ' + p['Desc_ar'])
                        # print('')
                        frappe.get_doc({
                            "doctype":"Activity Types",
                            "code":p.get("code"),
                            "desc_en":p.get("Desc_en"),
                            "desc_ar":p.get("Desc_ar"),
                        }).insert()
                    except Exception as e :
                        return
                        print (str(e))    
    except Exception as e :
        print (str(e))




@frappe.whitelist()
def install_Country_Codes_Data ():
    filename = Master_Data+'Country_Codes.json'
    try :
        with open(filename) as json_file:
                data = json.load(json_file)
                for p in data:
                    try :
                        # print('Code: ' + p['code'])
                        # print('Desc_en: ' + p['Desc_en'])
                        # print('Desc_ar: ' + p['Desc_ar'])
                        # print('')
                        frappe.get_doc({
                            "doctype":"Country Codes",
                            "code":p.get("code"),
                            "desc_en":p.get("Desc_en"),
                            "desc_ar":p.get("Desc_ar"),
                        }).insert()
                    except Exception as e :
                        return
                        print (str(e))    
    except Exception as e :
        print (str(e))
        

@frappe.whitelist()
def install_Unit_Types_Data ():
    filename = Master_Data+'Unit_Types.json'
    try :
        with open(filename) as json_file:
                data = json.load(json_file)
                for p in data:
                    try :
                        # print('Code: ' + p['code'])
                        # print('Desc_en: ' + p['desc_en'])
                        # print('Desc_ar: ' + p['desc_ar'])
                        # print('')
                        frappe.get_doc({
                            "doctype":"Unit Types",
                            "code":p.get("code"),
                            "desc_en":p.get("desc_en"),
                            "desc_ar":p.get("desc_ar"),
                        }).insert()
                    except Exception as e :
                        return
                        print (str(e))    
    except Exception as e :
        print (str(e))



@frappe.whitelist()
def install_Taxable_Types_Data ():
    filename = Master_Data+'Taxable_Types.json'
    try :
        with open(filename) as json_file:
                data = json.load(json_file)
                for p in data:
                    try :
                        # print('Code: ' + p['code'])
                        # print('Desc_en: ' + p['Desc_en'])
                        # print('Desc_ar: ' + p['Desc_ar'])
                        # print('')
                        frappe.get_doc({
                            "doctype":"Taxable Types",
                            "code":p.get("Code"),
                            "desc_en":p.get("Desc_en"),
                            "desc_ar":p.get("Desc_ar"),
                            "taxable":1
                        }).insert()
                    except Exception as e :
                        return
                        print (str(e))    
    except Exception as e :
        print (str(e))



@frappe.whitelist()
def install_NON_Taxable_Types_Data ():
    filename = Master_Data+'Non_Taxable_Types.json'
    try :
        with open(filename) as json_file:
                data = json.load(json_file)
                for p in data:
                    try :
                        # print('Code: ' + p['code'])
                        # print('Desc_en: ' + p['Desc_en'])
                        # print('Desc_ar: ' + p['Desc_ar'])
                        # print('')
                        frappe.get_doc({
                            "doctype":"Taxable Types",
                            "code":p.get("Code"),
                            "desc_en":p.get("Desc_en"),
                            "desc_ar":p.get("Desc_ar"),
                            "taxable":0
                        }).insert()
                    except Exception as e :
                        return
                        print (str(e))    
    except Exception as e :
        print (str(e))


@frappe.whitelist()
def install_Tax_Subtypes_Data ():
    filename = Master_Data+'Tax_Subtypes.json'
    try :
        with open(filename) as json_file:
                data = json.load(json_file)
                for p in data:
                    try :
                        # print('Code: ' + p['code'])
                        # print('Desc_en: ' + p['Desc_en'])
                        # print('Desc_ar: ' + p['Desc_ar'])
                        # print('')
                        frappe.get_doc({
                            "doctype":"Tax Subtypes",
                            "code":p.get("Code"),
                            "desc_en":p.get("Desc_en"),
                            "desc_ar":p.get("Desc_ar"),
                            "parent_tax":p.get("TaxtypeReference")
                        }).insert()
                    except Exception as e :
                        return
                        print (str(e))    
    except Exception as e :
        print (str(e))



                    
                   
