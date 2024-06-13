import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    summary = get_summary()
    data.extend(summary)
    return columns, data

def get_columns():
    return [
        {"label": _("Project Name"), "fieldname": "project_name", "fieldtype": "Data", "width": 150},
        {"label": _("Project Manager"), "fieldname": "project_manager", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 100},
        {"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 100},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Budget"), "fieldname": "budget", "fieldtype": "Currency", "width": 100},
        {"label": _("Budget Utilization"), "fieldname": "budget_utilization", "fieldtype": "Percent", "width": 100}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("status"):
        conditions += " AND status = %(status)s"
    
    data = frappe.db.sql("""
        SELECT 
            project_name, project_manager, start_date, end_date, status, budget, budget_utilization
        FROM
            `tabProject`
        WHERE
            1=1 {conditions}
    """.format(conditions=conditions), filters, as_dict=1)

    return data

def get_summary():
    ongoing_projects = frappe.db.count('Project', filters={'status': 'Execution'})
    completed_projects = frappe.db.count('Project', filters={'status': 'Closure', 'end_date': ['between', [frappe.utils.add_months(frappe.utils.nowdate(), -3), frappe.utils.nowdate()]]})
    budget_utilization = frappe.db.sql("""
        SELECT
            project_name, budget, budget_utilization
        FROM
            `tabProject`
    """, as_dict=1)

    return [
        {"label": _("Ongoing Projects"), "fieldname": "ongoing_projects", "fieldtype": "Data", "value": ongoing_projects},
        {"label": _("Completed Projects (Last Quarter)"), "fieldname": "completed_projects", "fieldtype": "Data", "value": completed_projects},
        {"label": _("Budget Utilization"), "fieldname": "budget_utilization", "fieldtype": "Data", "value": budget_utilization}
    ]



