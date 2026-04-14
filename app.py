"""
Application Flask pour le Marketing et la Publicité des Produits
"""
import os
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, redirect, url_for, request,
    flash, session, jsonify, send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# ── Configuration ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "marketing-app-secret-2024")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "products.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

db = SQLAlchemy(app)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Models ─────────────────────────────────────────────────────────────────────
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, default="")
    icon = db.Column(db.String(50), default="tag")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship("Product", backref="category", lazy=True)

    def product_count(self):
        return len(self.products)


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, nullable=False, default=0.0)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    image_filename = db.Column(db.String(255), default="")
    featured = db.Column(db.Boolean, default=False)
    in_stock = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def image_url(self):
        if self.image_filename:
            return url_for("static", filename=f"uploads/{self.image_filename}")
        return url_for("static", filename="img/placeholder.svg")


# ── Helpers ────────────────────────────────────────────────────────────────────
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = generate_password_hash(
    os.environ.get("ADMIN_PASSWORD", "admin123")
)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Veuillez vous connecter pour accéder à l'interface admin.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


def save_image(file):
    """Save uploaded image and return the filename."""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid collisions
        base, ext = os.path.splitext(filename)
        filename = f"{base}_{int(datetime.utcnow().timestamp())}{ext}"
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return filename
    return None


# ── Public Routes ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    categories = Category.query.all()
    featured = Product.query.filter_by(featured=True, in_stock=True).limit(8).all()
    latest = Product.query.filter_by(in_stock=True).order_by(Product.created_at.desc()).limit(8).all()
    total_products = Product.query.filter_by(in_stock=True).count()
    return render_template(
        "index.html",
        categories=categories,
        featured=featured,
        latest=latest,
        total_products=total_products,
    )


@app.route("/category/<int:cat_id>")
def category(cat_id):
    cat = db.get_or_404(Category, cat_id)
    products = Product.query.filter_by(category_id=cat_id, in_stock=True).all()
    categories = Category.query.all()
    return render_template("category.html", category=cat, products=products, categories=categories)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = db.get_or_404(Product, product_id)
    related = (
        Product.query
        .filter(Product.category_id == product.category_id, Product.id != product_id, Product.in_stock == True)
        .limit(4).all()
    )
    return render_template("product.html", product=product, related=related)


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    cat_id = request.args.get("cat", "")
    min_price = request.args.get("min_price", "")
    max_price = request.args.get("max_price", "")

    query = Product.query.filter_by(in_stock=True)
    if q:
        query = query.filter(
            db.or_(
                Product.name.ilike(f"%{q}%"),
                Product.description.ilike(f"%{q}%"),
            )
        )
    if cat_id:
        query = query.filter_by(category_id=int(cat_id))
    if min_price:
        query = query.filter(Product.price >= float(min_price))
    if max_price:
        query = query.filter(Product.price <= float(max_price))

    products = query.all()
    categories = Category.query.all()
    return render_template(
        "search.html",
        products=products,
        categories=categories,
        query=q,
        selected_cat=cat_id,
        min_price=min_price,
        max_price=max_price,
    )


# ── Admin Auth ─────────────────────────────────────────────────────────────────
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["admin_logged_in"] = True
            session.permanent = True
            flash("Connexion réussie! Bienvenue dans l'interface admin.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("index"))


# ── Admin Dashboard ────────────────────────────────────────────────────────────
@app.route("/admin")
@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    stats = {
        "total_products": Product.query.count(),
        "total_categories": Category.query.count(),
        "featured_products": Product.query.filter_by(featured=True).count(),
        "out_of_stock": Product.query.filter_by(in_stock=False).count(),
    }
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    categories = Category.query.all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_products=recent_products,
        categories=categories,
    )


# ── Admin Products ─────────────────────────────────────────────────────────────
@app.route("/admin/products")
@login_required
def admin_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("admin/products.html", products=products)


@app.route("/admin/products/add", methods=["GET", "POST"])
@login_required
def admin_product_add():
    categories = Category.query.all()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", 0)
        category_id = request.form.get("category_id") or None
        featured = bool(request.form.get("featured"))
        in_stock = bool(request.form.get("in_stock", True))

        if not name:
            flash("Le nom du produit est obligatoire.", "danger")
            return render_template("admin/product_form.html", categories=categories, product=None)

        image_filename = ""
        file = request.files.get("image")
        if file and file.filename:
            saved = save_image(file)
            if saved:
                image_filename = saved
            else:
                flash("Format d'image non supporté.", "warning")

        product = Product(
            name=name,
            description=description,
            price=float(price),
            category_id=int(category_id) if category_id else None,
            image_filename=image_filename,
            featured=featured,
            in_stock=in_stock,
        )
        db.session.add(product)
        db.session.commit()
        flash(f"Produit «{name}» ajouté avec succès!", "success")
        return redirect(url_for("admin_products"))

    return render_template("admin/product_form.html", categories=categories, product=None)


