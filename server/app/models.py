from . import db
from flask import current_app, url_for

class Permission:
    VIEW_PRODUCTS = 1
    VIEW_INVENTORY = 2
    VIEW_PRODUCTION_RUN = 4
    MANAGE_PRODUCTS = 8
    MANAGE_INVENTORY = 16
    MANAGE_PRODUCTION_RUN = 32
    VIEW_SALES_REPORT = 64
    MANAGE_SALES_REPORT = 128
    VIEW_RECIPE_DETAILS = 256
    MANAGE_RECIPE_DETAILS = 512
    MANAGER = 1024
    ADMINISTRATOR = 2048


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # role assigned to new users upon registration
    default = db.Column(db.Boolean, default=False, index=True)
    # permissions allowed for different users
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # set the value of permissions to 0 if no initial value is given
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    # add permission
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    # remove permission
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    # reset permission
    def reset_permissions(self):
        self.permissions = 0

    # check if user has permission
    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    # adding roles to the database
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.VIEW_PRODUCTS],

            'Baker': [Permission.VIEW_RECIPE_DETAILS, Permission.MANAGE_RECIPE_DETAILS, Permission.VIEW_PRODUCTS],

            'Sales_Associate': [Permission.VIEW_SALES_REPORT, Permission.MANAGE_SALES_REPORT, Permission.VIEW_INVENTORY, Permission.VIEW_PRODUCTS],

            'Production_Supervisor': [Permission.VIEW_PRODUCTS, Permission.VIEW_PRODUCTION_RUN, Permission.VIEW_INVENTORY, Permission.MANAGE_PRODUCTS, Permission.MANAGE_INVENTORY, Permission.MANAGE_PRODUCTION_RUN],

            'Manager': [Permission.VIEW_PRODUCTS, Permission.VIEW_INVENTORY, Permission.VIEW_PRODUCTION_RUN, Permission.VIEW_SALES_REPORT, Permission.MANAGE_PRODUCTS, Permission.MANAGE_INVENTORY, Permission.MANAGE_PRODUCTION_RUN, Permission.MANAGE_SALES_REPORT, Permission.MANAGER],

            'Administrator': [Permission.VIEW_PRODUCTS, Permission.VIEW_INVENTORY, Permission.VIEW_PRODUCTION_RUN, Permission.MANAGE_PRODUCTS, Permission.MANAGE_INVENTORY, Permission.MANAGE_PRODUCTION_RUN, Permission.VIEW_SALES_REPORT, Permission.MANAGE_SALES_REPORT, Permission.VIEW_RECIPE_DETAILS, Permission.MANAGE_RECIPE_DETAILS, Permission.MANAGER, Permission.ADMINISTRATOR]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_no = db.Column(db.String(13))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    
    routes = db.relationship("Route", backref="sales_agent", lazy="dynamic")

    # assigning roles to users
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['APP_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # role verification
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMINISTRATOR)

    def to_json(self):
        json_user = {
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "phone_no": self.phone_no,
            "role": self.role.name
        }

        return json_user


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(13), unique=True, nullable=False)
    product_name = db.Column(db.String(56), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_description = db.Column(db.Text)

    production_runs = db.relationship('ProductionRuns', backref='product', lazy='dynamic')
    product_recipe = db.relationship('Recipe', backref='product_recipe', lazy='dynamic')
    product_dispatch = db.relationship('DispatchDetails', backref='product_dispatch', lazy='dynamic')
    
    def to_json(self):
        json_product = {
            "Product ID": self.product_id,
            "Product Name": self.product_name,
            "Product Price": self.product_price,
            "Product Description": self.product_description,
        }

        return json_product
    

class ProductionRuns(db.Model):
    __tablename__ = "production_runs"

    id = db.Column(db.Integer, primary_key=True)
    flour_kneaded = db.Column(db.Integer, nullable=False)
    oil_used = db.Column(db.Float, nullable=False)
    packets_produced = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def to_json(self):
        json_productionRun = {
            "Product Name": self.product.product_name,
            "Flour Kneaded": self.flour_kneaded,
            "Oil Used": self.oil_used,
            "Packets Produced": self.packets_produced
        }

        return json_productionRun
    

class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.String(13), unique=True, nullable=False)
    ingredient_name = db.Column(db.String(50), unique=True, nullable=False)
    ingredient_quantity = db.Column(db.Integer, nullable=False)
    ingredient_measurement = db.Column(db.Integer, nullable=False)
    ingredient_cost = db.Column(db.Float, nullable=False)

    recipe_association = db.relationship('RecipeIngredient', backref='recipe_association', lazy='dynamic')

    def to_json(self):
        json_ingredient = {
            "Ingredient Id": self.ingredient_id,
            "Ingredient Name": self.ingredient_name,
            "Unit of Measurement": str(self.ingredient_quantity) + " " + self.ingredient_measurement,
            "Ingredient Cost": self.ingredient_cost
        }

        return json_ingredient
    

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    description = db.Column(db.Text)
    yield_amount = db.Column(db.Integer, nullable=False)

    recipe_ingredients = db.relationship('RecipeIngredient', backref="recipe", lazy='dynamic')

    def to_json(self):
        ingredient_details = []

        for ingredient in self.recipe_ingredients:
            ingredient_details.append({
                "Ingredient Name": ingredient.recipe_association.ingredient_name,
                "Quantity": ingredient.quantity,
                "Unit of Measurement": ingredient.unit_of_measurement
            })

        json_recipe = {
            "Product Name": self.product_recipe.product_name,
            "Yield Amount": self.yield_amount,
            "Description": self.description,
            "Recipe Details": ingredient_details
        }

        return json_recipe


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"))
    quantity = db.Column(db.Float, nullable=False)
    unit_of_measurement = db.Column(db.String(12))


    def to_json(self):
        json_recipeIngredient = {
            "Recipe Name": self.recipe.product_recipe.product_name,
            "Ingredient Name": self.recipe_association.ingredient_name,
            "Quantity": self.quantity,
            "Unit of measurement": self.unit_of_measurement
        }

        return json_recipeIngredient
    

