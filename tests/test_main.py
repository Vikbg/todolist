from datetime import datetime

import bcrypt

from main import Task, User


def test_user_password_is_hashed():
    user = User("alice", "correct-horse-battery-staple")

    assert user.password_hash != "correct-horse-battery-staple"
    assert bcrypt.checkpw(
        b"correct-horse-battery-staple",
        user.password_hash.encode("utf-8"),
    )


def test_task_initializes_expected_fields():
    before_creation = datetime.now()
    task = Task("Fix CI", 2, "Verify the Python workflow")

    assert task.name == "Fix CI"
    assert task.description == "Verify the Python workflow"
    assert task.completed is False
    assert task.last_modified >= before_creation
    assert task.complete_before > task.last_modified
