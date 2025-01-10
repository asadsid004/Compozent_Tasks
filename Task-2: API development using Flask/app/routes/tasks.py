from flask import (
    Blueprint,
    abort,
    jsonify,
    redirect,
    request,
    flash,
    url_for,
    render_template,
)
from flask_login import login_required, current_user
from app.models import PriorityLevel, Task
from app import db
from datetime import datetime
from sqlalchemy import desc, asc

tasks = Blueprint("tasks", __name__)


@tasks.route("/", methods=["GET", "POST"])
@login_required
def manage_tasks():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority", "medium").lower()

        # Validate priority
        if priority not in [level.value for level in PriorityLevel]:
            flash("Invalid priority level.", "error")
            return redirect(url_for("tasks.manage_tasks"))

        try:
            task = Task(
                title=title,
                description=description,
                due_date=datetime.strptime(due_date, "%Y-%m-%d"),
                priority=PriorityLevel(priority),
                user_id=current_user.id,
                status="pending",
            )
            db.session.add(task)
            db.session.commit()
            flash("Task added successfully.", "success")
        except ValueError as e:
            flash(f"Error creating task: {str(e)}", "error")

        return redirect(url_for("tasks.manage_tasks"))

    # Get filter and sort parameters
    priority_filter = request.args.get("priority")
    sort_by = request.args.get("sort_by", "due_date")
    order = request.args.get("order", "asc")

    # Build query
    query = Task.query.filter_by(user_id=current_user.id)

    # Apply priority filter if specified
    if priority_filter and priority_filter in [level.value for level in PriorityLevel]:
        query = query.filter_by(priority=PriorityLevel(priority_filter))

    # Apply sorting
    sort_column = getattr(Task, sort_by, Task.due_date)
    query = query.order_by(desc(sort_column) if order == "desc" else asc(sort_column))

    tasks = query.all()

    upcoming_tasks = [task for task in tasks if task.status != "completed"]
    completed_tasks = [task for task in tasks if task.status == "completed"]

    # Get priority counts for statistics
    priority_counts = {
        priority.value: Task.query.filter_by(
            user_id=current_user.id, priority=priority, status="pending"
        ).count()
        for priority in PriorityLevel
    }

    return render_template(
        "tasks/tasks.html",
        upcoming_tasks=upcoming_tasks,
        completed_tasks=completed_tasks,
        now=datetime.today(),
        priority_levels=PriorityLevel,
        priority_counts=priority_counts,
        current_priority=priority_filter,
        current_sort=sort_by,
        current_order=order,
    )


@tasks.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully.", "success")
    return redirect(url_for("tasks.manage_tasks"))


@tasks.route("/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    task.status = "completed" if task.status == "pending" else "pending"
    db.session.commit()
    flash("Task status updated.", "success")
    return redirect(url_for("tasks.manage_tasks"))


@tasks.route("/<int:task_id>/priority", methods=["POST"])
@login_required
def update_priority(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)

    new_priority = request.form.get("priority", "").lower()
    if new_priority not in [level.value for level in PriorityLevel]:
        flash("Invalid priority level.", "error")
        return redirect(url_for("tasks.manage_tasks"))

    task.priority = PriorityLevel(new_priority)
    db.session.commit()
    flash("Task priority updated.", "success")
    return redirect(url_for("tasks.manage_tasks"))


@tasks.route("/filter", methods=["GET"])
@login_required
def filter_tasks():
    priority = request.args.get("priority")
    sort_by = request.args.get("sort_by", "due_date")
    order = request.args.get("order", "asc")

    return redirect(
        url_for("tasks.manage_tasks", priority=priority, sort_by=sort_by, order=order)
    )
