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
#         # New columns for Bank Transaction details
#         {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
#         {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
#         {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Reference Number", "fieldname": "cheque_no", "fieldtype": "Data", "width": 150},
#         {"label": "Reference Date", "fieldname": "cheque_date", "fieldtype": "Date", "width": 120}

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

#             # Base row for the document (indent=0)
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
#                 # New columns (None for the document row)
#                 "txn_date": None,
#                 "bank_account_txn": None,
#                 "allocated_amount": None,
#                 "deposit": None,
#                 "withdrawal": None,
#                 "indent": 0
#             }
#             data.append(base_row)

#             # Child rows for items (indent=1)
#             if item_table:
#                 if doctype == "Journal Entry":
#                     child_fields = ["account", "debit_in_account_currency", "credit_in_account_currency"]

#                     cheque_data = frappe.get_value("Journal Entry", name, ["cheque_no", "cheque_date"], as_dict=True)
#                     cheque_no = cheque_data.cheque_no if cheque_data else None
#                     cheque_date = cheque_data.cheque_date if cheque_data else None
#                 else:
#                     child_fields = ["item_code", "rate", "amount"]
#                     cheque_no = None
#                     cheque_date = None

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
#                         # New columns (None for item rows)
#                         "txn_date": None,
#                         "bank_account_txn": None,
#                         "allocated_amount": None,
#                         "deposit": None,
#                         "withdrawal": None,
#                         "cheque_no": cheque_no,
#                         "cheque_date": cheque_date,
#                         "indent": 1
#                     }
#                     data.append(child_row)

#                 bank_txn_meta = frappe.get_meta("Bank Transaction")
#                 bank_txn_fields = [df.fieldname for df in bank_txn_meta.fields]

#             if "reference_doctype" in bank_txn_fields and "reference_name" in bank_txn_fields:
#                 txns = frappe.get_all(
#                         "Bank Transaction",
#                         filters={"reference_doctype": "Journal Entry", "reference_name": name},
#                         fields=["date", "bank_account", "allocated_amount", "deposit", "withdrawal"],
#                         ignore_permissions=True
#                     )
                    
#                 for txn in txns:
#                         data.append({
#                             "doctype": "Bank Transaction",
#                             "doc_name": f"Transaction: {txn.get('date')} on {txn.get('bank_account')}",
#                             "grand_total": None,
#                             "rounded_total": None,
#                             "outstanding_amount": None,
#                             "rate": None,
#                             "amount": None,
#                             "account": None,
#                             "debit": None,
#                             "credit": None,
#                             "total_debit": None,
#                             "total_credit": None,
#                             "txn_date": txn.get("date"),
#                             "bank_account_txn": txn.get("bank_account"),
#                             "allocated_amount": txn.get("allocated_amount"),
#                             "deposit": txn.get("deposit"),
#                             "withdrawal": txn.get("withdrawal"),
#                             "indent": 1
#                         })
#             else:
#                 # No required fields, so no txns to process
#                 txns = []

    

#             # Existing Payment Entry logic for invoices remains unchanged
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
#                         # New columns (None for payment entry rows)
#                         "txn_date": None,
#                         "bank_account_txn": None,
#                         "allocated_amount": None,
#                         "deposit": None,
#                         "withdrawal": None,
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
#         {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
#         {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
#         {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Reference Number", "fieldname": "cheque_no", "fieldtype": "Data", "width": 150},
#         {"label": "Reference Date", "fieldname": "cheque_date", "fieldtype": "Date", "width": 120}
#     ]

#     data = []
#     doc_totals = {}

#     bank_txn_meta_fields = [f.fieldname for f in frappe.get_meta("Bank Transaction").fields]
#     has_ref_fields = "reference_doctype" in bank_txn_meta_fields and "reference_name" in bank_txn_meta_fields

#     bank_txn_fields = ["date", "bank_account", "allocated_amount", "deposit", "withdrawal", "reference_number"]
#     if "reference_date" in bank_txn_meta_fields:
#         bank_txn_fields.append("reference_date")

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

