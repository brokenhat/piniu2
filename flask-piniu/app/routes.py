import os
import re
import datetime
from PIL import Image
from flask_mail import Message, Mail
from flask import render_template, flash, redirect, url_for, request, jsonify
# from flask import session
from app import app, db, celery

from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.forms import UpdatePost, DeletePost, NewPage, RemovePage, IsIndex
from app.forms import UploadFile, UploadAttach, ContactForm, AddContactForm
from app.forms import DateForm

from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Page, Sortable, Order
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app.webfunctions import menuSort, isIndexQuery, filterSortState
from app.webfunctions import postParent, gridSort, allowed_image
# from app.celery_function import send_email


@celery.task
def send_email(email_data, n_n):

    mail = Mail()
    msg = Message('Kocioł ' + email_data['nr.'] + ', przegląd: ' + n_n,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=['domino.zarzycki@gmail.com',
                              'za.marcin@gmail.com',
                              'dodo.elektronic@gmail.com'])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET'])
def index():
    # Showing  pages
    pages = menuSort()
    pages_other = Page.query.all()
    current_page = isIndexQuery()
    posts = gridSort(id=current_page.id)
    contactForm = ContactForm()

    return render_template('index.html', title='Strona główna',
                           pages=pages, posts=posts,
                           current_page=current_page,
                           pages_other=pages_other,
                           contactForm=contactForm)


# podstrony
@app.route('/<string:title>/', methods=['GET'])
def page(title):

    # displaying pages
    current_page = Page.query.filter(Page.title == title).first()
    pages_other = Page.query.all()
    pages = menuSort()
    contactForm = ContactForm()
# end displaying pages
    if current_page is not None:
        posts = gridSort(id=current_page.id)
    else:
        return redirect(url_for('index'))

    return render_template('index.html', posts=posts,
                           pages=pages,
                           current_page=current_page,
                           pages_other=pages_other,
                           contactForm=contactForm)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/display_attach/<filename>')
def display_attach(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='attachments/' + filename), code=301)


# edycja stron
@app.route('/editpage/<int:id>/', methods=['GET', 'POST'])
@login_required
def editpage(id):

    filename = ''
    # Forms
    form = PostForm()
    pageform = NewPage()
    checkform = IsIndex()
    update = UploadFile()
    attachForm = UploadAttach()
    addContactForm = AddContactForm()
    contactForm = ContactForm()
    # end Forms
    current_page_id = Page.query.filter(Page.id == id).first()
# INSTALATORZY
    matchlist = ''
    users = User.query.all()
    for i in users:
        matches = re.search("instalator", str(i.username), re.IGNORECASE)
        if matches is not None:
            matchlist = matchlist + ',' + str(i.id)
    matchList = []
    for i in matchlist:
        if i is not None:
            matchList.append(User.query.filter_by(id=i).first())
    matchList = [i for i in matchList if i]
    pages_other = Page.query.all()
# INSTALATORZY End
# ----------------
# Displaying posts
    posts = gridSort(id=id)
# Displaying pages in menu
    pages = menuSort()
# Adding pages // zapis stanu nowej strony dla POSTÓW w sstate
    if pageform.validate_on_submit():
        page = Page(title=pageform.title.data)
        db.session.add(page)
        db.session.commit()
        iD = page.id
        with db.session.no_autoflush:
            sstate = Sortable(id=iD, data=',1,2')
            if Sortable.query.get(iD) != iD:
                db.session.add(sstate)
# sortable_state_for_menu start saves to 0 ->
# def in webfunctions repeated page.id var ! poprawić
        filterSortState(post=page, id=0)
        db.session.commit()
        flash('Strona została dodana.')
        return redirect(url_for('editpage', id=id))
# 0 ADDING POSTS
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user,
                    parent=current_page_id)
        db.session.add(post)
        db.session.commit()
