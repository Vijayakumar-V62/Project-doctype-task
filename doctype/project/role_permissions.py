import frappe

def setup_role_permissions():
    role = frappe.get_doc({
        "doctype": "Role",
        "role_name": "Project Coordinator",
    })
    role.insert(ignore_permissions=True)

    permissions = [
        {
            "doctype": "Project",
            "role": "Project Coordinator",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 0
        }
    ]

    for perm in permissions:
        frappe.get_doc(perm).insert(ignore_permissions=True)

setup_role_permissions()


