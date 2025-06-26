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



# from __future__ import unicode_literals
# import frappe
# from frappe.utils import get_link_to_form, get_url_to_form

# def execute(filters=None):
#     columns = [
#         {
#             "label": "Document Type",
#             "fieldname": "doctype",
#             "fieldtype": "Data",
#             "width": 150
#         },
#         {
#             "label": "Document / Item / Payment",
#             "fieldname": "doc_name",
#             "fieldtype": "Data",  # Use Data to allow HTML rendering
#             "width": 300
#         },
#         {
#             "label": "Grand Total",
#             "fieldname": "grand_total",
#             "fieldtype": "Currency",
#             "options": "currency",
#             "width": 120
#         },
#         {
#             "label": "Rounded Total",
#             "fieldname": "rounded_total",
#             "fieldtype": "Currency",
#             "options": "currency",
#             "width": 120
#         },
#         {
#             "label": "Outstanding Amt",
#             "fieldname": "outstanding_amount",
#             "fieldtype": "Currency",
#             "options": "currency",
#             "width": 120
#         },
#         {
#             "label": "Rate",
#             "fieldname": "rate",
#             "fieldtype": "Currency",
#             "options": "currency",
#             "width": 100
#         },
#         {
#             "label": "Amount",
#             "fieldname": "amount",
#             "fieldtype": "Currency",
#             "options": "currency",
#             "width": 120
#         },
#     ]

#     data = []
#     doc_totals = {}

#     doctypes = [
#         {"doctype": "Sales Invoice", "item_table": "Sales Invoice Item"},
#         {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
#         {"doctype": "Journal Entry", "item_table": None},
#         {"doctype": "Purchase Receipt", "item_table": "Purchase Receipt Item"},
#         {"doctype": "Delivery Note", "item_table": "Delivery Note Item"},
#         {"doctype": "Sales Order", "item_table": "Sales Order Item"},
#         {"doctype": "Purchase Order", "item_table": "Purchase Order Item"},
#         {"doctype": "Expense Claim", "item_table": "Expense Claim Detail"},
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
        
#         date_filter_field = "posting_date" if "posting_date" in available_fields else "transaction_date" if "transaction_date" in available_fields else None
#         filters_dict = {"docstatus": 1}
#         if date_filter_field and filters.get("from_date") and filters.get("to_date"):
#              filters_dict[date_filter_field] = ["between", [filters["from_date"], filters["to_date"]]]
#         records = frappe.get_all(
# 			doctype,
# 			filters=filters_dict,
# 			fields=fields,
# 			ignore_permissions=True
#         )

    
# 	   # records = frappe.get_all(
#         #     doctype,
#         #     filters={"docstatus": 1},
#         #     fields=fields,
#         #     ignore_permissions=True
#         # )



#         for rec in records:
#             name = rec.get("name")
#             grand_total = rec.get("grand_total")
#             rounded_total = rec.get("rounded_total")
#             outstanding = rec.get("outstanding_amount")

#             if grand_total:
#                 doc_totals[doctype] += grand_total

#             # Use get_link_to_form to generate the clickable link
#             base_row = {
#                 "doctype": doctype,
#                 "doc_name": get_link_to_form(doctype, name, name),  # Ensure the label is the document name
#                 "grand_total": grand_total,
#                 "rounded_total": rounded_total,
#                 "outstanding_amount": outstanding,
#                 "rate": None,
#                 "amount": None,
#                 "indent": 0
#             }
#             data.append(base_row)

#             if item_table:
#                 items = frappe.get_all(
#                     item_table,
#                     filters={"parent": name},
#                     fields=["item_code", "rate", "amount"]
#                 )
#                 for item in items:
#                     data.append({
#                         "doctype": doctype,
#                         "doc_name": f"Item: {item.get('item_code')}",
#                         "grand_total": None,
#                         "rounded_total": None,
#                         "outstanding_amount": None,
#                         "rate": item.get("rate"),
#                         "amount": item.get("amount"),
#                         "indent": 1
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
#                         "doc_name": f"Payment Entry: {get_link_to_form('Payment Entry', pe_name, pe_name)}",
#                         "grand_total": None,
#                         "rounded_total": None,
#                         "outstanding_amount": None,
#                         "rate": None,
#                         "amount": paid_amt,
#                         "indent": 1
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



