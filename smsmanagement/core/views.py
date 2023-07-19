from flask import render_template, request, Blueprint

core = Blueprint('core', __name__)


@core.route('/index')
def index():
    return render_template('index.html')


# @core.route('/',  methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')


@core.route('/aboutUs')
def aboutUs():
    return render_template('about_us.html')


