# from __future__ import unicode_literals
# import frappe


# def execute(filters=None):
#     columns = [
#         {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
#         {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Data", "width": 300},
#         {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "currency", "width": 100},
#         {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#     ]

#     data = []
#     doc_totals = {}

#     doctypes = [
#         {"doctype": "Sales Invoice",    "item_table": "Sales Invoice Item"},
#         {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
#         {"doctype": "Journal Entry",    "item_table": None},
#         {"doctype": "Purchase Receipt", "item_table": "Purchase Receipt Item"},
#         {"doctype": "Delivery Note",    "item_table": "Delivery Note Item"},
#         {"doctype": "Sales Order",      "item_table": "Sales Order Item"},
#         {"doctype": "Purchase Order",   "item_table": "Purchase Order Item"},
#         {"doctype": "Expense Claim",    "item_table": "Expense Claim Detail"},
#     ]

#     for dt in doctypes:
#         doctype = dt["doctype"]
#         item_table = dt.get("item_table")

#         try:
#             meta = frappe.get_meta(doctype)
#         except frappe.DoesNotExistError:
#             continue

#         available_fields = [df.fieldname for df in meta.fields]
#         fields = ["name"]
#         if "grand_total" in available_fields:
#             fields.append("grand_total")
#         if "rounded_total" in available_fields:
#             fields.append("rounded_total")
#         if "outstanding_amount" in available_fields:
#             fields.append("outstanding_amount")

#         doc_totals[doctype] = 0.0

#         records = frappe.get_all(
#             doctype,
#             filters={"docstatus": 1},
#             fields=fields,
#             ignore_permissions=True
#         )

#         for rec in records:
#             name = rec.get("name")
#             grand_total = rec.get("grand_total")
#             rounded_total = rec.get("rounded_total")
#             outstanding = rec.get("outstanding_amount")

#             if grand_total:
#                 doc_totals[doctype] += grand_total

#             base_row = {
#                 "doctype": doctype,
#                 "doc_name": name,
#                 "grand_total": grand_total,
#                 "rounded_total": rounded_total,
#                 "outstanding_amount": outstanding,
#                 "rate": None,
#                 "amount": None
#             }
#             data.append(base_row.copy())

#             if item_table:
#                 items = frappe.get_all(
#                     item_table,
#                     filters={"parent": name},
#                     fields=["item_code", "rate", "amount"]
#                 )
#                 for item in items:
#                     data.append({
#                         "doctype": doctype,
#                         "doc_name": f"↳ Item: {item.get('item_code')}",
#                         "grand_total": None,
#                         "rounded_total": None,
#                         "outstanding_amount": None,
#                         "rate": item.get("rate"),
#                         "amount": item.get("amount")
#                     })

#             if doctype in ["Sales Invoice", "Purchase Invoice"]:
#                 pe_refs = frappe.get_all(
#                     "Payment Entry Reference",
#                     filters={"reference_doctype": doctype, "reference_name": name},
#                     fields=["parent"]
#                 )
#                 for ref in pe_refs:
#                     pe_name = ref.parent
#                     paid_amt = frappe.db.get_value("Payment Entry", pe_name, "paid_amount")
#                     data.append({
#                         "doctype": "Payment Entry",
#                         "doc_name": f"↳ Payment Entry: {pe_name}",
#                         "grand_total": None,
#                         "rounded_total": None,
#                         "outstanding_amount": None,
#                         "rate": None,
#                         "amount": paid_amt
#                     })

#     chart = {
#         "data": {
#             "labels": list(doc_totals.keys()),
#             "datasets": [{"values": list(doc_totals.values())}]
#         },
#         "type": "pie",
#         "height": 300
#     }

#     cumulative_total = sum(doc_totals.values())
#     report_summary = [{
#         "value": cumulative_total,
#         "indicator": "Green" if cumulative_total >= 0 else "Red",
#         "label": "Cumulative Total",
#         "datatype": "Currency",
#         "currency": frappe.get_cached_value('Company', frappe.db.get_default('company'), 'default_currency')
#             if frappe.db.get_default('company') else ""
#     }]

#     return columns, data, None, chart, report_summary



from __future__ import unicode_literals
import frappe
from frappe.utils import get_link_to_form, get_url_to_form

