from . import sales
from .. import db
from ..models import Customer, Route, User, Dispatch, DispatchDetails, Product
from flask import request, jsonify
import datetime


class RoutesRoutes:
    @sales.post("/routes")
    def new_route():
        data = request.get_json()
        sales_agent = User.query.get(data.get("sales_associate_id"))
        if not sales_agent:
            return jsonify({"message": "Sales Agent not found"})
        new_route = Route(
            route_name = data.get("route_name"),
            sales_associate_id = data.get("sales_associate_id")
        )

        db.session.add(new_route)
        db.session.commit()
        return jsonify({"message": [
            {"data": "Route created successfully"},
            {"route": new_route.to_json()}
        ]})
    
    @sales.get("/routes")
    def view_routes():
        routes = Route.query.all()
        routes_list = []

        for route in routes:
            routes_list.append(route.to_json())
        return jsonify(routes_list)
    
    @sales.get("/routes/<int:id>")
    def view_route(id):
        route = Route.query.get(id)
        if not route:
            return jsonify({"message": "Route not found"})
        
        return jsonify(route.to_json())
    
    @sales.put("/routes/<int:id>")
    def update_route(id):
        data = request.get_json()
        route = Route.query.get(id)

        if not route:
            return jsonify({"message": "Route not found"})

        route.route_name = data.get("route_name")
        route.sales_associate_id = data.get("sales_associate_id")
        
        db.session.add(route)
        db.session.commit()

        return jsonify({"message": [
            {"data": "Route updated successfully"},
            {"route": route.to_json()}
            ]
        })
    
    @sales.delete("/routes/<int:id>")
    def delete_route(id):
        route = Route.query.get(id)
        if not route:
            return jsonify({"message": "Route not found"})
        
        db.session.delete(route)
        db.session.commit()
        return jsonify({"message": "Route deleted successfully"})

class CustomerRoutes:
    @sales.post("/customers")
    def new_customer():
        data = request.get_json()
        new_customer = Customer(
            customer_name = data.get("customer_name"),
            customer_email = data.get("customer_email"),
            customer_phone = data.get("customer_phone"),
            customer_agent_name = data.get("customer_agent_name")
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"message": [
            {"data": "Customer added successfully"},
            {"customer": new_customer.to_json()}
            ]
        })
    
    @sales.get("/customers")
    def view_customers():
        customers = Customer.query.all()
        customers_list = []
        
        for customer in customers:
            customers_list.append(customer.to_json())
        
        return jsonify({customers_list})
    
    @sales.get("/customers/<int:id>")
    def view_customer(id):
        customer = Customer.query.get(id)
        if not customer:
            return jsonify({"message": "Customer not found"})
        
        return jsonify(customer.to_json())
    
    @sales.put("/customers/<int:id>")
    def update_customer(id):
        data = request.get_json()
        customer = Customer.query.get(id)

        if not customer:
            return jsonify({"message": "Customer not found"})

        customer.customer_name = data.get("customer_name")
        customer.customer_email = data.get("customer_email")
        customer.customer_phone = data.get("customer_phone")
        customer.customer_agent_name = data.get("customer_agent_name")
        
        db.session.add(customer)
        db.session.commit()

        return jsonify({"message": [
            {"data": "Customer updated successfully"},
            {"customer": customer.to_json()}
            ]
        })
    
    @sales.delete("/customers/<int:id>")
    def delete_customer(id):
        customer = Customer.query.get(id)
        if not customer:
            return jsonify({"message": "Customer not found"})
        
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted successfully"})
    

class DispatchRoutes:
    @sales.post("/dispatches")
    def new_dispatch():
        data = request.get_json()
        route = Route.query.get(data.get("route_id"))
        if not route:
            jsonify({"message": "Route not found"})
        new_disptach = Dispatch(
            dispatch_date = datetime.datetime.utcnow(),
            route_id = data.get("route_id")
        )

        db.session.add(new_disptach)
        db.session.commit()
        return jsonify({"message": "Dispatch created successfully!"})

    @sales.get("/dispatches")
    def view_disptaches():
        dispatches = Dispatch.query.all()
        dispatches_list = []

        for dispatch in dispatches:
            dispatches_list.append(dispatch.to_json())

        return jsonify(dispatches_list)
    
    @sales.get("/dispatches/<int:id>")
    def view_dispatch(id):
        dispatch = Dispatch.query.get(id)
        if not dispatch:
            return jsonify({"message": "Dispatch not found"})
        return jsonify(dispatch.to_json())
    
    @sales.put("/dispatches/<int:id>")
    def update_dispatch(id):
        data = request.get_json()
        dispatch = Dispatch.query.get(id)

        if not dispatch:
            return jsonify({"message": "Dispatch not found"})

        dispatch.dispatch_date = datetime.datetime.utcnow()
        dispatch.route_id = data.get("route_id")
        
        db.session.add(dispatch)
        db.session.commit()

        return jsonify({"message": [
            {"data": "Dispatch updated successfully"},
            {"dispatch": dispatch.to_json()}
            ]
        })
    
    @sales.delete("/dispatches/<int:id>")
    def delete_dispatch(id):
        dispatch = Dispatch.query.get(id)
        if not dispatch:
            return jsonify({"message": "Dispatch not found"})
        
        db.session.delete(dispatch)
        db.session.commit()
        return jsonify({"message": "Dispatch deleted successfully"})