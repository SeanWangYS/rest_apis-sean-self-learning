from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str, 
        required=True, 
        help='This filed connot be left blank!'
    )
    parser.add_argument('password', 
        type=str, 
        required=True, 
        help='This filed connot be left blank!'
    )

    def post(self):
        data = __class__.parser.parse_args() # it's a dict

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        # user = UserModel(data['username'], data['password'])
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully."}, 201
        
