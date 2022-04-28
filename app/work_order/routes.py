from flask import Blueprint, request

# models
from app.models import WorkOrder, Customer, System, db
from app.token_required import token_required

# blueprint
work_order = Blueprint('work_order', __name__, template_folder='work_order_templates')

@work_order.route('/api/customers/<int:customer_id>/systems/<int:system_id>/work-order-list')
@token_required
def apiSystemWorkOrderList(customer_id, system_id, user):
    work_orders = WorkOrder.query.filter_by(system_id=system_id).all()

    return {
        'status': 'success',
        'total_results': len(work_orders),
        'work_order': [w.to_dict() for w in work_orders][:-10:-1]
    }

@work_order.route('/api/recent/work-order-list')
@token_required
def apiRecentUserWorkOrderList(user):
    work_orders = WorkOrder.query.filter_by(user_id=user.id).all()

    return {
        'status': 'success',
        'total_results': len(work_orders),
        'work_order': [w.to_dict() for w in work_orders][::-1]
    }

@work_order.route('/api/customers/<int:customer_id>/work-order-list')
@token_required
def apiRecentCustomerWorkOrderList(customer_id, user):
    work_orders = WorkOrder.query.filter_by(customer_id=customer_id).all()
    
    return {
        'status': 'success',
        'total_results': len(work_orders),
        'work_order': [w.to_dict() for w in work_orders][::-1]
    }

@work_order.route('/api/customers/<int:customer_id>/systems/<int:system_id>/work-order/<int:work_order_id>')
@token_required
def apiWorkOrderInfo(customer_id, system_id, work_order_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()
    if user.id != customer.user_id and user.company_id != customer.company_id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this customer information.'
        }
    
    work_order = WorkOrder.query.filter_by(id=work_order_id).first()
    if work_order:
        return {
            'status': 'success',
            'message': 'Work Order info retrieved',
            'work_order': work_order.to_dict()
        }
    else:
        return {
            'status': 'error',
            'message': 'Error retrieving work order information'
        }

@work_order.route('/api/customers/<int:customer_id>/systems/<int:system_id>/create-work-order', methods=["POST"])
@token_required
def apiCreateWorkOrder(customer_id, system_id, user):
    system = System.query.filter_by(id=system_id).first()
    customer = Customer.query.filter_by(id=customer_id).first()

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

    user_id = user.id
    customer_id = customer_id
    system_id = system.id
    order_type = data['order_type']
    work_performed = data['work_performed']

    work_order = WorkOrder(user_id, customer_id, system_id, order_type, work_performed)

    db.session.add(work_order)
    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully created a new {order_type} work order.',
        'work_order': work_order.to_dict()
    }

@work_order.route('/api/customers/<int:customer_id>/systems/<int:system_id>/work-order/<int:work_order_id>/edit', methods=["POST"])
@token_required
def apiUpdateWorkOrder(customer_id, system_id, work_order_id, user):
    system = System.query.filter_by(id=system_id).first()
    customer = Customer.query.filter_by(id=customer_id).first()
    work_order = WorkOrder.query.filter_by(id=work_order_id).first()

    if (system is None) or (customer is None) or (work_order is None):
        return {
            'status': 'error',
            'message': 'No work order found.'
        }
    if user.id != customer.user_id and user.company_id != customer.company_id:
        return {
            'status': 'error',
            'message': 'You do not have access to edit this customer information.'
        }
    
    
    data = request.json

    work_order.order_type = data['order_type']
    work_order.work_performed = data['work_performed']

    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully update {customer.name}\'s Work Order.',
        'work_order': work_order.to_dict()
    }

@work_order.route('/api/customers/<int:customer_id>/systems/<int:system_id>/work-order/delete/<int:work_order_id>', methods=["POST"])
@token_required
def apiDeleteWorkOrder(customer_id, system_id, work_order_id, user):
    customer = Customer.query.filter_by(id=customer_id).first()
    system = System.query.filter_by(id=system_id).first()
    work_order = WorkOrder.query.filter_by(id=work_order_id).first()

    if (system is None) or (customer is None) or (work_order is None):
        return {
            'status': 'error',
            'message': 'No order found.'
        }
    # if (user.id != customer.user_id and user.company_id != customer.company_id) or system.customer_id != customer.id:
    #     return {
    #         'status': 'error',
    #         'message': 'You do not have access to edit this information.'
    #     }

    db.session.delete(work_order)
    db.session.commit()

    return {
        'status': 'success',
        'message': f'You have successfully deleted {customer.name}\'s work order.'
    }