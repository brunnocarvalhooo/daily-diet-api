from app_factory import create_app
from modules.users import users
from modules.meals import meals
from database import db

app = create_app()

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(meals, url_prefix='/meals')


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello world'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
