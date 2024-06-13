frappe.ui.form.on('Project', {
    refresh: function(frm) {
        set_project_status_color(frm);
    },
    status: function(frm) {
        set_project_status_color(frm);
    }
});

function set_project_status_color(frm) {
    let status_color = {
        "Planning": "#FFCDD2",
        "Execution": "#FFF9C4",
        "Closure": "#C8E6C9"
    };
    frm.page.wrapper.style.backgroundColor = status_color[frm.doc.status] || "#FFFFFF";
}

frappe.ui.form.on('Project', {
    refresh: function(frm) {
        toggle_budget_field(frm);
    },
    status: function(frm) {
        toggle_budget_field(frm);
    }
});

function toggle_budget_field(frm) {
    if (frm.doc.status === "Planning") {
        frm.set_df_property('budget', 'hidden', 1);
    } else {
        frm.set_df_property('budget', 'hidden', 0);
    }
}

frappe.ui.form.on('Project Task', {
    task_cost: function(frm, cdt, cdn) {
        calculate_budget_utilization(frm);
    }
});

function calculate_budget_utilization(frm) {
    let total_spent = 0;
    frm.doc.project_tasks.forEach(task => {
        total_spent += task.task_cost || 0;
    });
    let budget_utilization = (total_spent / frm.doc.budget) * 100;
    frm.set_value('budget_utilization', budget_utilization);
}

frappe.ui.form.on('Project', {
    before_save: function(frm) {
        if (frm.doc.status_changed) {
            frappe.confirm('Are you sure you want to close this project?', function() {
                frm.doc.status_changed = false;
                frm.save();
            }, function() {
                frappe.msgprint('Project closure canceled');
                frm.doc.status = frm.doc._original_status;
            });
            return false;
        }
        frm.doc._original_status = frm.doc.status;
    },
    status: function(frm) {
        frm.doc.status_changed = true;
    }
});

frappe.ui.form.on('Project', {
    before_save: function(frm) {
        if (frm.doc.end_date < frm.doc.start_date) {
            frappe.msgprint(__('End Date cannot be earlier than Start Date'));
            frappe.validated = false;
        }
    }
});