# from __future__ import unicode_literals
# import frappe
# from frappe.utils import get_link_to_form

# def execute(filters=None):
#     columns = [
#         {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
#         {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Data", "width": 300},
#         {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "currency", "width": 100},
#         {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Total Debit", "fieldname": "total_debit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Total Credit", "fieldname": "total_credit", "fieldtype": "Currency", "options": "currency", "width": 120},
#     ]

#     data = []
#     doc_totals = {}

#     doctypes = [
#         {"doctype": "Sales Invoice", "item_table": "Sales Invoice Item"},
#         {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
#         {"doctype": "Journal Entry", "item_table": "Journal Entry Account"},
#         {"doctype": "Purchase Receipt", "item_table": "Purchase Receipt Item"},
#         {"doctype": "Delivery Note", "item_table": "Delivery Note Item"},
#         {"doctype": "Sales Order", "item_table": "Sales Order Item"},
#         {"doctype": "Purchase Order", "item_table": "Purchase Order Item"},
#         {"doctype": "Expense Claim", "item_table": "Expense Claim Detail"},
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
#         if doctype == "Journal Entry":
#             fields += ["total_debit", "total_credit"]

#         doc_totals[doctype] = 0.0

#         date_filter_field = "posting_date" if "posting_date" in available_fields else "transaction_date" if "transaction_date" in available_fields else None
#         filters_dict = {"docstatus": 1}
#         if date_filter_field and filters and filters.get("from_date") and filters.get("to_date"):
#             filters_dict[date_filter_field] = ["between", [filters["from_date"], filters["to_date"]]]

#         records = frappe.get_all(
#             doctype,
#             filters=filters_dict,
#             fields=fields,
#             ignore_permissions=True
#         )

#         for rec in records:
#             name = rec.get("name")
#             grand_total = rec.get("grand_total")
#             rounded_total = rec.get("rounded_total")
#             outstanding = rec.get("outstanding_amount")
#             total_debit = rec.get("total_debit")
#             total_credit = rec.get("total_credit")

#             if grand_total:
#                 doc_totals[doctype] += grand_total
#             elif total_debit:
#                 doc_totals[doctype] += total_debit  # Use total_debit as primary aggregation for Journal Entry

#             base_row = {
#                 "doctype": doctype,
#                 "doc_name": get_link_to_form(doctype, name, name),
#                 "grand_total": grand_total,
#                 "rounded_total": rounded_total,
#                 "outstanding_amount": outstanding,
#                 "rate": None,
#                 "amount": None,
#                 "total_debit": total_debit,
#                 "total_credit": total_credit,
#                 "indent": 0
          
            
#             }
#             data.append(base_row)

#             if item_table:
#                 child_fields = ["item_code", "rate", "amount"] if doctype != "Journal Entry" else ["account", "debit", "credit"]
#                 items = frappe.get_all(
#                     item_table,
#                     filters={"parent": name},
#                     fields=child_fields
#                 )
#                 for item in items:
#                     data.append({
#                         "doctype": doctype,
#                         "doc_name": f"Item: {item.get('item_code') or item.get('account')}",
#                         "grand_total": None,
#                         "rounded_total": None,
#                         "outstanding_amount": None,
#                         "rate": item.get("rate"),
#                         "amount": item.get("amount"),
#                         "total_debit": item.get("debit"),
#                         "total_credit": item.get("credit"),
#                         "indent": 1
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
#                         "doc_name": f"Payment Entry: {get_link_to_form('Payment Entry', pe_name, pe_name)}",
#                         "grand_total": None,
#                         "rounded_total": None,
#                         "outstanding_amount": None,
#                         "rate": None,
#                         "amount": paid_amt,
#                         "total_debit": None,
#                         "total_credit": None,
#                         "indent": 1
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



# from __future__ import unicode_literals
# import frappe
# from frappe.utils import get_link_to_form

