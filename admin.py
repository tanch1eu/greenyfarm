from flask import Blueprint
from . import db
from .models import Product, Item, Order
import datetime


bp = Blueprint('admin', __name__, url_prefix='/admin/')

# function to put some seed data in the database
@bp.route('/dbseed/')
def dbseed():
    product1 = Product(name='Milk', image='milkImg1.jpg', \
        description='Milk is a nutrient-rich beverage that may benefit your health in several ways. Drinking milk and dairy products may prevent osteoporosis and bone fractures and even help you maintain a healthy weight.')
    product2 = Product(name='Vitamin', image='vitaminImg2.jpg', \
        description='Vitamins and minerals are considered essential nutrients — they perform hundreds of roles in the body. They help shore up bones, heal wounds, and bolster your immune system. They also convert food into energy, and repair cellular damage.')
    try:
        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()
    except:
        return 'There was an issue adding the product lines in dbseed function'

    i1 = Item(product_id = product1.id, image='a2milk.png', price=109.99,\
        name='A2 milk powder 1kg-pack',\
        description= 'A2 milk is the milk produced by Desi Cows who have only A2 beta-casein protein. There are 2 kinds of proteins in cow milk – A1 and A2, which differ by one single amino acid. Yet, this one difference can change the way the milk is digested in the human body. A2 is the original protein that is present in cows since the beginning. In fact, all other mammals including humans produce A2 milk only.') 
    
    i2 = Item(product_id = product1.id, image='milo.jpg', price=229.99,\
        name='Nestle Milo 1kg-pack',\
        description= '''Tasty and trusted, Milo brand is the world’s leading chocolate malt beverage that can be prepared with hot or cold milk or water. It offers essential vitamins and minerals to meet the nutrition and energy demands of young bodies and minds. Launched in Australia in the early 1930s, the Milo brand takes kids' development seriously. It has long been known as an energy beverage strongly associated with sports and good health.''')
    
    i3 = Item(product_id = product1.id, image='organic.jpg', price=370.99,\
        name='NOD Organic formula milk 6-12 months',\
        description= 'By choosing organic milk, you can get the nutritional benefits of milk without exposing your family to chemical contaminants. Numerous studies have found that organic milk has a higher nutritional content, and even more healthy omega-3 fatty acids, and more disease-fighting antioxidants than non-organic milk.') 

    i4 = Item(product_id = product1.id, image='glucerna.jpg', price=450.99,\
        name='Abbott Glucerna',\
        description= 'Glucerna is designed to provide the body with carbohydrates that are slower digesting, much like low-GI foods. For best nutrition, balance your diet with low-GI foods, using products like Glucerna only occasionally. The protein in Glucerna products may also be helpful for type 2 diabetes.') 

    i5 = Item(product_id = product1.id, image='ensure.jpg', price=420.99,\
        name='Abbott Ensure',\
        description= 'Ensure has been carefully formulated to include all the key ingredients for a nutritionally-balanced health drink. In addition, as a source of energy and high-quality protein, Ensure includes 28 essential vitamins and minerals to help keep you strong and healthy.')

    i6 = Item(product_id = product2.id, image='vitaminD3.jpg', price=30.99,\
        name='Progetic Vitamin D3',\
        description= 'Vitamin D (ergocalciferol-D2, cholecalciferol-D3, alfacalcidol) is a fat-soluble vitamin that helps your body absorb calcium and phosphorus. Having the right amount of vitamin D, calcium, and phosphorus is important for building and keeping strong bones.')

    i7 = Item(product_id = product2.id, image='glucosamine.jpg', price=40.99,\
        name='Progetic Glucosamine',\
        description= 'Glucosamine is a chemical compound that occurs naturally in both human and animal tissues. In humans, it helps form cartilage and is commonly used as a dietary supplement to treat joint disorders like osteoarthritis.')

    i8 = Item(product_id = product2.id, image='multivitamin.jpg', price=45.99,\
        name='Progetic Multivitamin',\
        description= 'Good for your heart: Studies show that taking a high-quality multivitamin may reduce cardiovascular disease. Heart disease is the leading cause of death in both men and women in the U.S. Vitamins B1, B2, B6, K1, Niacin (B3), CoQ10 and magnesium, all play a role in cardiovascular health.')

    try:
        db.session.add(i1)
        db.session.add(i2)
        db.session.add(i3)
        db.session.add(i4)
        db.session.add(i5)
        db.session.add(i6)
        db.session.add(i7)
        db.session.add(i8)       
        db.session.commit()
    except:
        return 'There was an issue adding a tour in dbseed function'

    return 'DATA LOADED'


