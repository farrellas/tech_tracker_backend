# from flask import Blueprint, redirect, render_template, request, url_for


# logs = Blueprint('logs', __name__, template_folder='logs_templates')

# from .forms import CreateCustomerForm, UpdateCustomerForm, CreateLogForm, UpdateLogForm
# from app.models import db, MaintenanceLog, Customer

# @logs.route('/user_logs')
# @login_required
# def userLogs():
#     if current_user.company_id:
#         customers = Customer.query.filter_by(company_id=current_user.company_id).all()
#     else:
#         customers = Customer.query.filter_by(user_id=current_user.id).all()
#     if not customers:
#         print(customers)
#         return render_template('no_customers.html')
#     else:
#         return render_template('user_logs.html', customers=customers)
        

# @logs.route('/create-customer', methods=["GET","POST"])
# @login_required
# def createCustomer():
#     form = CreateCustomerForm()
#     if request.method == "POST":
#         if form.validate():
#             name = form.name.data
#             address = form.address.data
#             email = form.email.data

#             customer = Customer(name, address, email, current_user.id)

#             db.session.add(customer)
#             db.session.commit()

#             return redirect(url_for('home'))
#     return render_template('create_customer.html', form=form)

# @logs.route('/customers/<int:customer_id>')
# @login_required
# def customerInfo(customer_id):
#     customer = Customer.query.filter_by(id=customer_id).first()
#     reports = MaintenanceLog.query.filter_by(customer_id=customer_id).all()[::-1]
#     if customer is None:
#         return redirect(url_for('logs.userLogs'))
#     return render_template('customer_info.html', customer=customer, reports=reports)

# @logs.route('/customers/update/<int:customer_id>', methods=["GET","POST"])
# @login_required
# def updateCustomer(customer_id):
#     customer = Customer.query.filter_by(id=customer_id).first()
#     if customer is None:
#         return redirect(url_for('logs.userLogs'))
#     if customer.user_id != current_user.id:
#         return redirect(url_for('logs.userLogs'))
#     form = UpdateCustomerForm()
#     if request.method == "POST":
#         if form.validate():
#                 name = form.name.data
#                 address = form.address.data
#                 email = form.email.data

#                 customer.name= name
#                 customer.address = address
#                 customer.email = email

#                 db.session.commit()
#                 return redirect(url_for('home'))
#     return render_template('update_customer.html', form=form, customer=customer, customer_id=customer_id)

# @logs.route('/customers/delete/<int:customer_id>', methods=["POST"])
# @login_required
# def deleteCustomer(customer_id):
#     customer = Customer.query.filter_by(id=customer_id).first()
#     if customer is None:
#         return redirect(url_for('logs.userLogs'))
#     if customer.user_id != current_user.id:
#         return redirect(url_for('logs.userLogs'))

#     db.session.delete(customer)
#     db.session.commit()
#     return redirect(url_for('logs.userLogs'))

# @logs.route('/create-log/<int:customer_id>', methods=["GET","POST"])
# @login_required
# def createLog(customer_id):
#     form = CreateLogForm()
#     if request.method == "POST":
#         if form.validate():
#             work_performed = form.work_performed.data

#             log = MaintenanceLog(customer_id, work_performed)

#             db.session.add(log)
#             db.session.commit()

#             return redirect(url_for('logs.customerInfo', customer_id=customer_id))
#     return render_template('create_log.html', form=form, customer_id=customer_id)

# @logs.route('/logs/<int:log_id>')
# @login_required
# def logInfo(log_id):
#     log = MaintenanceLog.query.filter_by(id=log_id).first()
#     if log is None:
#         return redirect(url_for('logs.userLogs'))
#     return render_template('log_info.html', log=log, customer_id=log.customer_id)

# @logs.route('/logs/update/<int:log_id>', methods=["GET","POST"])
# @login_required
# def updateLog(log_id):
#     log = MaintenanceLog.query.filter_by(id=log_id).first()
#     if log is None:
#         return redirect(url_for('logs.userLogs'))
#     form = UpdateLogForm()
#     if request.method == "POST":
#         if form.validate():
#                 work_performed = form.work_performed.data

#                 log.work_performed = work_performed

#                 db.session.commit()
#                 return redirect(url_for('logs.customerInfo', customer_id=log.customer_id))
#     return render_template('update_log.html', form=form, log=log, customer_id=log.customer_id)

# @logs.route('/logs/delete/<int:log_id>', methods=["POST"])
# @login_required
# def deleteLog(log_id):
#     log = MaintenanceLog.query.filter_by(id=log_id).first()
#     if log is None:
#         return redirect(url_for('logs.userLogs'))

#     db.session.delete(log)
#     db.session.commit()
#     return redirect(url_for('logs.userLogs'))