# def execute(filters=None):
#     columns = [
#         {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
#         {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Data", "width": 300},
#         {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "currency", "width": 100},
#         {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
#         {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Total Debit", "fieldname": "total_debit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Total Credit", "fieldname": "total_credit", "fieldtype": "Currency", "options": "currency", "width": 120},
#     ]

#     data = []
#     doc_totals = {}

#     doctypes = [
#         {"doctype": "Sales Invoice", "item_table": "Sales Invoice Item"},
#         {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
#         {"doctype": "Journal Entry", "item_table": "Journal Entry Account"},
#         {"doctype": "Purchase Receipt", "item_table": "Purchase Receipt Item"},
#         {"doctype": "Delivery Note", "item_table": "Delivery Note Item"},
#         {"doctype": "Sales Order", "item_table": "Sales Order Item"},
#         {"doctype": "Purchase Order", "item_table": "Purchase Order Item"},
#         {"doctype": "Expense Claim", "item_table": "Expense Claim Detail"},
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
#         if doctype == "Journal Entry":
#             fields += ["total_debit", "total_credit"]

#         doc_totals[doctype] = 0.0

#         date_filter_field = "posting_date" if "posting_date" in available_fields else "transaction_date" if "transaction_date" in available_fields else None
#         filters_dict = {"docstatus": 1}
#         if date_filter_field and filters and filters.get("from_date") and filters.get("to_date"):
#             filters_dict[date_filter_field] = ["between", [filters["from_date"], filters["to_date"]]]

#         records = frappe.get_all(
#             doctype,
#             filters=filters_dict,
#             fields=fields,
#             ignore_permissions=True
#         )

#         for rec in records:
#             name = rec.get("name")
#             grand_total = rec.get("grand_total")
#             rounded_total = rec.get("rounded_total")
#             outstanding = rec.get("outstanding_amount")
#             total_debit = rec.get("total_debit")
#             total_credit = rec.get("total_credit")

#             if grand_total:
#                 doc_totals[doctype] += grand_total
#             elif total_debit:
#                 doc_totals[doctype] += total_debit

#             base_row = {
#                 "doctype": doctype,
#                 "doc_name": get_link_to_form(doctype, name, name),
#                 "grand_total": grand_total,
#                 "rounded_total": rounded_total,
#                 "outstanding_amount": outstanding,
#                 "rate": None,
#                 "amount": None,
#                 "account": None,
#                 "debit": None,
#                 "credit": None,
#                 "total_debit": total_debit,
#                 "total_credit": total_credit,
#                 "indent": 0
#             }
#             data.append(base_row)

#             if item_table:
#                 if doctype == "Journal Entry":
#                     child_fields = ["account", "debit_in_account_currency", "credit_in_account_currency"]
#                 else:
#                     child_fields = ["item_code", "rate", "amount"]

#                 items = frappe.get_all(
#                     item_table,
#                     filters={"parent": name},
#                     fields=child_fields
#                 )

#                 for item in items:
#                     child_row = {
#                         "doctype": doctype,
#                         "doc_name": f"Item: {item.get('item_code') or item.get('account')}",
#                         "grand_total": None,
#                         "rounded_total": None,
#                         "outstanding_amount": None,
#                         "rate": item.get("rate") if doctype != "Journal Entry" else None,
#                         "amount": item.get("amount") if doctype != "Journal Entry" else None,
#                         "account": item.get("account") if doctype == "Journal Entry" else None,
#                         "debit": item.get("debit_in_account_currency") if doctype == "Journal Entry" else None,
#                         "credit": item.get("credit_in_account_currency") if doctype == "Journal Entry" else None,
#                         "total_debit": None,
#                         "total_credit": None,
#                         "indent": 1
                      
#                     }
#                     data.append(child_row)

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
#                         "doc_name": f"Payment Entry: {get_link_to_form('Payment Entry', pe_name, pe_name)}",
#                         "grand_total": None,
#                         "rounded_total": None,
#                         "outstanding_amount": None,
#                         "rate": None,
#                         "amount": paid_amt,
#                         "account": None,
#                         "debit": None,
#                         "credit": None,
#                         "total_debit": None,
#                         "total_credit": None,
#                         "indent": 1
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
from frappe.utils import get_link_to_form