# 0 creating entries in states for posts
        filterSortState(post=post, id=id)
        db.session.commit()
        flash('Zmiany zostały opublikowane!')
        return redirect(url_for('editpage', id=id))
# 1 UPLOADING IMAGES with description
    if update.validate_on_submit():
        descr = update.descr.data
        file = update.image.data
        if allowed_image(file.filename):  # def in webfunctions allowed ext.
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
# 1 simple compression of saved images
            basewidth = 900
            image = Image.open(image_path)
            imgwidth, imgheight = image.size
            if imgwidth >= basewidth:
                basewidth = basewidth
            else:
                basewidth = imgwidth
            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)
            thumb_name = 'thumb-' + filename
            thumb_path = os.path.join(app.config['UPLOAD_FOLDER'], thumb_name)
            image.save(thumb_path, quality=85, optimize=True)
        else:
            flash('Błędne rozszerzenie.')
            return redirect(request.url)
# 1 adding post(images Column)
        img = Post(body=descr, author=current_user,
                   parent=current_page_id, images=filename)
        db.session.add(img)
        db.session.commit()
# 1 creating entries for img in POSTS DATA
        filterSortState(post=img, id=id)
        db.session.commit()
        flash('Plik został przesłany')
        return redirect(url_for('editpage', id=id))
# 2 ADDING ATTACHEMENTS
    if attachForm.validate_on_submit():
        descr = attachForm.descr.data
        attachment = attachForm.attach.data
        # allowing specific attach ext. ?????
        filename = secure_filename(attachment.filename)
        attachment.save(os.path.join(app.config['UPLOAD_FOLDER_FOR_ATTACH'], filename))
# 2 saving file end
        attachPost = Post(body=descr, author=current_user,
                          parent=current_page_id, attachments=filename)
        db.session.add(attachPost)
        db.session.commit()
# 2 creating entries for attach in POSTS DATA
        filterSortState(post=attachPost, id=id)
        db.session.commit()
        flash('Plik został przesłany')
        return redirect(url_for('editpage', id=id))
# 3 ADDING CONTACT FORM
    if addContactForm.validate_on_submit():
        formPost = Post(author=current_user, parent=current_page_id,
                        contact=True)
        db.session.add(formPost)
        db.session.commit()
        filterSortState(post=formPost, id=id)
        db.session.commit()
        flash("Dodano formularz.")
        return redirect(url_for('editpage', id=id))

    return render_template('edit.html', title='Edycja strony',
                           form=form, current_page_id=current_page_id,
                           pages=pages, pageform=pageform,
                           posts=posts, checkform=checkform,
                           update=update, attachForm=attachForm,
                           matchList=matchList, pages_other=pages_other,
                           addContactForm=addContactForm,
                           contactForm=contactForm)