#         records = frappe.get_all(doctype, filters=filters_dict, fields=fields, ignore_permissions=True)

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
#                 "txn_date": None,
#                 "bank_account_txn": None,
#                 "allocated_amount": None,
#                 "deposit": None,
#                 "withdrawal": None,
#                 "cheque_no": None,
#                 "cheque_date": None,
#                 "indent": 0
#             }
#             data.append(base_row)

#             if item_table:
#                 child_fields = ["item_code", "rate", "amount"]
#                 if doctype == "Journal Entry":
#                     child_fields = ["account", "debit_in_account_currency", "credit_in_account_currency"]
#                     cheque_data = frappe.get_value("Journal Entry", name, ["cheque_no", "cheque_date"], as_dict=True)
#                     cheque_no = cheque_data.cheque_no if cheque_data else None
#                     cheque_date = cheque_data.cheque_date if cheque_data else None
#                 else:
#                     cheque_no = cheque_date = None

#                 items = frappe.get_all(item_table, filters={"parent": name}, fields=child_fields)

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
#                         "txn_date": None,
#                         "bank_account_txn": None,
#                         "allocated_amount": None,
#                         "deposit": None,
#                         "withdrawal": None,
#                         "cheque_no": cheque_no,
#                         "cheque_date": cheque_date,
#                         "indent": 1
#                     }
#                     data.append(child_row)

#             if doctype == "Purchase Receipt":
#                 invoices = frappe.get_all("Purchase Invoice Item", filters={"purchase_receipt": name}, fields=["parent"])
#                 for inv in invoices:
#                     txn_filters = {"docstatus": 1}
#                     if has_ref_fields:
#                         txn_filters["reference_doctype"] = "Purchase Invoice"
#                         txn_filters["reference_name"] = inv.parent
#                     txns = frappe.get_all("Bank Transaction", filters=txn_filters, fields=bank_txn_fields)
#                     for txn in txns:
#                         data.append({
#                             "doctype": "Bank Transaction",
#                             "doc_name": f"Transaction: {txn.date} on {txn.bank_account}",
#                             "txn_date": txn.date,
#                             "bank_account_txn": txn.bank_account,
#                             "allocated_amount": txn.allocated_amount,
#                             "deposit": txn.deposit,
#                             "withdrawal": txn.withdrawal,
#                             "cheque_no": txn.reference_number,
#                             "cheque_date": getattr(txn, "reference_date", None),
#                             "indent": 1
#                         })

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

# def get_gl_entries_by_voucher():
#     gl_entries = frappe.get_all(
#         "GL Entry",
#         fields=["voucher_type", "voucher_no", "account", "debit", "credit", "name"],
#         filters={"docstatus": 1},
#         order_by="posting_date asc"
#     )

#     gl_map = {}
#     for entry in gl_entries:
#         key = (entry.voucher_type, entry.voucher_no)
#         if key not in gl_map:
#             gl_map[key] = []
#         gl_map[key].append(entry)

#     return gl_map

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
#         {"label": "GL Entry", "fieldname": "gl_entry", "fieldtype": "Data", "width": 250},
#         {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
#         {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
#         {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Reference Number", "fieldname": "cheque_no", "fieldtype": "Data", "width": 150},
#         {"label": "Reference Date", "fieldname": "cheque_date", "fieldtype": "Date", "width": 120}
#     ]

#     data = []
#     doc_totals = {}
#     gl_map = get_gl_entries_by_voucher()

#     bank_txn_meta_fields = [f.fieldname for f in frappe.get_meta("Bank Transaction").fields]
#     has_ref_fields = "reference_doctype" in bank_txn_meta_fields and "reference_name" in bank_txn_meta_fields

#     bank_txn_fields = ["date", "bank_account", "allocated_amount", "deposit", "withdrawal", "reference_number"]
#     if "reference_date" in bank_txn_meta_fields:
#         bank_txn_fields.append("reference_date")

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