def execute(filters=None):
    columns = [
        {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
        {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Data", "width": 300},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "currency", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Total Debit", "fieldname": "total_debit", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Total Credit", "fieldname": "total_credit", "fieldtype": "Currency", "options": "currency", "width": 120},
        # New columns for Bank Transaction details
        {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
        {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
        {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "currency", "width": 120},
    ]

    data = []
    doc_totals = {}

    doctypes = [
        {"doctype": "Sales Invoice", "item_table": "Sales Invoice Item"},
        {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
        {"doctype": "Journal Entry", "item_table": "Journal Entry Account"},
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
        if doctype == "Journal Entry":
            fields += ["total_debit", "total_credit"]

        doc_totals[doctype] = 0.0

        date_filter_field = "posting_date" if "posting_date" in available_fields else "transaction_date" if "transaction_date" in available_fields else None
        filters_dict = {"docstatus": 1}
        if date_filter_field and filters and filters.get("from_date") and filters.get("to_date"):
            filters_dict[date_filter_field] = ["between", [filters["from_date"], filters["to_date"]]]

        records = frappe.get_all(
            doctype,
            filters=filters_dict,
            fields=fields,
            ignore_permissions=True
        )

        for rec in records:
            name = rec.get("name")
            grand_total = rec.get("grand_total")
            rounded_total = rec.get("rounded_total")
            outstanding = rec.get("outstanding_amount")
            total_debit = rec.get("total_debit")
            total_credit = rec.get("total_credit")

            if grand_total:
                doc_totals[doctype] += grand_total
            elif total_debit:
                doc_totals[doctype] += total_debit

            # Base row for the document (indent=0)
            base_row = {
                "doctype": doctype,
                "doc_name": get_link_to_form(doctype, name, name),
                "grand_total": grand_total,
                "rounded_total": rounded_total,
                "outstanding_amount": outstanding,
                "rate": None,
                "amount": None,
                "account": None,
                "debit": None,
                "credit": None,
                "total_debit": total_debit,
                "total_credit": total_credit,
                # New columns (None for the document row)
                "txn_date": None,
                "bank_account_txn": None,
                "allocated_amount": None,
                "deposit": None,
                "withdrawal": None,
                "indent": 0
            }
            data.append(base_row)

            # Child rows for items (indent=1)
            if item_table:
                if doctype == "Journal Entry":
                    child_fields = ["account", "debit_in_account_currency", "credit_in_account_currency"]
                else:
                    child_fields = ["item_code", "rate", "amount"]

                items = frappe.get_all(
                    item_table,
                    filters={"parent": name},
                    fields=child_fields
                )

                for item in items:
                    child_row = {
                        "doctype": doctype,
                        "doc_name": f"Item: {item.get('item_code') or item.get('account')}",
                        "grand_total": None,
                        "rounded_total": None,
                        "outstanding_amount": None,
                        "rate": item.get("rate") if doctype != "Journal Entry" else None,
                        "amount": item.get("amount") if doctype != "Journal Entry" else None,
                        "account": item.get("account") if doctype == "Journal Entry" else None,
                        "debit": item.get("debit_in_account_currency") if doctype == "Journal Entry" else None,
                        "credit": item.get("credit_in_account_currency") if doctype == "Journal Entry" else None,
                        "total_debit": None,
                        "total_credit": None,
                        # New columns (None for item rows)
                        "txn_date": None,
                        "bank_account_txn": None,
                        "allocated_amount": None,
                        "deposit": None,
                        "withdrawal": None,
                        "indent": 1
                    }
                    data.append(child_row)

            # **New**: Fetch Bank Transactions linked to this Journal Entry
            # if doctype == "Journal Entry":
            #     txns = frappe.get_all(
            #         "Bank Transaction",
            #         filters={"reference_doctype": "Journal Entry", "reference_name": name},
            #         fields=["date", "bank_account", "allocated_amount", "deposit", "withdrawal"]
            #     )
            #     for txn in txns:
            #         data.append({
            #             "doctype": "Bank Transaction",
            #             "doc_name": f"Transaction: {txn.get('date')} on {txn.get('bank_account')}",
            #             "grand_total": None,
            #             "rounded_total": None,
            #             "outstanding_amount": None,
            #             "rate": None,
            #             "amount": None,
            #             "account": None,
            #             "debit": None,
            #             "credit": None,
            #             "total_debit": None,
            #             "total_credit": None,
            #             # Populate new Bank Transaction columns
            #             "txn_date": txn.get("date"),
            #             "bank_account_txn": txn.get("bank_account"),
            #             "allocated_amount": txn.get("allocated_amount"),
            #             "deposit": txn.get("deposit"),
            #             "withdrawal": txn.get("withdrawal"),
            #             "indent": 1
            #         })
            # Safe Bank Transaction fetch (only if required fields exist)
            # bank_txn_meta = frappe.get_meta("Bank Transaction")
            # bank_txn_fields = [df.fieldname for df in bank_txn_meta.fields]

            # if "reference_doctype" in bank_txn_fields and "reference_name" in bank_txn_fields:
            #     txns = frappe.get_all(
            #         "Bank Transaction",
            #         filters={"reference_doctype": "Journal Entry", "reference_name": name},
            #         fields=["date", "bank_account", "allocated_amount", "deposit", "withdrawal"],
            #         ignore_permissions=True
            # )
            # for txn in txns:
            #     data.append({
            #         "doctype": "Bank Transaction",
            #         "doc_name": f"Transaction: {txn.get('date')} on {txn.get('bank_account')}",
            #         "grand_total": None,
            #         "rounded_total": None,
            #         "outstanding_amount": None,
            #         "rate": None,
            #         "amount": None,
            #         "account": None,
            #         "debit": None,
            #         "credit": None,
            #         "total_debit": None,
            #         "total_credit": None,
            #         # Populate new Bank Transaction columns
            #         "txn_date": txn.get("date"),
            #         "bank_account_txn": txn.get("bank_account"),
            #         "allocated_amount": txn.get("allocated_amount"),
            #         "deposit": txn.get("deposit"),
            #         "withdrawal": txn.get("withdrawal"),
            #         "indent": 1
            #     })
            # else:
            #    frappe.logger().info("Bank Transaction does not have reference_doctype/reference_name fields.")

            # Safe Bank Transaction fetch (only if required fields exist)
                bank_txn_meta = frappe.get_meta("Bank Transaction")
                bank_txn_fields = [df.fieldname for df in bank_txn_meta.fields]

            if "reference_doctype" in bank_txn_fields and "reference_name" in bank_txn_fields:
                txns = frappe.get_all(
                        "Bank Transaction",
                        filters={"reference_doctype": "Journal Entry", "reference_name": name},
                        fields=["date", "bank_account", "allocated_amount", "deposit", "withdrawal"],
                        ignore_permissions=True
                    )
                    
                for txn in txns:
                        data.append({
                            "doctype": "Bank Transaction",
                            "doc_name": f"Transaction: {txn.get('date')} on {txn.get('bank_account')}",
                            "grand_total": None,
                            "rounded_total": None,
                            "outstanding_amount": None,
                            "rate": None,
                            "amount": None,
                            "account": None,
                            "debit": None,
                            "credit": None,
                            "total_debit": None,
                            "total_credit": None,
                            "txn_date": txn.get("date"),
                            "bank_account_txn": txn.get("bank_account"),
                            "allocated_amount": txn.get("allocated_amount"),
                            "deposit": txn.get("deposit"),
                            "withdrawal": txn.get("withdrawal"),
                            "indent": 1
                        })
            else:
                # No required fields, so no txns to process
                txns = []

    

            # Existing Payment Entry logic for invoices remains unchanged
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
                        "account": None,
                        "debit": None,
                        "credit": None,
                        "total_debit": None,
                        "total_credit": None,
                        # New columns (None for payment entry rows)
                        "txn_date": None,
                        "bank_account_txn": None,
                        "allocated_amount": None,
                        "deposit": None,
                        "withdrawal": None,
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







