import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nigdy nie zgadniesz'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    POSTS_PER_PAGE = 3  # ?????????
    # end of bare template -> pure css framework config ->
    PURECSS_RESPONSIVE_GRIDS = True
    PURECSS_USE_CDN = True
    PURECSS_USE_MINIFIED = True
    # upload configs
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF", "TIFF", 'TIF']

    UPLOAD_FOLDER_FOR_ATTACH = 'app/static/attachments'

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'dodo.elektronic@gmail.com'
    MAIL_PASSWORD = 'Mandelbroot96'

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PRIVATE_KEY = '6LcnG7UZAAAAAGEwN2q12R4GbFBpJ63ADSth60Wq'
    RECAPTCHA_PUBLIC_KEY = '6LcnG7UZAAAAAGEwN2q12R4GbFBpJ63ADSth60Wq'
    RECAPTCHA_DATA_ATTRS = {'theme': 'light'}
    RECAPTCHA_PARAMETERS = {'hl': 'pl'}
