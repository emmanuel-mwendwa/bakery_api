from . import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(56), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def to_json(self):
        json_product = {
            "name": self.name,
            "price": self.price
        }

        return json_product