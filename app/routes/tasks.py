from flask import Blueprint, request, jsonify
from ..models.task import db, Task

bp = Blueprint("tasks", __name__)


@bp.route("/health")
def health():
    return "ok", 200


@bp.route("/tasks", methods=["GET", "POST"])
def tasks():

    if request.method == "POST":
        data = request.json or {}

        task = Task(
            title=data.get("title"),
            room=data.get("room")
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({
            "id": task.id,
            "title": task.title,
            "room": task.room
        }), 201

    tasks = Task.query.all()

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "room": t.room
        }
        for t in tasks
    ])