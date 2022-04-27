from flask import Blueprint, request
from werkzeug.security import check_password_hash
from flask_cors import CORS

# models
from app.models import User, Company, db
from app.token_required import token_required

# blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates')

CORS(auth)

# routes
@auth.route('/api/login', methods=["POST"])
def apiLoginUser():
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user:
        if check_password_hash(user.password, password):
            return {
                'status': 'success',
                'message': f'Welcome back, {email}',
                'user': user.to_dict()
            }
        else:
            return {
                'status': 'error',
                'message': 'Incorrect password.'
            }
    else:
        return {
            'status': 'error',
            'message': 'A user with that email does not exist.'
        }

@auth.route('/api/signup', methods=["POST"])
def apiSignUp():
    data = request.json  
    
    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']
    password = data['password']
    conf_password = data['conf_password']

    if password != conf_password:
        return {
            'status': 'error',
            'message': 'The passwords do not match.'
        }

    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'status': 'error',
            'message': 'A user with that email already exists.'
        }

    user = User(email, password, first_name, last_name)
    db.session.add(user)
    db.session.commit()

    return {
        'status': 'success',
        'message': 'Successfully created a new account.',
        'user': user.to_dict()
    }

@auth.route('/api/user-info')
@token_required
def apiUserInfo(user):
    id = user.id

    user = User.query.filter_by(id=id).first()

    if user:
        return {
            'status': 'success',
            'message': 'User info retrieved',
            'user': user.to_dict()
        }
    else:
        return {
            'status': 'error',
            'message': 'Error retrieving user information'
        }

@auth.route('/api/profile/edit', methods=["POST"])
@token_required
def apiEditProfile(user):
    data = request.json

    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']

    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    db.session.commit()

    return {
        'status': 'success',
        'message': 'Successfully edited user profile.',
        'user': user.to_dict()
    }

@auth.route('/api/profile/add-company', methods=["POST"])
@token_required
def apiAddCompany(user):
    data = request.json
    print(data)
    company_name = data['company_name']
    company_password = data['company_password']

    company = Company.query.filter_by(company_name=company_name).first()

    if user.company_id:
        return {
            'status': 'error',
            'message': 'This user is already affiliated with a company'
        }
    if not company:
        return {
            'status': 'error',
            'message': 'No company with that name exists. Please try again.'
        }
    if company.company_password != company_password:
        return {
            'status': 'error',
            'message': 'Invalid password.'
        }

    user.company_id = company.id
    db.session.commit()

    return {
        'status': 'success',
        'message': f'Successfully linked account to {company_name}.',
        'user': user.to_dict()
    }

@auth.route('/api/profile/delete', methods=["POST"])
@token_required
def apiDeleteUser(user):
    if user is None:
        return {
            'status': 'error',
            'message': 'No user to delete.'
        }
    db.session.delete(user)
    db.session.commit()

    return {
            'status': 'success',
            'message': 'Successfully deleted your account.'
        }