@app.route('/login', methods=['GET', 'POST'])
def login():

    indexquery = isIndexQuery()
    indexid = indexquery.id
    current_page = indexquery
    match = ''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # szukanie słowa instalator po wprowadzeniu do formy loginu.
        if user is None or not user.check_password(form.password.data):
            flash('Nieprawidłowa nazwa użytkownika lub hasło.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        next_page_inst = next_page
        if not next_page or url_parse(next_page).netloc != '':
            next_page_inst = url_for('instalator', username=current_user.username)
            next_page = url_for('editpage', id=indexid)
        match = re.search("instalator", str(user.username))
        if match is not None:
            return redirect(next_page_inst)
        else:
            return redirect(next_page)
    if current_user.is_authenticated:
        if match is not None:
            return redirect(url_for('instalator', username=current_user.username))
        else:
            return redirect(url_for('editpage', id=indexid))
    return render_template('login.html', title='Zaloguj się', form=form,
                           current_page=current_page)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# rejestracja użytkownika
@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    indexquery = isIndexQuery()
    indexid = indexquery.id
    current_page = indexquery  # do poprawy

    # if current_user.is_authenticated:
    #    return redirect(url_for('editpage', id=indexid))
    form = RegistrationForm()
    if form.validate_on_submit():
        match = re.search("instalator", str(form.username.data), re.IGNORECASE)
        username = form.username.data  # jakby co-to pusty string-tylko dla VIP
        if match is not None:
            username = username.lower()
        user = User(username=username, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
# Tylko dla instalatorów:
        match = re.search("instalator", str(user.username))
        if match is not None:
            page = Page(title=user.username)
            db.session.add(page)
            db.session.commit()
            iD = page.id
            with db.session.no_autoflush:
                sstate = Sortable(id=iD, data=',1,2')
                if Sortable.query.get(iD) != iD:
                    db.session.add(sstate)
                # filterSortState(post=page, id=0)  # ???????????
                db.session.commit()
# dla instalatorów END
        # flash('Możesz teraz zalogować się na swoje konto.')
        return redirect(url_for('editpage', id=indexid))
    return render_template('register.html', title='Rejestracja',
                           form=form, current_page=current_page)


# profil użytkownika
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):

    # Displaying pages
    pages = menuSort()

    pageform = NewPage()
    checkform = IsIndex()

    indexquery = isIndexQuery()
    indexid = indexquery.id

    user = User.query.filter_by(username=username).first_or_404()

    if request.method == 'POST':
        flash('Dopiero teraz możesz wprowadzać zmiany.')
        return redirect(url_for('editpage', id=indexid))

    return render_template('user.html', user=user,
                           pageform=pageform, pages=pages,
                           checkform=checkform, indexid=indexid)


# zmiana nazwy użytkownika
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    indexquery = isIndexQuery()
    indexid = indexquery.id
    current_page_id = indexquery

    pageform = NewPage()
    checkform = IsIndex()
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Zmiany zostały zapisane.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Zmiana nazwy użytkownika',
                           form=form, pageform=pageform,
                           checkform=checkform,
                           current_page_id=current_page_id,
                           indexid=indexid)


# edycja postów
@app.route('/editpost/<int:id>', methods=['GET', 'POST'])
@login_required
def editpost(id):

    checkform = IsIndex()
    pageform = NewPage()
    # displaying pages
    pages = menuSort()
# End of displaying pages
    pParent = postParent(id=id).id
    # postParent takes id as an argument then -
    # - it returns page -> then you have to take page.id!

    post = Post.query.filter(Post.id == id).first()
    form = UpdatePost()  # class <- forms <- import na początku
    if form.validate_on_submit():
        post.body = form.post.data
        db.session.commit()
        flash('Post został zedytowany.')
        return redirect(url_for('editpage', id=pParent))
    elif request.method == 'GET':
        form.post.data = post.body
    return render_template('edit_post.html', form=form, post=post,
                           pageform=pageform, pages=pages,
                           checkform=checkform)


# usuwanie postów
@app.route('/deletepost/<int:id>', methods=['GET'])
@login_required
def deletepost(id):
    post = Post.query.filter(Post.id == id).first()
    pParent = postParent(id=id).id
    form = DeletePost()
    form.delete = db.session.delete(post)
    db.session.commit()
    flash('Post został usunięty')
    return redirect(url_for('editpage', id=pParent))


# usuwanie stron
@app.route('/deletepage/<int:id>', methods=['GET'])
@login_required
def deletepage(id):
    page = Page.query.filter(Page.id == id).first()
    indexquery = isIndexQuery()
    indexid = indexquery.id
    form = RemovePage()
    if page.id == indexid:
        flash('Nie można usunąć strony głównej.')
    else:
        form.remove = db.session.delete(page)
        sstate_for_posts = Sortable.query.get(id)
        db.session.delete(sstate_for_posts)
        db.session.commit()
        flash('Strona została usunięta')
    return redirect(url_for('editpage', id=indexid))  # poprawić !!!!


