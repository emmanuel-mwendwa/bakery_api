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