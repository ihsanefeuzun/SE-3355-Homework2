from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_no = db.Column(db.Integer)
    description = db.Column(db.String(255))
    price = db.Column(db.Integer)
    city = db.Column(db.String(50))
    image = db.Column(db.String(255))
    category = db.Column(db.String(50))

with app.app_context():
    db.create_all()

products_data = [
    {"ad_no": 1, "description": "Very cheap, perfect car from owner", "price": 150000, "city": "İstanbul", "image": "car1.jpg", "category": "Car"},
    {"ad_no": 2, "description": "Super car from car gallery with a great price", "price": 200000, "city": "İzmir", "image": "car2.jpg", "category": "Car"},
    {"ad_no": 3, "description": "Fastest sport car in the world you can get", "price": 175000, "city": "İzmir", "image": "car3.jpg", "category": "Car"},
    {"ad_no": 4, "description": "Clean used motorcyle from owner", "price": 10000, "city": "Ankara", "image": "motorcycle1.jpg", "category": "Motorcycle"},
    {"ad_no": 5, "description": "Well-maintained, new model ATV", "price": 130000, "city": "Antalya", "image": "atv1.jpg", "category": "ATV"},
    {"ad_no": 6, "description": "The house that makes your dream come true", "price": 2000000.0, "city": "Edirne", "image": "house1.jpg", "category": "House"},
    {"ad_no": 7, "description": "Super house from owner, you would love", "price": 3000000.0, "city": "Edirne", "image": "house2.jpg", "category": "House"},
    {"ad_no": 8, "description": "Excellent house with a great view", "price": 4000000.0, "city": "İzmir", "image": "house3.jpg", "category": "House"},
    {"ad_no": 9, "description": "Great office for your business", "price": 2000000.0, "city": "İstanbul", "image": "office1.jpg", "category": "Office"},
    {"ad_no": 10, "description": "Low priced land on a high productive plain", "price": 5000000.0, "city": "Konya", "image": "plot1.jpg", "category": "Plot"},
]

with app.app_context():
    for product_data in products_data:
        product = Product.query.filter_by(ad_no=product_data['ad_no']).first()
        if product is None:
            product = Product(**product_data)
            db.session.add(product)
    db.session.commit()

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        products = search_products(keyword)
    else:
        products = Product.query.all()
        keyword = ''

    categories_with_counts = db.session.query(Product.category, db.func.count(Product.id)).group_by(Product.category).all()

    return render_template("home.html", products=products, keyword=keyword, categories_with_counts=categories_with_counts)

def search_products(keyword):
    return Product.query.filter(
        (Product.description.ilike(f"%{keyword}%")) |
        (Product.city.ilike(f"%{keyword}%")) |
        (Product.category.ilike(f"%{keyword}%"))
    ).all()

@app.route("/search", methods=['POST'])
def search():
    keyword = request.form.get('keyword', '')
    products = search_products(keyword)

    categories_with_counts = db.session.query(Product.category, db.func.count(Product.id)).filter(
        (Product.description.ilike(f"%{keyword}%")) |
        (Product.city.ilike(f"%{keyword}%")) |
        (Product.category.ilike(f"%{keyword}%"))
    ).group_by(Product.category).all()

    return render_template("search.html", products=products, keyword=keyword, categories_with_counts=categories_with_counts)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("detail.html", product=product)

@app.route("/products/category/<string:category_name>")
def products_by_category(category_name):
    products = Product.query.filter_by(category=category_name).all()

    categories_with_counts = db.session.query(Product.category, db.func.count(Product.id)).group_by(Product.category).all()

    return render_template("products_by_category.html", products=products, category_name=category_name, categories_with_counts=categories_with_counts)

if __name__ == "__main__":
    app.run(debug=True)