def execute(filters=None):
    columns = [
        {
            "label": "Document Type",
            "fieldname": "doctype",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Document / Item / Payment",
            "fieldname": "doc_name",
            "fieldtype": "Data",  # Use Data to allow HTML rendering
            "width": 300
        },
        {
            "label": "Grand Total",
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        },
        {
            "label": "Rounded Total",
            "fieldname": "rounded_total",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        },
        {
            "label": "Outstanding Amt",
            "fieldname": "outstanding_amount",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        },
        {
            "label": "Rate",
            "fieldname": "rate",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 100
        },
        {
            "label": "Amount",
            "fieldname": "amount",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        },
    ]

    data = []
    doc_totals = {}

    doctypes = [
        {"doctype": "Sales Invoice", "item_table": "Sales Invoice Item"},
        {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
        {"doctype": "Journal Entry", "item_table": None},
        {"doctype": "Purchase Receipt", "item_table": "Purchase Receipt Item"},
        {"doctype": "Delivery Note", "item_table": "Delivery Note Item"},
        {"doctype": "Sales Order", "item_table": "Sales Order Item"},
        {"doctype": "Purchase Order", "item_table": "Purchase Order Item"},
        {"doctype": "Expense Claim", "item_table": "Expense Claim Detail"},
    ]

    for dt in doctypes:
        doctype = dt["doctype"]
        item_table = dt.get("item_table")

        try:
            meta = frappe.get_meta(doctype)
        except frappe.DoesNotExistError:
            continue

        available_fields = [df.fieldname for df in meta.fields]
        fields = ["name"]
        if "grand_total" in available_fields:
            fields.append("grand_total")
        if "rounded_total" in available_fields:
            fields.append("rounded_total")
        if "outstanding_amount" in available_fields:
            fields.append("outstanding_amount")

        doc_totals[doctype] = 0.0
        
        date_filter_field = "posting_date" if "posting_date" in available_fields else "transaction_date" if "transaction_date" in available_fields else None
        filters_dict = {"docstatus": 1}
        if date_filter_field and filters.get("from_date") and filters.get("to_date"):
             filters_dict[date_filter_field] = ["between", [filters["from_date"], filters["to_date"]]]
        records = frappe.get_all(
			doctype,
			filters=filters_dict,
			fields=fields,
			ignore_permissions=True
        )

    
	   # records = frappe.get_all(
        #     doctype,
        #     filters={"docstatus": 1},
        #     fields=fields,
        #     ignore_permissions=True
        # )



        for rec in records:
            name = rec.get("name")
            grand_total = rec.get("grand_total")
            rounded_total = rec.get("rounded_total")
            outstanding = rec.get("outstanding_amount")

            if grand_total:
                doc_totals[doctype] += grand_total

            # Use get_link_to_form to generate the clickable link
            base_row = {
                "doctype": doctype,
                "doc_name": get_link_to_form(doctype, name, name),  # Ensure the label is the document name
                "grand_total": grand_total,
                "rounded_total": rounded_total,
                "outstanding_amount": outstanding,
                "rate": None,
                "amount": None,
                "indent": 0
            }
            data.append(base_row)

            if item_table:
                items = frappe.get_all(
                    item_table,
                    filters={"parent": name},
                    fields=["item_code", "rate", "amount"]
                )
                for item in items:
                    data.append({
                        "doctype": doctype,
                        "doc_name": f"Item: {item.get('item_code')}",
                        "grand_total": None,
                        "rounded_total": None,
                        "outstanding_amount": None,
                        "rate": item.get("rate"),
                        "amount": item.get("amount"),
                        "indent": 1
                    })

            if doctype in ["Sales Invoice", "Purchase Invoice"]:
                pe_refs = frappe.get_all(
                    "Payment Entry Reference",
                    filters={"reference_doctype": doctype, "reference_name": name},
                    fields=["parent"]
                )
                for ref in pe_refs:
                    pe_name = ref.parent
                    paid_amt = frappe.db.get_value("Payment Entry", pe_name, "paid_amount")
                    data.append({
                        "doctype": "Payment Entry",
                        "doc_name": f"Payment Entry: {get_link_to_form('Payment Entry', pe_name, pe_name)}",
                        "grand_total": None,
                        "rounded_total": None,
                        "outstanding_amount": None,
                        "rate": None,
                        "amount": paid_amt,
                        "indent": 1
                    })

    chart = {
        "data": {
            "labels": list(doc_totals.keys()),
            "datasets": [{"values": list(doc_totals.values())}]
        },
        "type": "pie",
        "height": 300
    }

    cumulative_total = sum(doc_totals.values())
    report_summary = [{
        "value": cumulative_total,
        "indicator": "Green" if cumulative_total >= 0 else "Red",
        "label": "Cumulative Total",
        "datatype": "Currency",
        "currency": frappe.get_cached_value('Company', frappe.db.get_default('company'), 'default_currency')
            if frappe.db.get_default('company') else ""
    }]

    return columns, data, None, chart, report_summary
