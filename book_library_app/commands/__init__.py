from flask import Blueprint

db_manager_bp = Blueprint('db_manager_cmd', __name__, cli_group=None)

from book_library_app.commands import db_manage_commands