#         records = frappe.get_all(doctype, filters=filters_dict, fields=fields, ignore_permissions=True)

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
#                 "gl_entry": None,
#                 "txn_date": None,
#                 "bank_account_txn": None,
#                 "allocated_amount": None,
#                 "deposit": None,
#                 "withdrawal": None,
#                 "cheque_no": None,
#                 "cheque_date": None,
#                 "indent": 0
#             }
#             data.append(base_row)

#             # Append GL Entries
#             for gle in gl_map.get((doctype, name), []):
#                 data.append({
#                     "doctype": doctype,
#                     "doc_name": f"GL Entry: {gle.account}",
#                     "account": gle.account,
#                     "debit": gle.debit,
#                     "credit": gle.credit,
#                     "gl_entry": get_link_to_form("GL Entry", gle.name),
#                     "indent": 1
#                 })

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

# def get_gl_entries_by_voucher(company=None):
#     gl_filters = {"docstatus": 1}
#     if company:
#         gl_filters["company"] = company

#     gl_entries = frappe.get_all(
#         "GL Entry",
#         fields=["voucher_type", "voucher_no", "account", "debit", "credit", "name", "company", "transaction_currency"],
#         filters=gl_filters,
#         order_by="posting_date asc"
#     )

#     gl_map = {}
#     for entry in gl_entries:
#         key = (entry.voucher_type, entry.voucher_no)
#         gl_map.setdefault(key, []).append(entry)
#     return gl_map

# def execute(filters=None):
#     filters = filters or {}
#     company_filter = filters.get("company")

#     doctype_filter = set()
#     if filters.get("doctype_filter"):
#         raw = filters["doctype_filter"]
#         if isinstance(raw, list):
#             doctype_filter = set([d for d in raw if d])
#         else:
#             doctype_filter = set(d.strip() for d in raw.replace("\n", ",").split(",") if d.strip())

#     gl_map = get_gl_entries_by_voucher(company_filter)

#     columns = [
#         {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
#         {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Data", "width": 300, "filterable": 1,"in_standard_filter": 1},
#         {"label": "Reference Doc", "fieldname": "reference_doc", "fieldtype": "Data", "width": 250},


#         {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "currency", "width": 100},
#         {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},

#         {"label": "GL Entry", "fieldname": "gl_entry", "fieldtype": "Data", "width": 250},

#          {"label": "Currency", "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 100},

#         {"label": "Exchange Rate", "fieldname": "exchange_rate", "fieldtype": "Float", "width": 100},
       

#         {"label": "Amount (Currency)", "fieldname": "amount_currency", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Amount (Local)", "fieldname": "amount_local", "fieldtype": "Currency","options": "currency", "width": 120},
#         {"label": "Amount (Reporting)", "fieldname": "amount_reporting", "fieldtype": "Currency","options": "currency", "width": 120},
#         {"label": "Amount (Transaction)", "fieldname": "amount_transaction", "fieldtype": "Currency","options": "currency", "width": 120},
#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 180},
#         {"label": "Account Effect", "fieldname": "account_effect", "fieldtype": "Data", "width": 120},


#         {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
#         {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
#         {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "currency", "width": 120},
#         {"label": "Reference Number", "fieldname": "cheque_no", "fieldtype": "Data", "width": 150},
#         {"label": "Reference Date", "fieldname": "cheque_date", "fieldtype": "Date", "width": 120},

#         # NEW CURRENCY COLUMNS
       
#     ]

#     data = []
#     doc_totals = {}
#     gl_map = get_gl_entries_by_voucher()

#     bank_txn_meta_fields = [f.fieldname for f in frappe.get_meta("Bank Transaction").fields]
#     has_ref_fields = "reference_doctype" in bank_txn_meta_fields and "reference_name" in bank_txn_meta_fields

#     bank_txn_fields = ["date", "bank_account", "allocated_amount", "deposit", "withdrawal", "reference_number"]
#     if "reference_date" in bank_txn_meta_fields:
#         bank_txn_fields.append("reference_date")

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

#         if doctype_filter and doctype not in doctype_filter:
#             continue

#         try:
#             meta = frappe.get_meta(doctype)
#         except frappe.DoesNotExistError:
#             continue

