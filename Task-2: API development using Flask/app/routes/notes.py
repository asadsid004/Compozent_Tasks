from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Note

notes = Blueprint("notes", __name__)


@notes.route("/", methods=["GET", "POST"])
@login_required
def view_notes():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if content.strip() or title.strip():
            new_note = Note(content=content, title=title, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added successfully!", "success")
            return redirect(url_for("notes.view_notes"))
        else:
            flash("Note title or content cannot be empty.", "danger")
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes/notes.html", notes=user_notes)


@notes.route("/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash("You do not have permission to edit this note.", "danger")
        return redirect(url_for("notes.view_notes"))

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if content.strip() or title.strip():
            note.title = title
            note.content = content
            db.session.commit()
            flash("Note updated successfully!", "success")
            return redirect(url_for("notes.view_notes"))
        else:
            flash("Note title or content cannot be empty.", "danger")
    return render_template("notes/edit_note.html", note=note)


@notes.route("/delete/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash("You do not have permission to delete this note.", "danger")
        return redirect(url_for("notes.view_notes"))

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted successfully!", "success")
    return redirect(url_for("notes.view_notes"))


@notes.route("/search", methods=["GET", "POST"])
@login_required
def search_notes():
    query = request.form.get("query") if request.method == "POST" else ""
    if query:
        notes = (
            Note.query.filter(
                (Note.title.ilike(f"%{query}%")) | (Note.content.ilike(f"%{query}%"))
            )
            .filter_by(user_id=current_user.id)
            .all()
        )
        return render_template("notes/search_results.html", notes=notes, query=query)
    flash("Please enter a search query.", "warning")
    return redirect(url_for("notes.view_notes"))
