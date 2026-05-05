from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Shop, Product, Category, CartItem, Order, OrderItem, User
from decimal import Decimal

ecommerce_bp = Blueprint('ecommerce', __name__)

@ecommerce_bp.route('/ecommerce')
def ecommerce_entry():
    return render_template('ecommerce/entry.html')

@ecommerce_bp.route('/create-shop')
def create_shop_page():
    return render_template('ecommerce/create_shop.html')

@ecommerce_bp.route('/storefront')
def storefront():
    return render_template('ecommerce/storefront.html')

@ecommerce_bp.route('/shop-admin')
def shop_admin():
    return render_template('ecommerce/shop_admin.html')

@ecommerce_bp.route('/product/<id>')
def product_page(id):
    return render_template('ecommerce/product.html', product_id=id)

@ecommerce_bp.route('/cart')
def cart():
    return render_template('ecommerce/cart.html')

@ecommerce_bp.route('/orders')
def orders():
    return render_template('ecommerce/orders.html')

# API endpoints
@ecommerce_bp.route('/api/shop', methods=['GET'])
@jwt_required()
def api_get_shop():
    """
    Get user's shop
    ---
    tags:
      - E-commerce
    security:
      - Bearer: []
    responses:
      200:
        description: Shop information
      404:
        description: Shop not found
    """
    user_id = get_jwt_identity()
    shop = Shop.query.filter_by(user_id=user_id).first()
    
    if not shop:
        return jsonify({'error': 'Shop not found'}), 404
    
    return jsonify({
        'id': shop.id,
        'name': shop.name,
        'description': shop.description
    }), 200

