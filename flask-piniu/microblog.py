from app import app, db
from app.models import User, Post, Page, Sortable, Order


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Page': Page, 'Sortable': Sortable, 'Order': Order}
