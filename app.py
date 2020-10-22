from flask import Flask, render_template
from flask_restful import Api, Resource, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import model


app = Flask(__name__)
api = Api(app)
CORS(app)

URL = "postgresql://postgres:admin1234@localhost:5432/postgres"


# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Add swager UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Api Test"
    }
)


# Render a html page with jquery
@app.route('/')
def index():
    return render_template('index.html')


# Get all Member
class getAll(Resource):
    def get(self):
        try:
            result = model.Member.query.all()
            res = []
            for r in result:
                res.append(r.serialize())
            return {'status': 'success', 'user': res}
        except Exception as e:
            print('Database Exception: ', e)
            return {'status': 'fail',
                    'detail': e}, 400


# Get Member by Id
class getById(Resource):
    def get(self, uid):
        try:
            result = model.Member.query.filter_by(id=uid).first()
            return {'status': 'success', 'user': result.serialize()}
        except Exception as e:
            print('Database Exception: ', e)
            return {'status': 'fail',
                    'detail': e}, 400


# Add Member by JSON
class addMemberByJSON(Resource):
    def post(self):
        try:
            data_obj = request.get_json()
            member = model.Member(**data_obj)
            model.db.session.add(member)
            model.db.session.commit()
            return {'status': 'success'}
        except Exception as e:
            print('Database Exception: ', e)
            return {'status': 'fail',
                    'detail': e}, 400


# Delete Member by ID
class deleteById(Resource):
    def delete(self, uid):
        try:
            result = model.Member.query.filter_by(id=uid).first()
            model.db.session.delete(result)
            model.db.session.commit()
            return {'status': 'success'}
        except Exception as e:
            print('Database Exception: ', e)
            return {'status': 'fail',
                    'detail': e}, 400


# Update Member by ID
class updateById(Resource):
    def put(self, uid):
        try:
            data_js = request.get_json()
            result = model.Member.query.filter_by(id=uid).first()
            result.name = data_js['name']
            result.age = data_js['age']
            result.email = data_js['email']
            result.phone = data_js['phone']
            model.db.session.commit()
            return {'status': 'success'}
        except Exception as e:
            print('Database Exception: ', e)
            return {'status': 'fail',
                    'detail': e}, 400


# URL for get all Member
api.add_resource(getAll, '/all')
# URL for get Member by Id
api.add_resource(getById, '/user/<uid>')
# URL for add Member by JSON
api.add_resource(addMemberByJSON, '/add')
# URL for delete Member by ID
api.add_resource(deleteById, '/delete/<uid>')
# URL for update Member by ID
api.add_resource(updateById, '/update/<uid>')

if __name__ == '__main__':
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    app.run(debug=True)
