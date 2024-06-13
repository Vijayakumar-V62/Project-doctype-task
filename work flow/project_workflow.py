import frappe

def setup_workflow():
    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": "Project Workflow",
        "document_type": "Project",
        "is_active": 1,
        "states": [
            {"state": "Planning", "doc_status": 0, "allow_edit": "Project Coordinator"},
            {"state": "Execution", "doc_status": 1, "allow_edit": "Project Coordinator"},
            {"state": "Closure", "doc_status": 2, "allow_edit": "Project Coordinator"},
        ],
        "transitions": [
            {"state": "Planning", "action": "Start Execution", "next_state": "Execution", "allow": "Project Coordinator"},
            {"state": "Execution", "action": "Close Project", "next_state": "Closure", "allow": "Project Coordinator"},
        ],
        "permissions": [
            {"role": "Project Coordinator", "state": "Planning"},
            {"role": "Project Coordinator", "state": "Execution"},
        ],
    })
    workflow.insert(ignore_permissions=True)

setup_workflow()


