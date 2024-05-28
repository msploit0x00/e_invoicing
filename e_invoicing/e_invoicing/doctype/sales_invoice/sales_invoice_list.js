// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
frappe.listview_settings["Sales Invoice"] = {
  onload: function (listview) {
    var method =
      "e_invoicing.e_invoicing.doctype.sales_invoice.sales_invoice.submit_invoice_status";

    listview.page.add_menu_item(__("Submit To Portal"), function () {
      listview.call_for_selected_items(method, { status: "Pending" });
      listview.refresh();
    });

    method =
      "e_invoicing.e_invoicing.doctype.sales_invoice.sales_invoice.submit_invoice_status";
    listview.page.add_menu_item(__("Cancel Submission ti Portal"), function () {
      listview.call_for_selected_items(method, { status: "Cancelled" });
      listview.refresh();
    });

    method =
      "e_invoicing.e_invoicing.doctype.sales_invoice.sales_invoice.get_documents_status_bulk";
    listview.page.add_menu_item(__("Get Documents Status"), function () {
      listview.call_for_selected_items(method);
      listview.refresh();
    });
  },
};