@app.route("/admin/products/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def admin_product_edit(product_id):
    product = db.get_or_404(Product, product_id)
    categories = Category.query.all()
    if request.method == "POST":
        product.name = request.form.get("name", "").strip()
        product.description = request.form.get("description", "").strip()
        product.price = float(request.form.get("price", 0))
        cat_id = request.form.get("category_id")
        product.category_id = int(cat_id) if cat_id else None
        product.featured = bool(request.form.get("featured"))
        product.in_stock = bool(request.form.get("in_stock"))
        product.updated_at = datetime.utcnow()

        file = request.files.get("image")
        if file and file.filename:
            saved = save_image(file)
            if saved:
                # Remove old image
                if product.image_filename:
                    old_path = os.path.join(app.config["UPLOAD_FOLDER"], product.image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                product.image_filename = saved

        db.session.commit()
        flash(f"Produit «{product.name}» modifié avec succès!", "success")
        return redirect(url_for("admin_products"))

    return render_template("admin/product_form.html", categories=categories, product=product)


@app.route("/admin/products/delete/<int:product_id>", methods=["POST"])
@login_required
def admin_product_delete(product_id):
    product = db.get_or_404(Product, product_id)
    if product.image_filename:
        img_path = os.path.join(app.config["UPLOAD_FOLDER"], product.image_filename)
        if os.path.exists(img_path):
            os.remove(img_path)
    name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f"Produit «{name}» supprimé.", "info")
    return redirect(url_for("admin_products"))


@app.route("/admin/products/toggle-featured/<int:product_id>", methods=["POST"])
@login_required
def admin_toggle_featured(product_id):
    product = db.get_or_404(Product, product_id)
    product.featured = not product.featured
    db.session.commit()
    return jsonify({"featured": product.featured})


# ── Admin Categories ───────────────────────────────────────────────────────────
@app.route("/admin/categories")
@login_required
def admin_categories():
    categories = Category.query.all()
    return render_template("admin/categories.html", categories=categories)


@app.route("/admin/categories/add", methods=["POST"])
@login_required
def admin_category_add():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    icon = request.form.get("icon", "tag").strip()
    if not name:
        flash("Le nom de la catégorie est obligatoire.", "danger")
    elif Category.query.filter_by(name=name).first():
        flash(f"La catégorie «{name}» existe déjà.", "warning")
    else:
        cat = Category(name=name, description=description, icon=icon)
        db.session.add(cat)
        db.session.commit()
        flash(f"Catégorie «{name}» ajoutée avec succès!", "success")
    return redirect(url_for("admin_categories"))


@app.route("/admin/categories/edit/<int:cat_id>", methods=["POST"])
@login_required
def admin_category_edit(cat_id):
    cat = db.get_or_404(Category, cat_id)
    cat.name = request.form.get("name", cat.name).strip()
    cat.description = request.form.get("description", cat.description).strip()
    cat.icon = request.form.get("icon", cat.icon).strip()
    db.session.commit()
    flash(f"Catégorie «{cat.name}» modifiée.", "success")
    return redirect(url_for("admin_categories"))


@app.route("/admin/categories/delete/<int:cat_id>", methods=["POST"])
@login_required
def admin_category_delete(cat_id):
    cat = db.get_or_404(Category, cat_id)
    # Unlink products
    for p in cat.products:
        p.category_id = None
    name = cat.name
    db.session.delete(cat)
    db.session.commit()
    flash(f"Catégorie «{name}» supprimée.", "info")
    return redirect(url_for("admin_categories"))


# ── DB Init & Seed ─────────────────────────────────────────────────────────────
def seed_data():
    """Add some demo data if the DB is empty."""
    if Category.query.count() == 0:
        cats = [
            Category(name="Électronique", description="Appareils et gadgets électroniques", icon="laptop"),
            Category(name="Mode", description="Vêtements et accessoires", icon="tshirt"),
            Category(name="Maison & Déco", description="Décoration et mobilier", icon="home"),
            Category(name="Sport", description="Articles de sport et fitness", icon="futbol"),
        ]
        db.session.add_all(cats)
        db.session.commit()

    if Product.query.count() == 0:
        cats = Category.query.all()
        products = [
            Product(name="Smartphone Premium X1", description="Le dernier smartphone avec écran AMOLED 6.7\", appareil photo 200MP et batterie 5000mAh. Expérience utilisateur exceptionnelle.", price=899.99, category_id=cats[0].id, featured=True),
            Product(name="Laptop UltraBook Pro", description="Ordinateur portable ultra-fin avec processeur Intel Core i9, 32GB RAM et SSD 1TB. Parfait pour les professionnels.", price=1499.00, category_id=cats[0].id, featured=True),
            Product(name="Casque Audio Sans Fil", description="Casque Bluetooth avec réduction de bruit active, 40h d'autonomie et son haute fidélité.", price=249.99, category_id=cats[0].id, featured=False),
            Product(name="Veste Élégante Premium", description="Veste en laine mérinos de haute qualité, coupe moderne, disponible en plusieurs couleurs.", price=189.00, category_id=cats[1].id, featured=True),
            Product(name="Chaussures Sport Pro", description="Chaussures de running avec semelle amortissante, légères et respirantes. Idéal pour la course longue distance.", price=129.99, category_id=cats[1].id, featured=False),
            Product(name="Sac à Main Luxe", description="Sac en cuir véritable, design minimaliste et élégant, plusieurs compartiments pratiques.", price=299.00, category_id=cats[1].id, featured=False),
            Product(name="Lampe Design Moderne", description="Lampe LED design avec variateur d'intensité, lumière chaude et froide réglable.", price=89.99, category_id=cats[2].id, featured=True),
            Product(name="Canapé Scandinave", description="Canapé 3 places en tissu premium, design scandinave, très confortable et durable.", price=799.00, category_id=cats[2].id, featured=False),
            Product(name="Vélo de Route Carbon", description="Vélo de route en cadre carbone, 22 vitesses Shimano, roues aérodynamiques. Pour les cyclistes passionnés.", price=2199.00, category_id=cats[3].id, featured=True),
            Product(name="Tapis de Yoga Premium", description="Tapis de yoga antidérapant, épaisseur 6mm, matière écologique et durable.", price=59.99, category_id=cats[3].id, featured=False),
        ]
        db.session.add_all(products)
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_data()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
