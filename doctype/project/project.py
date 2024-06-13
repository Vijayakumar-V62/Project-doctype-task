import frappe
from frappe.model.document import Document

class Project(Document):
    def validate(self):
        self.validate_dates()
        self.calculate_budget_utilization()

    def validate_dates(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            frappe.throw(_("End Date cannot be earlier than Start Date"))

    def calculate_budget_utilization(self):
        total_spent = sum([task.cost for task in self.project_tasks])
        self.budget_utilization = total_spent / self.budget * 100 if self.budget else 0