# USUWANIE INSTALATORÓW  <user.username> <page.id>
@app.route('/delete_user/<username>/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(username, id):
    indexquery = isIndexQuery()
    indexid = indexquery.id
    instalator = User.query.filter(User.username == username).first()
    db.session.delete(instalator)
    page = Page.query.get(id)
    db.session.delete(page)
    sort = Sortable.query.get(id)
    db.session.delete(sort)
    db.session.commit()
    return redirect(url_for('editpage', id=indexid))


# select index page
@app.route('/selectpage/<string:is_index>/<int:id>/', methods=['GET', 'POST'])
@login_required
def selectpage(is_index, id):
    checkform = IsIndex()
    pages = Page.query.all()
    page = Page.query.filter_by(id=id).first()
    for p in pages:
        checkform.question = p.is_index = False
        checkform.question = db.session.add(p)

    checkform.question = page.is_index = True
    checkform.question = db.session.add(page)
    flash('Ustawiono stronę główną.')
    db.session.commit()
    return redirect(url_for('editpage', is_index=is_index, id=id))


# menu sort
@app.route('/sort', methods=['GET', 'POST'])
@login_required
def sort():
    json = request.json
    x = json.replace('elem[]=', ',')
    final = x.replace('&,', ',')
    # final = y.replace(',', '')

    sort = Sortable.query.filter_by(id=0).first()
    sort.data = final

    db.session.commit()

    return jsonify(final)


# post sorting (Sortable)
@app.route('/sortgrid/<int:id>/', methods=['GET', 'POST'])
@login_required
def sortgrid(id):
    json = request.json
    x = json.replace('item[]=', ',')
    final = x.replace('&,', ',')
    # final = y.replace(',', '')

    sort = Sortable.query.filter_by(id=id).first()
    # newdata = sort.data
    # newdata = f'{olddata}{final}'
    sort.data = final

    db.session.commit()

    return jsonify(final)


# post layout changing -> Storing data in Post.data -> buttons in edit -> panel
@app.route('/lay/<int:id>/', methods=['GET', 'POST'])
@login_required
def lay(id):
    jsony = request.json
    sort = Post.query.filter_by(id=id).first()
    sort.data = jsony
    db.session.commit()

    # print(json.dumps(jsony))
    return jsonify(jsony)


# #####################public part-end#######################
# WIDOK DLA INSTALATORÓW
@app.route('/instalator/<username>', methods=['GET'])
@login_required
def instalator(username):
    current_page = Page.query.filter(Page.title == username).first()
    pages = Page.query.all()
    posts = gridSort(id=current_page.id)
    return render_template('index.html',
                           current_page=current_page,
                           pages=pages, posts=posts)


# KONTAKT FORM
@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    contactForm = ContactForm()
    mail = Mail()
    print(f'Request method: {request.method}')
    print(f'Validation: {contactForm.validate_on_submit()}')
    print(f'Recaptcha: {contactForm.recaptcha}')
    if contactForm.validate_on_submit():
        msg = Message(contactForm.subject.data,
                      sender='dodo.elektronic@gmail.com',
                      recipients=['domino.zarzycki@gmail.com',
                                  'za.marcin@gmail.com',
                                  'dodo.elektronic@gmail.com'])
        msg.body = """
        Od: %s <%s>
        %s
        """ % (contactForm.name.data,
               contactForm.email.data,
               contactForm.message.data)
        mail.send(msg)
        flash("Formularz został przesłany.")
        return redirect(url_for('index'))
    else:
        flash('Wszystkie pola są wymagane!')
        return redirect(url_for('index'))


# Przypomnienia, Historia zamówień --> CELERY CONT.
@app.route('/orders-history/', methods=['GET', 'POST'])
@login_required
def reminder():
    # Date Form
    dateform = DateForm()
    now = datetime.datetime.utcnow()
    # for redirect
    indexid = isIndexQuery().id
    current_page = {"id": indexid, 'title': "Zamówienia"}
    # print(current_page['title'])
    # indexid needed for get back to editpage
    if request.method == 'GET':
        orders = Order.query.order_by(Order.timestamp.desc()).all()
        reminders = Order.query.order_by(Order.reminder.asc()).all()
        return render_template('reminder.html', current_page=current_page,
                               orders=orders,
                               dateform=dateform,
                               reminders=reminders, now=now)

    numer = request.form['numer']
    miejsce = request.form['miejsce']
    opis = request.form['opis']
    data = dateform.dt.data

    year = int(data.strftime('%Y'))
    month = int(data.strftime('%m'))
    day = int(data.strftime('%d'))
    date_from_data = datetime.datetime(year=year, month=month, day=day)

    # session['numer'] = numer
    # session['miejsce'] = miejsce
    # session['opis'] = opis

    order = Order(numer=numer,
                  miejsce=miejsce,
                  opis=opis,
                  reminder=date_from_data)  # REMINDER COLUMN !!!
    db.session.add(order)
    db.session.commit()
    stamp = Order.query.filter(Order.id == order.id).first().timestamp
    flash("Dodano wpis.")

    yearnow = int(now.strftime('%Y'))
    monthnow = int(now.strftime('%m'))
    daynow = int(now.strftime('%d'))
    object = datetime.datetime(year=yearnow, month=monthnow, day=daynow)

    oneday = 86400
    week = oneday * 7
    twodays = oneday * 2
    n_1 = 'Jutro'
    n_2 = 'Pojutrze'
    n_7 = 'za Tydzień'

    email_data = {
        'nr.': numer,
        'body': """
| ustawiono datę przeglądu na -- %s
| nr. kotła------ < %s >
| miejsce---------- %s
| opis------------- %s
| przypomnienie utworzono dnia - %s
         """ % (data,
                numer,
                miejsce,
                opis,
                stamp)
        }

    set_reminder = (date_from_data - object).days
    # print(str(set_reminder) + ' days.')

    if request.method == 'POST':
        if set_reminder < 7 and set_reminder > 0:

            send_email.apply_async(args=[email_data, n_1],
                                   countdown=set_reminder * oneday - oneday)
        elif set_reminder > 7:
            send_email.apply_async(args=[email_data, n_7],
                                   countdown=set_reminder * oneday - week)
            send_email.apply_async(args=[email_data, n_2],
                                   countdown=set_reminder * oneday - twodays)
    return redirect(url_for('reminder'))


# DO EDYCJI TABELKI
@app.route('/get_order/<int:id>', methods=['GET', 'POST'])
@login_required
def get_order(id):
    json = request.json

    numer = json['numer']
    n = numer.replace('<i></i>', '')
    numer_fin = n

    miejsce = json['miejsce']
    m = miejsce.replace('<i></i>', '')
    miejsce_fin = m

    opis = json['opis']
    o = opis.replace('<i></i>', '')
    opis_fin = o

    order = Order.query.get(id)
    order.numer = numer_fin
    order.miejsce = miejsce_fin
    order.opis = opis_fin
    db.session.commit()

    final = numer_fin + ',' + miejsce_fin + ',' + opis_fin

    return jsonify(final)


# USUWANIE WPISU W TABLECE i db.Model(Order)
@app.route('/delete-order/<int:id>/', methods=['GET', 'POST'])
@login_required
def delete_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    flash("Usunięto wpis.")
    return redirect(url_for('reminder'))


# DO KOLOROWANIA WYBRANEGO WIERSZA W TABLECE(wpisu)
@app.route('/oznacz/<int:id>/', methods=['GET', 'POST'])
@login_required
def oznacz(id):
    json = request.json
    order = Order.query.filter(Order.id == id).first()
    order.data = json
    db.session.commit()

    return jsonify(json)



@app.route('/setBackground/<int:id>/', methods=['GET', 'POST'])
@login_required
def setBackground(id):
    json = request.json
    post = Post.query.filter(Post.id == id).first()
    post.background = json
    db.session.commit()

    return jsonify(json)