#         available_fields = [df.fieldname for df in meta.fields]
#         fields = ["name"]
#         if "company" in available_fields:
#             fields.append("company")
#         if "grand_total" in available_fields:
#             fields.append("grand_total")
#         if "rounded_total" in available_fields:
#             fields.append("rounded_total")
#         if "outstanding_amount" in available_fields:
#             fields.append("outstanding_amount")
#         if "currency" in available_fields:
#             fields.append("currency")
#         if "conversion_rate" in available_fields:
#             fields.append("conversion_rate")
#         if "transaction_date" in available_fields:
#             fields.append("transaction_date")
#         if doctype == "Journal Entry":
#             fields += ["total_debit", "total_credit"]
#         # if doctype == "Sales Order":
#         #     fields += ["currency", "selling_price_list", "transaction_date"]
#         if doctype in ["Sales Order", "Purchase Order"]:
#             fields += ["currency", "conversion_rate", "transaction_date"]
#         if doctype == "Sales Order":
#             fields.append("selling_price_list")


#         doc_totals[doctype] = 0.0

#         date_filter_field = "posting_date" if "posting_date" in available_fields else "transaction_date" if "transaction_date" in available_fields else None
#         filters_dict = {"docstatus": 1}
#         if "company" in available_fields and company_filter:
#             filters_dict["company"] = company_filter
#         if date_filter_field and filters and filters.get("from_date") and filters.get("to_date"):
#             filters_dict[date_filter_field] = ["between", [filters["from_date"], filters["to_date"]]]

#         records = frappe.get_all(doctype, filters=filters_dict, fields=fields, ignore_permissions=True)

#         for rec in records:
#             name = rec.get("name")
#             grand_total = rec.get("grand_total")
#             rounded_total = rec.get("rounded_total")
#             outstanding = rec.get("outstanding_amount")
#             total_debit = rec.get("total_debit")
#             total_credit = rec.get("total_credit")

#             currency = rec.get("currency") 

#             if not currency:
#                 currency = frappe.get_cached_value('Company', frappe.db.get_default('company'), 'default_currency')


#             selling_price_list = rec.get("selling_price_list") if doctype == "Sales Order" else None
#             txn_date = rec.get("transaction_date") if doctype == "Sales Order" else None

#             exchange_rate = None
       

#             amount_currency = grand_total or 0
#             if doctype in ["Sales Order", "Purchase Order"]:
#                 exchange_rate = rec.get("conversion_rate") or 1
#             else:
#                 exchange_rate = 1

#             if currency and currency != "INR":
#                 # Show foreign currency amounts as-is
#                 amount_local = amount_currency
#                 amount_reporting = amount_currency
#                 amount_transaction = amount_currency
#             else:
#                 # Convert to INR
#                 amount_local = amount_currency * exchange_rate
#                 amount_reporting = amount_local
#                 amount_transaction = amount_local

#             if grand_total:
#                 doc_totals[doctype] += grand_total
#             elif total_debit:
#                 doc_totals[doctype] += total_debit   


#             reference_doc = None

#             if doctype in ["Sales Invoice", "Purchase Invoice", "Purchase Receipt", "Delivery Note"]:
#                 child_table = {
#                     "Sales Invoice": ("Sales Invoice Item", "sales_order"),
#                     "Purchase Invoice": ("Purchase Invoice Item", "purchase_order"),
#                     "Purchase Receipt": ("Purchase Receipt Item", "sales_order"),
#                     "Delivery Note": ("Delivery Note Item", "against_sales_order")
#                 }

#                 item_table, reference_field = child_table[doctype]
#                 references = frappe.get_all(item_table, filters={"parent": name}, fields=[reference_field])
                
#                 # Collect non-empty unique references
#                 ref_set = set([r[reference_field] for r in references if r.get(reference_field)])
#                 reference_doc = ", ".join(ref_set) if ref_set else None
    
#             company_name = rec.get("company") if "company" in rec else frappe.db.get_default('company')

