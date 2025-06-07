import json
import os
from typing import Any, Callable


class DB:
    def __init__(self):
        self.db = {}
        self.db_file = "db.json"
        if os.path.exists(self.db_file):
            self._load_db()

    def _save_db(self):
        with open(self.db_file, "w") as f:
            json.dump(self.db, f, indent=2)

    def _load_db(self):
        with open(self.db_file, "r") as f:
            self.db = json.load(f)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name != "db" and name != "db_file":
            self.db[name] = value
            self._save_db()

    def __getattr__(self, name: str) -> Any:
        return self.db[name]

    def __delattr__(self, name: str) -> None:
        del self.db[name]
        self._save_db()

    def __str__(self) -> str:
        return str(self.db)

    def __repr__(self) -> str:
        return repr(self.db)

    # creaeta a function wrapper to load and save the db
    def load_and_save(func: Callable) -> Callable:
        def wrapper(self, *args, **kwargs):
            self._load_db()
            result = func(self, *args, **kwargs)
            self._save_db()
            return result

        return wrapper

    @load_and_save
    def create_table(self, name: str) -> None:
        if name in self.db:
            raise ValueError(f"Table {name} already exists")
        self.db[name] = {}

    @load_and_save
    def get_table(self, name: str) -> dict:
        return self.db[name]

    @load_and_save
    def delete_table(self, name: str) -> None:
        del self.db[name]

    @load_and_save
    def get_all_tables(self) -> list:
        return list(self.db.keys())

    @load_and_save
    def create_record(self, table: str, data: dict) -> None:
        length = len(self.db[table])
        data["id"] = length
        self.db[table][length] = data

    @load_and_save
    def get_record(self, table: str, id: str) -> dict:
        return self.db[table][id]

    @load_and_save
    def update_record(self, table: str, id: str, data: dict) -> None:
        # update only the required keys
        for key in data.keys():
            self.db[table][id][key] = data[key]

    @load_and_save
    def delete_record(self, table: str, id: str) -> None:
        del self.db[table][id]


class Note(DB):
    def __init__(self):
        super().__init__()
        if "notes" not in self.db:
            self.create_table("notes")

    def create_note(self, title: str, content: str) -> None:
        self.create_record("notes", {"title": title, "content": content})

    def get_note(self, id: str) -> dict:
        return self.get_record("notes", id)

    def update_note(self, id: str, title: str, content: str) -> None:
        self.update_record("notes", id, {"title": title, "content": content})

    def delete_note(self, id: str) -> None:
        self.delete_record("notes", id)

    def get_all_notes(self) -> list:
        return list(self.get_table("notes").values()) or []

    def search_notes(self, query: str) -> list:
        return [
            note
            for note in self.get_all_notes()
            if query in note["title"] or query in note["content"]
        ]


note_db = Note()
