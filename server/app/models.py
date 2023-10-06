from . import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(13), unique=True, nullable=False)
    product_name = db.Column(db.String(56), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_description = db.Column(db.Text)

    production_runs = db.relationship('ProductionRuns', backref='product', lazy='dynamic')
    product_recipe = db.relationship('Recipe', backref='product_recipe', lazy='dynamic')
    
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
    

class Customer(db.Model):
    __tablename__ = "customers"

    cust_id = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(128))
    cust_email = db.Column(db.String(128))
    cust_phone_no = db.Column(db.Integer)
    cust_mpesa_agent_name = db.Column(db.String(128))

