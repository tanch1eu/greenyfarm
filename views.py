from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Product, Item, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db

# # This data will eventually be stored in a database
# milk = Product('1', 'Milk', 'Perfect milk for your daily essentials.', 'milkImg1.jpg')
# vitamin = Product('2', 'Vitamin', 'Nutrients for a wonderful life style.', 'vitaminImg2.jpg')
# item1 = Item('1', 'A2 Milk powder 1kg', 'Premium branded dairy nutritional company uniquely focused on products containing the A2 beta-casein protein type.', 'a2milk.png', 100.45, milk, datetime(2020,7,23))
# item2 = Item('2', 'Nestle Milo 1kg', 'A nutrient rich, low GI drink which gives kids the nourishing energy they need to take on the day.', 'milo.jpg', 200.00, milk, datetime(2019,10,30))
# item3 = Item('3', 'Progetic Vitamin D3', 'Visit Straddy and see the whales migrating', 'vitaminD3.jpg', 30.00, vitamin, datetime(2019,10,30))
# products = [milk, vitamin]
# items = [item1,item2,item3]
# order1 = Order('1', False, '', '','', '', datetime.now(), [item1, item2], item1.price+item2.price) # simulating order not checked out
# order2 = Order('2', False, '', '','', '', datetime.now(), [item1, item3], item1.price+item3.price) # simulating order not checked out
# orders = [order1,order2]

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    products = Product.query.order_by(Product.name).all()
    return render_template('index.html', products = products)

@bp.route('/about')
def about():
    return render_template('aboutus.html')

@bp.route('/items/')
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search)
    items = Item.query.filter(Item.description.like(search)).all()
    return render_template('productItems.html', items = items)

@bp.route('/items/<int:productid>/')
# def productItems(productid):
#     productItems = []
#     # create list of items for this product
#     for item in items:
#             if int(item.product.id) == int(productid): 
#                 productItems.append(item)
#     return render_template('productItems.html', items = productItems)

def productItems(productid):
    items = Item.query.filter(Item.product_id == productid)
    return render_template('productItems.html', items = items)

# Referred to as "Basket" to the user
@bp.route('/order/', methods=['POST','GET'])
# def order():

#     item_id = request.args.get('item_id')
#     # is this a new order?
#     if 'order_id'not in session:
#         session['order_id'] = 1 # arbitry, we could set either order 1 or order 2
    
#     #retrieve correct order object
#     for x in orders:
#             if int(x.id) == int(session['order_id']): 
#                 order = x
#     # are we adding an item? - will be implemented later with DB
#     if item_id:
#         print('user requested to add item id = {}'.format(item_id))

#     return render_template('order.html', order = order, totalprice = order.total_cost)

def order():
    item_id = request.values.get('item_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None
    
    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0)
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for item in order.items:
            totalprice = totalprice + item.price

    # are we adding an item?
    if item_id is not None and order is not None:
        item = Item.query.get(item_id)
        if item not in order.items:
            try:
                order.items.append(item)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('item already in basket')
            return redirect(url_for('main.order'))

    return render_template('order.html', order = order, totalprice = totalprice)

# @bp.route('/deleteorder/')
# def deleteorder():
#     if 'order_id' in session:
#         del session['order_id']
#     return render_template('index.html')

# @bp.route('/deleteorderitem/', methods=['POST'])
# def deleteorderitem():
#     print('User wants to delete item with id={}'.format(request.form['id']))
#     return render_template('index.html')

# Delete specific basket items
@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        item_to_delete = Item.query.get(id)
        try:
            order.items.remove(item_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket
@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))



@bp.route('/checkout/', methods=['POST','GET'])
#def checkout():
    # form = CheckoutForm() 
    # if 'order_id' in session:
        
    #     #retrieve correct order object
    #     for x in orders:
    #             if int(x.id) == int(session['order_id']): 
    #                 order = x
       
    #     if form.validate_on_submit():
    #         order.status = True
    #         order.firstname = form.firstname.data
    #         order.surname = form.surname.data
    #         order.email = form.email.data
    #         order.phone = form.phone.data
    #         print(order)
    #         flash('Thank you for your information')

    # return render_template('checkout.html', form = form)
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for item in order.items:
                totalcost = totalcost + item.price
            order.totalcost = totalcost
            #order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! One of our awesome team members will contact you soon...')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form = form)