@ecommerce_bp.route('/api/shop', methods=['POST'])
@jwt_required()
def api_create_shop():
    """
    Create a new shop
    ---
    tags:
      - E-commerce
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      201:
        description: Shop created
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if Shop.query.filter_by(user_id=user_id).first():
        return jsonify({'error': 'Shop already exists'}), 400
    
    shop = Shop(
        user_id=user_id,
        name=data.get('name', ''),
        description=data.get('description', '')
    )
    
    db.session.add(shop)
    db.session.commit()
    
    return jsonify({'id': shop.id}), 201

@ecommerce_bp.route('/api/shop', methods=['PUT'])
@jwt_required()
def api_update_shop():
    user_id = get_jwt_identity()
    shop = Shop.query.filter_by(user_id=user_id).first()
    
    if not shop:
        return jsonify({'error': 'Shop not found'}), 404
    
    data = request.get_json()
    shop.name = data.get('name', shop.name)
    shop.description = data.get('description', shop.description)
    
    db.session.commit()
    
    return jsonify({'message': 'Shop updated'}), 200

@ecommerce_bp.route('/api/products', methods=['GET'])
@jwt_required()
def api_list_products():
    """
    Get list of products
    ---
    tags:
      - E-commerce
    security:
      - Bearer: []
    parameters:
      - in: query
        name: sort
        type: string
      - in: query
        name: category
        type: string
      - in: query
        name: price_min
        type: number
      - in: query
        name: price_max
        type: number
    responses:
      200:
        description: List of products
    """
    user_id = get_jwt_identity()
    shop = Shop.query.filter_by(user_id=user_id).first()
    
    if not shop:
        return jsonify([]), 200
    
    products = Product.query.filter_by(shop_id=shop.id).all()
    
    # Apply filters
    category_filter = request.args.get('category')
    price_min = request.args.get('price_min')
    price_max = request.args.get('price_max')
    sort_by = request.args.get('sort', 'newest')
    
    filtered = products
    if category_filter:
        filtered = [p for p in filtered if p.category == category_filter]
    if price_min:
        filtered = [p for p in filtered if float(p.price) >= float(price_min)]
    if price_max:
        filtered = [p for p in filtered if float(p.price) <= float(price_max)]
    
    # Sort
    if sort_by == 'price_low':
        filtered.sort(key=lambda x: float(x.price))
    elif sort_by == 'price_high':
        filtered.sort(key=lambda x: float(x.price), reverse=True)
    elif sort_by == 'newest':
        filtered.sort(key=lambda x: x.id, reverse=True)
    elif sort_by == 'oldest':
        filtered.sort(key=lambda x: x.id)
    elif sort_by == 'name_asc':
        filtered.sort(key=lambda x: x.name)
    elif sort_by == 'name_desc':
        filtered.sort(key=lambda x: x.name, reverse=True)
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': str(p.price),
        'quantity': p.quantity,
        'image_url': p.image_url,
        'category': p.category
    } for p in filtered]), 200

@ecommerce_bp.route('/api/products/<id>', methods=['GET'])
@jwt_required()
def api_get_product(id):
    """
    Get product by ID
    ---
    tags:
      - E-commerce
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: string
        required: true
    responses:
      200:
        description: Product details
    """
    product = Product.query.get(id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'quantity': product.quantity,
        'image_url': product.image_url,
        'category': product.category
    }), 200

@ecommerce_bp.route('/api/products', methods=['POST'])
@jwt_required()
def api_create_product():
    """
    Create a new product
    ---
    tags:
      - E-commerce
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - price
          properties:
            name:
              type: string
            price:
              type: number
            category:
              type: string
    responses:
      201:
        description: Product created
    """
    user_id = get_jwt_identity()
    shop = Shop.query.filter_by(user_id=user_id).first()
    
    if not shop:
        return jsonify({'error': 'Shop not found'}), 404
    
    data = request.get_json()
    
    # Check if category exists, create if not
    category_name = data.get('category')
    if category_name:
        category = Category.query.filter_by(shop_id=shop.id, name=category_name).first()
        if not category:
            category = Category(shop_id=shop.id, name=category_name)
            db.session.add(category)
    
    product = Product(
        shop_id=shop.id,
        name=data.get('name', ''),
        description=data.get('description', ''),
        price=Decimal(data.get('price', 0)),
        quantity=data.get('quantity', 0),
        image_url=data.get('image_url', ''),
        category=category_name
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'id': product.id}), 201

@ecommerce_bp.route('/api/products/<id>', methods=['PUT'])
@jwt_required()
def api_update_product(id):
    user_id = get_jwt_identity()
    product = Product.query.get(id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if product.shop.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    # Handle category
    category_name = data.get('category')
    if category_name:
        category = Category.query.filter_by(shop_id=product.shop_id, name=category_name).first()
        if not category:
            category = Category(shop_id=product.shop_id, name=category_name)
            db.session.add(category)
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = Decimal(data.get('price', product.price))
    product.quantity = data.get('quantity', product.quantity)
    product.image_url = data.get('image_url', product.image_url)
    product.category = category_name
    
    db.session.commit()
    
    return jsonify({'message': 'Product updated'}), 200

@ecommerce_bp.route('/api/products/<id>', methods=['DELETE'])
@jwt_required()
def api_delete_product(id):
    user_id = get_jwt_identity()
    product = Product.query.get(id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if product.shop.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted'}), 200

@ecommerce_bp.route('/api/categories', methods=['GET'])
@jwt_required()
def api_list_categories():
    user_id = get_jwt_identity()
    shop = Shop.query.filter_by(user_id=user_id).first()
    
    if not shop:
        return jsonify([]), 200
    
    categories = Category.query.filter_by(shop_id=shop.id).all()
    return jsonify([c.name for c in categories]), 200

@ecommerce_bp.route('/api/cart', methods=['GET'])
@jwt_required()
def api_get_cart():
    """
    Get user's shopping cart
    ---
    tags:
      - E-commerce
    security:
      - Bearer: []
    responses:
      200:
        description: Cart items
    """
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': item.id,
        'product_id': item.product_id,
        'product_name': item.product.name,
        'product_price': str(item.product.price),
        'quantity': item.quantity,
        'image_url': item.product.image_url
    } for item in cart_items]), 200

@ecommerce_bp.route('/api/cart', methods=['POST'])
@jwt_required()
def api_add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # Check if item already in cart
    existing = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        existing.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({'message': 'Added to cart'}), 201

@ecommerce_bp.route('/api/cart/<id>', methods=['PUT'])
@jwt_required()
def api_update_cart_item(id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(id=id, user_id=user_id).first()
    
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    data = request.get_json()
    cart_item.quantity = data.get('quantity', cart_item.quantity)
    
    db.session.commit()
    
    return jsonify({'message': 'Cart item updated'}), 200

@ecommerce_bp.route('/api/cart/<id>', methods=['DELETE'])
@jwt_required()
def api_delete_cart_item(id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(id=id, user_id=user_id).first()
    
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'message': 'Cart item deleted'}), 200

@ecommerce_bp.route('/api/checkout', methods=['POST'])
@jwt_required()
def api_checkout():
    """
    Checkout cart and create order
    ---
    tags:
      - E-commerce
    security:
      - Bearer: []
    responses:
      201:
        description: Order created
    """
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    total = Decimal(0)
    order_items_data = []
    
    for item in cart_items:
        product = item.product
        if product.quantity < item.quantity:
            return jsonify({'error': f'Insufficient quantity for {product.name}'}), 400
        
        item_total = Decimal(product.price) * item.quantity
        total += item_total
        
        order_items_data.append({
            'product': product,
            'quantity': item.quantity,
            'price': product.price
        })
    
    # Create order
    order = Order(user_id=user_id, total_amount=total)
    db.session.add(order)
    db.session.flush()
    
    # Create order items and decrement product quantities
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data['product'].id,
            name=item_data['product'].name,
            price=item_data['price'],
            quantity=item_data['quantity']
        )
        db.session.add(order_item)
        item_data['product'].quantity -= item_data['quantity']
    
    # Clear cart
    CartItem.query.filter_by(user_id=user_id).delete()
    
    db.session.commit()
    
    return jsonify({'order_id': order.id, 'total': str(total)}), 201

@ecommerce_bp.route('/api/orders', methods=['GET'])
@jwt_required()
def api_list_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    return jsonify([{
        'id': order.id,
        'total_amount': str(order.total_amount),
        'created_at': order.created_at.isoformat(),
        'items': [{
            'name': item.name,
            'price': str(item.price),
            'quantity': item.quantity
        } for item in order.items]
    } for order in orders]), 200

