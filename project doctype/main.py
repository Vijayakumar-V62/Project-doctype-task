import frappe

def get_projects():
    projects = frappe.get_all('Project', fields=['project_name', 'project_manager', 'start_date'])
    for project in projects:
        print(f"Project Name: {project.project_name}, Project Manager: {project.project_manager}, Start Date: {project.start_date}")

get_projects()

def get_filtered_sorted_projects(project_manager):
    projects = frappe.get_all('Project', filters={'project_manager': project_manager}, fields=['project_name', 'start_date'], order_by='start_date asc')
    for project in projects:
        print(f"Project Name: {project.project_name}, Start Date: {project.start_date}")

get_filtered_sorted_projects('Project Manager Name')

def calculate_total_budget():
    total_budget = frappe.db.sum('Project', 'budget')
    print(f"Total Budget: {total_budget}")

calculate_total_budget()

def get_projects_by_date_range(start_date, end_date):
    projects = frappe.get_all('Project', filters={'end_date': ['between', [start_date, end_date]]}, fields=['project_name', 'end_date'])
    for project in projects:
        print(f"Project Name: {project.project_name}, End Date: {project.end_date}")

get_projects_by_date_range('2024-01-01', '2024-12-31')

def get_projects_with_incomplete_tasks():
    projects = frappe.get_all('Project', fields=['project_name'])
    for project in projects:
        incomplete_tasks = frappe.get_all('Project Task', filters={'parent': project.project_name, 'task_status': ['!=', 'Completed']}, fields=['task_name'])
        if incomplete_tasks:
            print(f"Project Name: {project.project_name}")
            for task in incomplete_tasks:
                print(f"  Incomplete Task: {task.task_name}")

get_projects_with_incomplete_tasks()
