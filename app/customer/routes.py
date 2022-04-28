from flask import Blueprint, request
from app.token_required import token_required

# models
from app.models import Customer, System, db

# blueprint
customer = Blueprint('customer', __name__, template_folder='customer_templates')

@customer.route('/api/customer-list')
@token_required
def apiCustomerList(user):
    if user.company_id:
        customers = Customer.query.filter_by(company_id=user.company_id).all()
        return {
            'status': 'success',
            'total_results': len(customers),
            'customers': [c.to_dict() for c in customers][::-1]
        }
    else:
        customers = Customer.query.filter_by(user_id=user.id).all()
        return{
            'status': 'success',
            'total_results': len(customers),
            'customers': [c.to_dict() for c in customers][::-1]
        }

@customer.route('/api/customers/create', methods=["POST"])
@token_required
def apiCreateCustomer(user):
    data = request.json

    name = data['name']
    street_address = data['street_address']
    city = data['city']
    state = data['state']
    zip_code = data['zip_code']
    email = data['email']
    
    customer = Customer(name, street_address, city, state, zip_code, email, user.id)

    if user.company_id:
        customer.company_id = user.company_id
    
    db.session.add(customer)
    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully created a new Customer, {name}.',
        'customer': customer.to_dict()
    }
    
@customer.route('/api/customers/<int:customer_id>')
@token_required
def apiCustomerInfo(customer_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return {
            'status': 'error',
            'message': 'No customer found.'
        }
    if (customer.user_id != user.id) and (customer.company_id != user.company_id):
        return {
            'status': 'error',
            'message': 'Access to this customer denied.'
        }

    return {
        'status': 'success',
        'total_results': 1,
        'customer': customer.to_dict()
    }

@customer.route('/api/customers/edit/<int:customer_id>', methods=["POST"])
@token_required
def apiUpdateCustomer(customer_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()

    if customer is None:
        return {
            'status': 'error',
            'message': 'No customer found.'
        }
    if (customer.user_id != user.id) and (customer.company_id != user.company_id):
        return {
            'status': 'error',
            'message': 'Access to this customer denied.'
        }

    data = request.json
    customer.name = data['name']
    customer.street_address = data['street_address']
    customer.city = data['city']
    customer.state = data['state']
    customer.zip_code = data['zip_code']
    customer.email = data['email']

    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully updated {customer.name}.',
        'company': customer.to_dict()
    }

@customer.route('/api/customers/delete/<int:customer_id>', methods=["POST"])
@token_required
def apiDeleteCustomer(customer_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()
    systems = System.query.filter_by(customer_id=customer_id).all()
    if customer is None:
        return {
            'status': 'error',
            'message': 'No customer found.'
        }
    if (customer.user_id != user.id) and (customer.company_id != user.company_id):
        return {
            'status': 'error',
            'message': 'Access to this customer denied.'
        }

    for system in systems:
        db.session.delete(system)
    db.session.commit()
    db.session.delete(customer)
    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully deleted {customer.name}.'
    }