#             account_effect_flag = "Yes" if gl_map.get((doctype, name)) else "No"
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
#                 "gl_entry": None,
#                 "txn_date": txn_date,
#                 "bank_account_txn": None,
#                 "allocated_amount": None,
#                 "deposit": None,
#                 "withdrawal": None,
#                 "cheque_no": None,
#                 "cheque_date": None,
#                 "currency": currency,
#                 "selling_price_list": selling_price_list,
#                 "exchange_rate": exchange_rate,
#                 "amount_currency": amount_currency,
#                 "amount_local": amount_local,
#                 "amount_reporting": amount_reporting,
#                 "amount_transaction": amount_transaction,
#                  "company": company_name,
#                 "account_effect": account_effect_flag,
#                 "reference_doc": reference_doc,
#                 "indent": 0
#             }
#             data.append(base_row)

    
#             for gle in gl_map.get((doctype, name), []):
#                 sign = ""
#                 if gle.debit and gle.debit > 0:
#                     sign = "+"
#                 elif gle.credit and gle.credit > 0:
#                     sign = "-"

#                 # Use grand_total if available, else use debit or credit as fallback
#                 base_amount = gle.debit if gle.debit > 0 else gle.credit or 0

#                 # Sign-prefixed amounts
#                 signed_amount = float(f"{sign}{base_amount}") if sign else base_amount

#                 data.append({
#                     "doctype": doctype,
#                     "doc_name": f"GL Entry: {gle.account}",
#                     "account": gle.account,
#                     "debit": gle.debit,
#                     "credit": gle.credit,
#                     "gl_entry": get_link_to_form("GL Entry", gle.name),
#                     "amount_currency": signed_amount,
#                     "amount_local": signed_amount,
#                     "amount_reporting": signed_amount,
#                     "amount_transaction": signed_amount,
#                     "company": gle.company if hasattr(gle, "company") else company_name,
#                     "account_effect": "Yes",
#                     "currency": gle.transaction_currency,
#                     "indent": 1
#                 })


#             # Fetch Payment Entries linked to this document
#             payment_refs = frappe.get_all("Payment Entry Reference",
#                 fields=["parent"],
#                 filters={
#                     "reference_doctype": doctype,
#                     "reference_name": name,
#                     "docstatus": 1
#                 }
#             )

#             for pref in payment_refs:
#                 payment_entry = frappe.get_doc("Payment Entry", pref.parent)
#                 if company_filter and payment_entry.company != company_filter:
#                     continue

#                 if doctype_filter and doctype not in doctype_filter:
#                     continue
#                 data.append({
#                     "doctype": "Payment Entry",
#                     "doc_name": f"Payment Entry: {payment_entry.name}",
#                     "reference_doc": name,  # Add Reference Doc column
#                     "grand_total": payment_entry.paid_amount,
#                     "account": payment_entry.paid_from if payment_entry.payment_type == "Receive" else payment_entry.paid_to,
#                     "amount_currency": payment_entry.paid_amount,
#                     "txn_date": payment_entry.posting_date,
#                     "cheque_no": payment_entry.reference_no,
#                     "cheque_date": payment_entry.reference_date,
#                     "company": payment_entry.company,
#                     "account_effect": "Yes",     
#                     "indent": 1
#                 })    

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
from frappe.utils import get_link_to_form, getdate, flt

# --- FX helper: convert any currency to INR on/before a given date ---
from frappe.utils import getdate, flt

