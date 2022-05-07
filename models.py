from . import db

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'default1.jpg')
    items = db.relationship('Item', backref = 'Product', cascade = "all, delete-orphan")

    #def get_product_details(self):
        #return str(self)

    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {} \n" 
        str =str.format( self.id, self.name,self.description,self.image)
        return str

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('item_id',db.Integer,db.ForeignKey('items.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'item_id') )

class Item(db.Model):
    # def __init__(self, id, name, description, image, price, product, date):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.image = image
    #     self.price = price
    #     self.product = product
    #     self.date = date
    __tablename__='items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    #date = db.Column(db.DateTime, nullable=False)
    #quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    
    # def get_item_details(self):
    #     return str(self)

    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {}, Price: {}, Product: {}\n" 
        str =str.format( self.id, self.name,self.description,self.image, self.price, self.product_id)
        return str

class Order(db.Model):
    # def __init__(self, id, status, firstname, surname, email, phone, date, items, total_cost):
    #     self.id = id
    #     self.status = status
    #     self.firstname = firstname
    #     self.surname = surname
    #     self.email = email
    #     self.phone = phone
    #     self.date = date
    #     self.items = items
    #     self.total_cost = total_cost

    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    #date = db.Column(db.DateTime)
    items = db.relationship("Item", secondary=orderdetails, backref="orders")
    
    def get_item_details(self):
        return str(self)

    def __repr__(self):
        str = "id: {}, Status: {}, Firstname: {}, Surname: {}, Email: {}, Phone: {}, Items: {}, Total Cost: {}\n" 
        str =str.format( self.id, self.status,self.firstname,self.surname, self.email, self.phone, self.items, self.total_cost)
        return str