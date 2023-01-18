from app import app
from app.models import Page, Sortable, Post
from sqlalchemy.sql.expression import case

# posprawdzać co jest użyte a co nie!!!!!!!!!


def menuSort():
    obiekt = Sortable.query.filter_by(id=0).first().data
    sort = obiekt.split(',')
    sort.pop(0)
    ordering = case(
        {id: index for index, id in enumerate(sort)},
        value=Page.id
        )
    pages = Page.query.filter(Page.id.in_(sort)).order_by(ordering).all()
    return pages


def gridSort(id):
    obiekt = Sortable.query.filter_by(id=id).first().data
    sort = obiekt.split(',')
    sort.pop(0)
    ordering = case(
        {id: index for index, id in enumerate(sort)},
        value=Post.id
        )
    posts = Post.query.filter(Post.parent.has(id=id)).filter(
            Post.id.in_(sort)).order_by(ordering).all()
    return posts


def isIndexQuery():
    indexquery = Page.query.filter(Page.is_index == True).first()
    return indexquery


def postParent(id):
    pparent = Page.query.filter(Post.parent).filter(Post.id == id).first()
    return pparent


# Creating entries in S-State for given post and id(for filter databse purpose)
# -> works only within forms after added Post -> has to be commited after!
def filterSortState(post, id):
    post_id = post.id
    sortable_state = Sortable.query.filter_by(id=id).first()
    comma = ','
    comma_page_id = f'{comma}{post_id}'
    sortable_state.data = f'{comma_page_id}{sortable_state.data}'
    return sortable_state.data


def allowed_image(filename):

    # We only want files with a . in the filename
    if "." not in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False