def get_rate_to_inr(from_currency: str, on_date=None) -> float:
    """Return FX rate to INR (latest <= date). Tries ERPNext util, then direct and reverse CE rows."""
    if not from_currency or from_currency == "INR":
        return 1.0

    date = getdate(on_date) if on_date else getdate()

    # 1) Prefer ERPNext's resolver (handles reverse pairs & provider hooks)
    try:
        from erpnext.setup.utils import get_exchange_rate as erp_get_rate
        r = flt(erp_get_rate(from_currency, "INR", date))
        if r:
            return r
        r_rev = flt(erp_get_rate("INR", from_currency, date))
        if r_rev:
            return 1.0 / r_rev
    except Exception:
        pass

    # 2) Fallback: direct Currency Exchange row
    rate = frappe.db.get_value(
        "Currency Exchange",
        {"from_currency": from_currency, "to_currency": "INR", "date": ["<=", date]},
        "exchange_rate",
        order_by="date desc",
    )
    if rate:
        return flt(rate)

    # 3) Fallback: reverse Currency Exchange row (INR -> foreign)
    rev = frappe.db.get_value(
        "Currency Exchange",
        {"from_currency": "INR", "to_currency": from_currency, "date": ["<=", date]},
        "exchange_rate",
        order_by="date desc",
    )
    if rev:
        return 1.0 / flt(rev)

    # 4) Last resort
    return 1.0



def get_gl_entries_by_voucher(company=None):
    gl_filters = {"docstatus": 1}
    if company:
        gl_filters["company"] = company

    gl_entries = frappe.get_all(
        "GL Entry",
        fields=[
            "voucher_type",
            "voucher_no",
            "account",
            "debit",
            "credit",
            "name",
            "company",
            "transaction_currency",
            "posting_date",
        ],
        filters=gl_filters,
        order_by="posting_date asc",
    )

    gl_map = {}
    for entry in gl_entries:
        key = (entry.voucher_type, entry.voucher_no)
        gl_map.setdefault(key, []).append(entry)
    return gl_map


