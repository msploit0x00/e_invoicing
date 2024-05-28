frappe.ui.form.on("Sales Invoice", {
  refresh(frm) {
    // your code here
    // if (frm.doc.items) {
    //     frm.doc.items.forEach((e) => {
    //         frm.events.set_total(frmm
    if (frm.doc.docstatus == 1) {
      frm.add_custom_button(
        __("Submit To Portal"),
        function () {
          frm.events.submit_invoice_status(frm, "Pending");
        },
        __("E Invoice Portal")
      );
      frm.add_custom_button(
        __("Cancel Submission"),
        function () {
          frm.events.submit_invoice_status(frm, "Cancelled");
        },
        __("E Invoice Portal")
      );
      // if ((frm.doc.invstatus || "").toString().lower() == "valid") {
      frm.add_custom_button(
        __("Download PDF"),
        function () {
          frm.events.download_pdf(frm);
        },
        __("E Invoice Portal")
      );
      frm.add_custom_button(
        __("Cancel Invoice from Portal"),
        function () {
          frm.events.cancel_invoice(frm);
        },
        __("E Invoice Portal")
      );
      frm.add_custom_button(
        __("Get Document Status"),
        function () {
          frm.events.get_document_status(frm);
        },
        __("E Invoice Portal")
      );
      // }
    }
  },
  submit_invoice_status: function (frm, status) {
    frappe.call({
      method:
        "e_invoicing.e_invoicing.doctype.sales_invoice.sales_invoice.submit_invoice_status",
      args: {
        names: [frm.doc.name],
        status: status,
      },
      callback: function (r) {
        frm.doc.submission_status = status;
        frm.refresh_field("submission_status");
      },
    });
  },
  download_pdf: function (frm) {
    window.open(
      `/api/method/e_invoicing.e_invoicing.doctype.sales_invoice.sales_invoice.download_pdf?doc=${frm.doc.name}`
    );
    // frappe.call({
    //   method:
    //     "e_invoicing.e_invoicing.doctype.sales_invoice.sales_invoice.get_settings",
    //   // args: {
    //   //   doc: frm.doc.name,
    //   //   // uuid: "1PZ0Z1XDD4JFADKHTVY4JFKF10",
    //   // },
    //   callback:function(){
    //     // frm.doc.submission_status = status
    //     // frm.refresh_field("submission_status")
    //   }
    // });
  },
  get_document_status : function (frm) {

    frappe.call({
      method:
        "e_invoicing.e_invoicing.doctype.sales_invoice.sales_invoice.get_document_status",
      args: {
        doc: frm.doc.name,
      },
      callback:function(){
        // frm.doc.submission_status = status
        frm.refresh()
      }
    });
  },
  cancel_invoice: function (frm) {
    var dialog = new frappe.ui.Dialog({
      title: __("Please Set Reason"),
      fields: [
        {
          label: "Reason",
          fieldname: "reason",
          fieldtype: "Select",
          options: ["Wrong buyer details", "Wrong invoice details", "Other"],
          default: "Wrong buyer details",
          reqd: 1,
        },
        {
          label: "Details",
          fieldname: "details",
          fieldtype: "Data",
          // options: ["Wrong buyer details", "Wrong invoice details", "Other"],
          // default: "Wrong buyer details",
          length: 60,
          hidden:1  
          // reqd: 1,
        },
      ],
      primary_action: function () {
        var data = dialog.get_values();
        let reason = data.reason == "Other" ? data.details :  data.reason
        frappe.call({
          method:
            "e_invoicing.e_invoicing.doctype.sales_invoice.sales_invoice.cancel_invoice",
          args: {
            doc: frm.doc.name,
            reason: reason,
          },
          callback: function () {
            frm.refresh();
          },
        });

        dialog.hide();
      },
      primary_action_label: __("Cancel Invoice"),
    });

    dialog.fields_dict["reason"].df.onchange = () => {
      var reason = dialog.fields_dict.reason.input.value;
      // if (reason == "Other") {
      dialog.fields_dict["details"].df.hidden = reason != "Other";
      dialog.fields_dict["details"].df.reqd = reason == "Other";
      dialog.refresh()
      // }
    };
    dialog.show();
  },
  async set_total(frm, cdt, cdn) {
    // your code here
    // await frm.script_manager.trigger("rate", cdt, cdn);
    var row = locals[cdt][cdn];
    row.tax_rate = row.tax_rate || 0;
    row.tax_amount = 0;
    row.net_after_tax = row.amount;
    if (row.taxable && row.tax_type && row.item_code) {
      row.tax_amount = (row.net_amount || 0) * (row.tax_rate / 100);
    }
    row.net_after_tax = (row.amount || 0) + row.tax_amount;
    frm.refresh_field("items");
  },
});

frappe.ui.form.on("Sales Invoice Item", {
  tax_type(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
  tax_rate(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
  taxable(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
  amount(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
  qty(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
  rate(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
  item_code(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
  price_list_rate(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
  discount_amount(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
  discount_percentage(frm, cdt, cdn) {
    // your code here
    frm.events.set_total(frm, cdt, cdn);
  },
});
