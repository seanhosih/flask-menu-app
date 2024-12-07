from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(200), nullable=True)

# Initialize database
with app.app_context():
    db.create_all()
  # 初始化資料庫
@app.route('/')
def menu_list():
    menu_items = MenuItem.query.all()
    return render_template('menu_list.html', menu_items=menu_items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        new_item = MenuItem(
            item=request.form['item'],
            size=request.form['size'],
            price=float(request.form['price']),
            note=request.form.get('note', '')
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('menu_list'))
    return render_template('add_item.html')

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    if request.method == 'POST':
        item.item = request.form['item']
        item.size = request.form['size']
        item.price = float(request.form['price'])
        item.note = request.form.get('note', '')
        db.session.commit()
        return redirect(url_for('menu_list'))
    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('menu_list'))
@app.route('/api/menu', methods=['POST'])
def api_create_item():
    data = request.get_json()
    new_item = MenuItem(
        item=data['item'],
        size=data['size'],
        price=data['price'],
        note=data.get('note', '')
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created', 'item_id': new_item.id})

@app.route('/api/menu/<int:item_id>', methods=['PUT'])
def api_update_item(item_id):
    data = request.get_json()
    item = MenuItem.query.get_or_404(item_id)
    item.item = data['item']
    item.size = data['size']
    item.price = data['price']
    item.note = data.get('note', '')
    db.session.commit()
    return jsonify({'message': 'Item updated'})

@app.route('/api/menu/<int:item_id>', methods=['DELETE'])
def api_delete_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'})
# Initialize database
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
