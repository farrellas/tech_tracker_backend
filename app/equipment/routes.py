from flask import Blueprint, request

# models
from app.models import Equipment, Customer, System, db
from app.token_required import token_required

# blueprint
equipment = Blueprint('equipment', __name__, template_folder='equipment_templates')

@equipment.route('/api/customers/<int:customer_id>/system-list')
@token_required
def apiSystemList(customer_id, user):
    systems = System.query.filter_by(customer_id=customer_id).all()
    return {
        'status': 'success',
        'total_results': len(systems),
        'systems': [s.to_dict() for s in systems]
    }

@equipment.route('/api/customers/<int:customer_id>/systems/<int:system_id>')
@token_required
def apiSystemInfo(customer_id, system_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()
    if user.id != customer.user_id and user.company_id != customer.company_id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this customer information.'
        }
    system = System.query.filter_by(id=system_id).first()
    if system:
        return {
            'status': 'success',
            'message': 'System info retrieved',
            'system': system.to_dict()
        }
    else:
        return {
            'status': 'error',
            'message': 'Error retrieving system information'
        }

@equipment.route('/api/customers/<int:customer_id>/systems/create', methods=["POST"])
@token_required
def apiCreateSystem(customer_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()
    if user.id != customer.user_id and user.company_id != customer.company_id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this customer information.'
        }

    data = request.json
    print(data)
    name = data['name']
    area_served = data['area_served']
    system_type = data['system_type']
    heating = data['heating']
    cooling = data['cooling']
    notes = data['notes']

    system = System(name, area_served, system_type, heating, cooling, notes, customer_id)

    db.session.add(system)
    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully created a new System, {name}.',
        'system': system.to_dict()
    }

@equipment.route('/api/customers/<int:customer_id>/systems/<int:system_id>/edit', methods=["POST"])
@token_required
def apiUpdateSystem(customer_id, system_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()
    system = System.query.filter_by(id=system_id).first()

    if (system is None) or (customer is None):
        return {
            'status': 'error',
            'message': 'No system found.'
        }
    if user.id != customer.user_id and user.company_id != customer.company_id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this customer information.'
        }

    data = request.json
    print(data)
    system.name = data['name']
    system.area_served = data['area_served']
    system.system_type = data['system_type']
    system.heating = data['heating']
    system.cooling = data['cooling']
    system.notes = data['notes']

    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully updated {system.name}.',
        'system': system.to_dict()
    }

@equipment.route('/api/customers/<int:customer_id>/systems/delete/<int:system_id>', methods=["POST"])
@token_required
def apiDeleteSystem(customer_id, system_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()
    system = System.query.filter_by(id=system_id).first()

    if (system is None) or (customer is None):
        return {
            'status': 'error',
            'message': 'No system found.'
        }
    if user.id != customer.user_id and user.company_id != customer.company_id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this customer information.'
        }

    db.session.delete(system)
    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully deleted {system.name}.'
    }

@equipment.route('/api/customers/<int:customer_id>/systems/<int:system_id>/equipment-list')
@token_required
def apiEquipmentList(customer_id, system_id, user):
    equipment = Equipment.query.filter_by(system_id=system_id).all()

    return {
        'status': 'success',
        'total_results': len(equipment),
        'equipment': [e.to_dict() for e in equipment]
    }

@equipment.route('/api/customers/<int:customer_id>/systems/<int:system_id>/equipment/<int:equipment_id>')
@token_required
def apiEquipmentInfo(customer_id, system_id, equipment_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()
    if user.id != customer.user_id and user.company_id != customer.company_id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this customer information.'
        }
    
    equipment = Equipment.query.filter_by(id=equipment_id).first()
    if equipment:
        return {
            'status': 'success',
            'message': 'System info retrieved',
            'equipment': equipment.to_dict()
        }
    else:
        return {
            'status': 'error',
            'message': 'Error retrieving equipment information'
        }

@equipment.route('/api/customers/<int:customer_id>/systems/<int:system_id>/create-equipment', methods=["POST"])
@token_required
def apiCreateEquipment(customer_id, system_id, user):
    system = System.query.filter_by(id=system_id).first()
    customer = Customer.query.filter_by(id=customer_id).first()

    if (system is None) or (customer is None):
        return {
            'status': 'error',
            'message': 'No system found.'
        }
    if (user.id != customer.user_id and user.company_id != customer.company_id) or system.customer_id != customer.id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this customer information.'
        }
    
    data = request.json

    equipment_class = data['equipment_class']

    brand = data['brand']
    model_no = data['model_no']
    serial_no = data['serial_no']
    year = data['year']
    equipment_type = data['equipment_type']
    notes = data['notes']
    fuel_type = data['fuel_type']
    refrigerant_type = data['refrigerant_type']

    equipment = Equipment(brand, model_no, serial_no, year, equipment_type, notes, system.id, fuel_type, refrigerant_type)

    db.session.add(equipment)
    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully created new {equipment_class} Equipment.',
        'equipment': equipment.to_dict()
    }

@equipment.route('/api/customers/<int:customer_id>/systems/<int:system_id>/equipment/<int:equipment_id>/edit', methods=["POST"])
@token_required
def apiUpdateEquipment(customer_id, system_id, equipment_id, user):
    system = System.query.filter_by(id=system_id).first()
    customer = Customer.query.filter_by(id=customer_id).first()
    equipment = Equipment.query.filter_by(id=equipment_id).first()

    if (system is None) or (customer is None) or (equipment is None):
        return {
            'status': 'error',
            'message': 'No equipment found.'
        }
    if (user.id != customer.user_id and user.company_id != customer.company_id) or system.customer_id != customer.id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this customer information.'
        }
    
    data = request.json

    equipment.equipment_class = data['equipment_class']
    equipment.brand = data['brand']
    equipment.model_no = data['model_no']
    equipment.serial_no = data['serial_no']
    equipment.year = data['year']
    equipment.equipment_type = data['equipment_type']
    equipment.notes = data['notes']
    equipment.fuel_type = data['fuel_type']
    equipment.refrigerant_type = data['refrigerant_type']

    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully update {customer.name}\'s Equipment.',
        'equipment': equipment.to_dict()
    }

@equipment.route('/api/customers/<int:customer_id>/systems/<int:system_id>/equipment/delete/<int:equipment_id>', methods=["POST"])
@token_required
def apiDeleteEquipment(customer_id, system_id, equipment_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()
    system = System.query.filter_by(id=system_id).first()
    equipment = Equipment.query.filter_by(id=equipment_id).first()

    if (system is None) or (customer is None) or (equipment is None):
        return {
            'status': 'error',
            'message': 'No system found.'
        }
    if (user.id != customer.user_id and user.company_id != customer.company_id) or system.customer_id != customer.id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this information.'
        }

    db.session.delete(equipment)
    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully deleted {customer.name}\'s equipment.'
    }