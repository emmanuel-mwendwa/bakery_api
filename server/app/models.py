from . import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(13), unique=True, nullable=False)
    product_name = db.Column(db.String(56), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_description = db.Column(db.Text)

    production_runs = db.relationship('ProductionRuns', backref='product', lazy='dynamic')
    
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

    def to_json(self):
        json_ingredient = {
            "Ingredient Id": self.ingredient_id,
            "Ingredient Name": self.ingredient_name,
            # "Ingredient Quantity": self.ingredient_quantity,
            "Unit of Measurement": str(self.ingredient_quantity) + " " + self.ingredient_measurement,
            "Ingredient Cost": self.ingredient_cost
        }

        return json_ingredient