class Route(db.Model):
    __tablename__ = "routes"

    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(26))
    sales_associate_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    customers = db.relationship('Customer', lazy='dynamic', backref="cust_route")
    dispatches = db.relationship('Dispatch', lazy='dynamic', backref='route_dispatch')

    def to_json(self):
        json_route = {
            "Route Name": self.route_name,
            "Sales Agent": self.sales_agent.name
        }

        return json_route


class Customer(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(128))
    customer_email = db.Column(db.String(128))
    customer_phone_no = db.Column(db.Integer)
    customer_mpesa_agent_name = db.Column(db.String(128))
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"))

    def to_json(self):
        json_customer = {
            "Customer Name": self.customer_name,
            "Customer Email": self.customer_email,
            "Customer Phone": self.customer_phone_no,
            "Agent Name": self.customer_mpesa_agent_name
        }

        return json_customer


class Dispatch(db.Model):
    __tablename__ = "dispatches"

    id = db.Column(db.Integer, primary_key=True)
    dispatch_date = db.Column(db.DateTime())
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"))

    dispatch_details = db.relationship('DispatchDetails', backref='dispatches', lazy='dynamic')

    def to_json(self):
        json_dispatch = {
            "Dispatch Date": self.dispatch_date,
            "Route Name": self.route_id
        }
        return json_dispatch


class DispatchDetails(db.Model):
    __tablename__ = "dispatch_details"

    id = db.Column(db.Integer, primary_key=True)
    dispatch_id = db.Column(db.Integer, db.ForeignKey("dispatches.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Float)
    returns = db.Column(db.Float)

    def to_json(self):
        json_dispatch_details = {
            "Dispatch Id": self.dispatch_id,
            "Product Id": self.product_id,
            "Quantity": self.quantity,
            "Returns": self.returns
        }