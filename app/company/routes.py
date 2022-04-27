from flask import Blueprint, request
from app.token_required import token_required

# models
from app.models import Company, db

# blueprint
company = Blueprint('company', __name__, template_folder='company_templates')

@company.route('/api/company')
@token_required
def apiCompanyInfo(user):
    company = Company.query.filter_by(id=user.company_id).first()
    if company:
        return {
            'status': 'success',
            'message': 'Company info retrieved',
            'company': company.to_dict()
        }
    else:
        return {
            'status': 'error',
            'message': 'Error retrieving company information'
        }

@company.route('/api/company/create', methods=["POST"])
@token_required
def apiCreateCompany(user):
    if user.company_id:
        return {
            'status': 'error',
            'message': 'This account is already affiliated with company.'
        }

    data = request.json
    company_name = data['company_name']
    company_password = data['company_password']
    street_address = data['street_address']
    city = data['city']
    state = data['state']
    zip_code = data['zip_code']
    logo_url = data['logo_url']
    admin_id = user.id

    company = Company.query.filter_by(company_name=company_name).first()
    if company:
        return {
            'status': 'error',
            'message': 'A company with this name already exists. Please choose another name.'
        }

    company = Company(company_name, street_address, city, state, zip_code, company_password)
    company.logo_url = logo_url
    company.admin_id = admin_id

    db.session.add(company)
    db.session.commit()

    user.company_id = company.id
    db.session.commit()
    
    return {
        'status': 'success',
        'message': f'You have successfully created a new Company, {company_name}.',
        'company': company.to_dict()
    }


@company.route('/api/company/update', methods=["POST"])
@token_required
def apiUpdateCompany(user):
    company = Company.query.filter_by(id=user.company_id).first()
    if user.id != company.admin_id and user.company_id != company.id:
        return {
            'status': 'error',
            'message': 'You do not have permission to edit this information.'
        }

    data = request.json
    company.company_name = data['company_name']
    company.company_password = data['company_password']
    company.street_address = data['street_address']
    company.city = data['city']
    company.state = data['state']
    company.zip_code = data['zip_code']
    company.logo_url = data['logo_url']
    
    db.session.commit()
    
    return {
        'status': 'success',
        'message': f'You have successfully updated {company.company_name}.',
        'company': company.to_dict()
    }
