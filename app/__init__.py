from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
_session = Session()

def create_app():
    app.config["SECRET_KEY"] = "jfjgfdklgfdklgfde6{OPI)Ujtub-89t940g8tnen7"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbase.db"
    app.config["SESSION_COOKIE_NAME"] = "unique"
    app.config['SESSION_TYPE'] = 'filesystem'  # Store session in temporary files
    app.config['SESSION_PERMANENT'] = False

    db.init_app(app)
    migrate.init_app(app,db)
    _session.init_app(app)
    

    from .controllers.post import post
    from .controllers.user import user

    app.register_blueprint(post,url_prefix="/p")
    app.register_blueprint(user,url_prefix="/u")

    from .models.post import Post
    from .models.user import User

    from .utils import get_nickname,generate_session

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
