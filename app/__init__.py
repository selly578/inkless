from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import MetaData
from dotenv import load_dotenv
from markdown import markdown
from os import getenv,path

load_dotenv()

app = Flask(__name__)

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
_session = Session()
cors = CORS(app, support_credentials=True)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
)

def create_app():
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbase.db"
    app.config["SESSION_COOKIE_NAME"] = "unique"
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SESSION_PERMANENT'] = False

    db.init_app(app)
    migrate.init_app(app,db)
    _session.init_app(app)



    from .controllers.post import post
    from .controllers.user import user

    app.register_blueprint(post,url_prefix="/posts")
    app.register_blueprint(user)

    from .models.post import Post
    from .models.user import User

    from .utils import get_nickname,generate_session

    @app.route("/landigpage")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        file = open(path.join(app.root_path,"docs/about.md"),"r").read()
        about = markdown(file)
        return render_template("about.html",about=about)

    @app.route("/policy")
    def policy():
        file = open(path.join(app.root_path,"docs/policy.md"),"r").read()
        policy = markdown(file)
        return render_template("policy.html",policy=policy)
    
    @app.route("/tos")
    def tos():
        file = open(path.join(app.root_path,"docs/tos.md"),"r").read()
        tos = markdown(file)
        return render_template("tos.html",tos=tos)

    return app