def execute(filters=None):
    filters = filters or {}
    company_filter = filters.get("company")

    # parse optional doctype filter
    doctype_filter = set()
    if filters.get("doctype_filter"):
        raw = filters["doctype_filter"]
        if isinstance(raw, list):
            doctype_filter = set([d for d in raw if d])
        else:
            doctype_filter = set(
                d.strip() for d in raw.replace("\n", ",").split(",") if d.strip()
            )

    gl_map = get_gl_entries_by_voucher(company_filter)

    columns = [
        {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
        {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Data", "width": 300, "filterable": 1, "in_standard_filter": 1},
        {"label": "Reference Doc", "fieldname": "reference_doc", "fieldtype": "Data", "width": 250},

        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "currency", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},

        {"label": "GL Entry", "fieldname": "gl_entry", "fieldtype": "Data", "width": 250},

        {"label": "Currency", "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 100},
        {"label": "Exchange Rate", "fieldname": "exchange_rate", "fieldtype": "Float", "width": 100},

        {"label": "Amount (Currency)", "fieldname": "amount_currency", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Amount (Local)", "fieldname": "amount_local", "fieldtype": "Currency", "options": "currency", "width": 120},
        # Force INR formatting for reporting column:
        {"label": "Amount (Reporting)", "fieldname": "amount_reporting", "fieldtype": "Currency", "options": "INR", "width": 120},
        {"label": "Amount (Transaction)", "fieldname": "amount_transaction", "fieldtype": "Currency", "options": "currency", "width": 120},

        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 180},
        {"label": "Account Effect", "fieldname": "account_effect", "fieldtype": "Data", "width": 120},

        {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
        {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
        {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": "Reference Number", "fieldname": "cheque_no", "fieldtype": "Data", "width": 150},
        {"label": "Reference Date", "fieldname": "cheque_date", "fieldtype": "Date", "width": 120},
    ]

    data = []
    doc_totals = {}

    bank_txn_meta_fields = [f.fieldname for f in frappe.get_meta("Bank Transaction").fields]
    has_ref_fields = "reference_doctype" in bank_txn_meta_fields and "reference_name" in bank_txn_meta_fields

    bank_txn_fields = ["date", "bank_account", "allocated_amount", "deposit", "withdrawal", "reference_number"]
    if "reference_date" in bank_txn_meta_fields:
        bank_txn_fields.append("reference_date")

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

        if doctype_filter and doctype not in doctype_filter:
            continue

        try:
            meta = frappe.get_meta(doctype)
        except frappe.DoesNotExistError:
            continue

        available_fields = [df.fieldname for df in meta.fields]
        fields = ["name"]

        # include company and monetary fields when present
        if "company" in available_fields:
            fields.append("company")
        if "grand_total" in available_fields:
            fields.append("grand_total")
        if "rounded_total" in available_fields:
            fields.append("rounded_total")
        if "outstanding_amount" in available_fields:
            fields.append("outstanding_amount")
        if "currency" in available_fields:
            fields.append("currency")
        if "conversion_rate" in available_fields:
            fields.append("conversion_rate")

        # include a suitable date field and remember which one
        date_field = None
        if "posting_date" in available_fields:
            date_field = "posting_date"
        elif "transaction_date" in available_fields:
            date_field = "transaction_date"
        if date_field and date_field not in fields:
            fields.append(date_field)

        if doctype == "Journal Entry":
            fields += ["total_debit", "total_credit"]
        if doctype in ["Sales Order", "Purchase Order"]:
            if "transaction_date" not in fields and "transaction_date" in available_fields:
                fields.append("transaction_date")
            if "currency" not in fields and "currency" in available_fields:
                fields.append("currency")
            if "conversion_rate" not in fields and "conversion_rate" in available_fields:
                fields.append("conversion_rate")
        if doctype == "Sales Order":
            if "selling_price_list" in available_fields:
                fields.append("selling_price_list")

        doc_totals[doctype] = 0.0

        # filters
        filters_dict = {"docstatus": 1}
        if "company" in available_fields and company_filter:
            filters_dict["company"] = company_filter
        if date_field and filters and filters.get("from_date") and filters.get("to_date"):
            filters_dict[date_field] = ["between", [filters["from_date"], filters["to_date"]]]

        records = frappe.get_all(doctype, filters=filters_dict, fields=fields, ignore_permissions=True)

        for rec in records:
            name = rec.get("name")
            grand_total = rec.get("grand_total")
            rounded_total = rec.get("rounded_total")
            outstanding = rec.get("outstanding_amount")
            total_debit = rec.get("total_debit")
            total_credit = rec.get("total_credit")
            currency = rec.get("currency")
            if not currency:
                # fallback to default company currency
                default_company = rec.get("company") or frappe.db.get_default("company")
                currency = frappe.get_cached_value("Company", default_company, "default_currency") if default_company else "INR"

            selling_price_list = rec.get("selling_price_list") if doctype == "Sales Order" else None

            # Decide document date for FX
            doc_date = rec.get(date_field) if date_field else None
            txn_date = rec.get("transaction_date") if "transaction_date" in rec else (rec.get("posting_date") if "posting_date" in rec else None)

            # Base amounts in document currency
            amount_currency = grand_total or 0.0

            # Reporting (INR) conversion
            rate_to_inr = get_rate_to_inr(currency, doc_date)
            amount_reporting = amount_currency * rate_to_inr  # ALWAYS INR

            # Keep your previous semantics for local/transaction if you like
            if doctype in ["Sales Order", "Purchase Order"]:
                exchange_rate = rec.get("conversion_rate") or 1
            else:
                exchange_rate = 1

            amount_local = amount_currency * (exchange_rate or 1)
            amount_transaction = amount_currency

            if grand_total:
                doc_totals[doctype] += grand_total
            elif total_debit:
                doc_totals[doctype] += total_debit

            # Build reference_doc from child tables where applicable
            reference_doc = None
            if doctype in ["Sales Invoice", "Purchase Invoice", "Purchase Receipt", "Delivery Note"]:
                child_table = {
                    "Sales Invoice": ("Sales Invoice Item", "sales_order"),
                    "Purchase Invoice": ("Purchase Invoice Item", "purchase_order"),
                    "Purchase Receipt": ("Purchase Receipt Item", "sales_order"),
                    "Delivery Note": ("Delivery Note Item", "against_sales_order"),
                }
                item_table, reference_field = child_table[doctype]
                references = frappe.get_all(item_table, filters={"parent": name}, fields=[reference_field])
                ref_set = set([r[reference_field] for r in references if r.get(reference_field)])
                reference_doc = ", ".join(ref_set) if ref_set else None

            company_name = rec.get("company") if "company" in rec else frappe.db.get_default("company")

            account_effect_flag = "Yes" if gl_map.get((doctype, name)) else "No"
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
                "gl_entry": None,
                "txn_date": txn_date,
                "bank_account_txn": None,
                "allocated_amount": None,
                "deposit": None,
                "withdrawal": None,
                "cheque_no": None,
                "cheque_date": None,
                "currency": currency,
                "selling_price_list": selling_price_list,
                "exchange_rate": exchange_rate,
                "amount_currency": amount_currency,
                "amount_local": amount_local,
                "amount_reporting": amount_reporting,      # <-- INR
                "amount_transaction": amount_transaction,
                "company": company_name,
                "account_effect": account_effect_flag,
                "reference_doc": reference_doc,
                "indent": 0,
            }
            data.append(base_row)

            # --- GL Entry detail lines (convert to INR from company base currency) ---
            for gle in gl_map.get((doctype, name), []):
                # Determine signed amount (+debit or -credit)
                if gle.debit and gle.debit > 0:
                    signed_amount = gle.debit
                elif gle.credit and gle.credit > 0:
                    signed_amount = -gle.credit
                else:
                    signed_amount = 0.0

                # GL is recorded in company currency (base); convert that base to INR
                gl_company = gle.company if hasattr(gle, "company") and gle.company else company_name
                company_currency = frappe.get_cached_value("Company", gl_company, "default_currency") if gl_company else "INR"
                rate_to_inr_gl = get_rate_to_inr(company_currency, gle.posting_date)
                amount_reporting_gl = signed_amount * rate_to_inr_gl  # ALWAYS INR

                data.append({
                    "doctype": doctype,
                    "doc_name": f"GL Entry: {gle.account}",
                    "account": gle.account,
                    "debit": gle.debit,
                    "credit": gle.credit,
                    "gl_entry": get_link_to_form("GL Entry", gle.name),
                    "amount_currency": signed_amount,
                    "amount_local": signed_amount,
                    "amount_reporting": amount_reporting_gl,   # <-- INR
                    "amount_transaction": signed_amount,
                    "company": gl_company,
                    "account_effect": "Yes",
                    "currency": company_currency,
                    "indent": 1,
                })

            # --- Payment Entries linked to this document (convert to INR) ---
            payment_refs = frappe.get_all(
                "Payment Entry Reference",
                fields=["parent"],
                filters={"reference_doctype": doctype, "reference_name": name, "docstatus": 1},
            )

            for pref in payment_refs:
                payment_entry = frappe.get_doc("Payment Entry", pref.parent)
                if company_filter and payment_entry.company != company_filter:
                    continue
                if doctype_filter and doctype not in doctype_filter:
                    continue

                pe_company_cur = frappe.get_cached_value("Company", payment_entry.company, "default_currency")
                pe_rate_to_inr = get_rate_to_inr(pe_company_cur, payment_entry.posting_date)
                amount_reporting_pe = (payment_entry.paid_amount or 0.0) * pe_rate_to_inr  # INR

                data.append({
                    "doctype": "Payment Entry",
                    "doc_name": f"Payment Entry: {payment_entry.name}",
                    "reference_doc": name,
                    "grand_total": payment_entry.paid_amount,
                    "account": payment_entry.paid_from if payment_entry.payment_type == "Receive" else payment_entry.paid_to,
                    "amount_currency": payment_entry.paid_amount,
                    "amount_local": payment_entry.paid_amount,
                    "amount_reporting": amount_reporting_pe,  # <-- INR
                    "amount_transaction": payment_entry.paid_amount,
                    "txn_date": payment_entry.posting_date,
                    "cheque_no": payment_entry.reference_no,
                    "cheque_date": payment_entry.reference_date,
                    "company": payment_entry.company,
                    "account_effect": "Yes",
                    "indent": 1,
                })

    chart = {
        "data": {
            "labels": list(doc_totals.keys()),
            "datasets": [{"values": list(doc_totals.values())}],
        },
        "type": "pie",
        "height": 300,
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

