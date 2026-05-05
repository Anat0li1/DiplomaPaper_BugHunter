from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    active_role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    test_cases = db.relationship('TestCase', backref='user', lazy=True)
    bug_reports = db.relationship('BugReport', backref='user', lazy=True)
    shop = db.relationship('Shop', backref='user', uselist=False, lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    boards = db.relationship('Board', backref='user', lazy=True)

class TestCase(db.Model):
    __tablename__ = 'test_cases'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    given_id = db.Column(db.String(50), nullable=True)  # Changed to String, nullable
    application_group = db.Column(db.String(100))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.Integer, default=2)  # 1=High, 2=Medium, 3=Low
    is_system = db.Column(db.Boolean, default=False)
    preconditions = db.Column(db.Text)
    postconditions = db.Column(db.Text)
    version = db.Column(db.String(50))
    environment = db.Column(db.String(100))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    steps = db.relationship('TestStep', backref='test_case', lazy=True, cascade='all, delete-orphan')

class TestStep(db.Model):
    __tablename__ = 'test_steps'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    test_case_id = db.Column(db.String(36), db.ForeignKey('test_cases.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    step_name = db.Column(db.String(200), nullable=False)
    test_data = db.Column(db.Text)
    expected_result = db.Column(db.Text)

class BugReport(db.Model):
    __tablename__ = 'bug_reports'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    given_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    preconditions = db.Column(db.Text)
    postconditions = db.Column(db.Text)
    actual_result = db.Column(db.Text)
    expected_result = db.Column(db.Text)
    severity = db.Column(db.String(20), default='Medium')  # Critical, High, Medium, Low
    priority = db.Column(db.String(20), default='Medium')  # High, Medium, Low
    status = db.Column(db.String(20), default='New')  # New, In Progress, Closed, Won't Fix
    system_and_browser_inf = db.Column(db.String(200))
    version = db.Column(db.String(50))
    environment = db.Column(db.String(100))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    test_case_id = db.Column(db.String(36), db.ForeignKey('test_cases.id'), nullable=True)
    is_system = db.Column(db.Boolean, default=False)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    steps = db.relationship('BugStep', backref='bug_report', lazy=True, cascade='all, delete-orphan')

class BugStep(db.Model):
    __tablename__ = 'bug_steps'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    bug_report_id = db.Column(db.String(36), db.ForeignKey('bug_reports.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    step_name = db.Column(db.String(200), nullable=False)

class Shop(db.Model):
    __tablename__ = 'shops'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    products = db.relationship('Product', backref='shop', lazy=True, cascade='all, delete-orphan')
    categories = db.relationship('Category', backref='shop', lazy=True, cascade='all, delete-orphan')

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shop_id = db.Column(db.String(36), db.ForeignKey('shops.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('shop_id', 'name', name='unique_category_per_shop'),)

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shop_id = db.Column(db.String(36), db.ForeignKey('shops.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Board(db.Model):
    __tablename__ = 'boards'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    columns = db.relationship('Column', backref='board', lazy=True, cascade='all, delete-orphan', order_by='Column.ordering')

class Column(db.Model):
    __tablename__ = 'columns'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    board_id = db.Column(db.String(36), db.ForeignKey('boards.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    ordering = db.Column(db.Integer, nullable=False)
    
    tasks = db.relationship('Task', backref='column', lazy=True, cascade='all, delete-orphan', order_by='Task.id')

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    column_id = db.Column(db.String(36), db.ForeignKey('columns.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    doer = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    priority = db.Column(db.String(20))

