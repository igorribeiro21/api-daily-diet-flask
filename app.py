from flask import Flask,jsonify,request
from database import db
from models.user import User
from models.meal import Meal
from datetime import datetime
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "api-daily-diet-flask"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-daily-diet'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)
# view login
login_manager.login_view = 'login'

# PING
@app.route("/", methods=["GET"])
def ping():
    return jsonify({ "enviroment": "dev", "datetime": datetime.now() })


# LOGIN

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login",methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({ "message": "Autenticação realizada com sucesso" }), 200
    
    return jsonify({ "message": "Credenciais inválidas" }), 400

@app.route("/logout",methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({ "message": "Logout realizado com sucesso!" })

# USERS

@app.route("/user",methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role="user")
        db.session.add(user)
        db.session.commit()
        return jsonify({ "message": "Usuário cadastrado com sucesso" })

    return jsonify({ "message": "Dados inválidos!" }), 400

@app.route("/user/<int:id_user>",methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return { "username": user.username }
    
    return jsonify({ "message": "Usuário não encontrado" }), 404

@app.route("/user/<int:id_user>",methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user": 
        return jsonify({ "message": "Operação não permitida" }), 403
    
    if user and data.get("password"):
        hashed_password = bcrypt.hashpw(str.encode(data.get("password")), bcrypt.gensalt())
        user.password = hashed_password
        db.session.commit()

        return jsonify({ "message": f"Usuário {id_user} atualizado com sucesso" })
    
    return jsonify({ "message": "Usuário não encontrado" }), 404

@app.route("/user/<int:id_user>",methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != "admin":
        return jsonify({ "message": "Operação não permitida" }),403

    if id_user == current_user.id:
        return jsonify({ "message": "Deleção não permitida" }), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({ "message": f"Usuário {id_user} deletado com sucesso" })
    
    return jsonify({ "message": "Usuário não encontrado" }), 404


    # MEALS
@app.route("/meals",methods=["POST"])
@login_required
def create_meal():
    data = request.json    
    user_id = current_user.id
    
    name = data.get("name")
    description = data.get("description")
    inside_diet = data.get("inside_diet")

    if name and description and not inside_diet is None:
        meal = Meal(name=name,description=description,inside_diet=inside_diet,user_id=user_id)
        db.session.add(meal)
        db.session.commit()

        return jsonify({"message": "Refeição criada com sucesso"})
    
    return jsonify({ "message": "Parâmetros inválidos" }), 400

@app.route("/meals/<int:id>",methods=["PUT"])
@login_required
def update_meal(id):
    data = request.json
    user_id = current_user.id

    name = data.get("name")
    description = data.get("description")
    inside_diet = data.get("inside_diet")

    meal = Meal.query.get(id)

    if not meal:
        return jsonify({ "message": "Refeição não encontrada" }), 400
    
    if meal.user_id != user_id:
        return jsonify({ "message": "Operação não permitida" }), 403

    if name or description or not inside_diet is None:
        if name:
            meal.name = name
        
        if description:
            meal.description = description

        if not inside_diet is None:
            meal.inside_diet = inside_diet

        db.session.commit()

        return jsonify({"message": "Refeição atualizada com sucesso"})
    else:
        return jsonify({ "message": "Parâmetros inválidos" }), 400
    
@app.route("/meals/<int:id>",methods=["DELETE"])
def delete_meal(id):
    user_id = current_user.id

    meal = Meal.query.get(id)

    if not meal:
        return jsonify({ "message": "Refeição não encontrada" }), 400
    
    if meal.user_id != user_id:
        return jsonify({ "message": "Operação não permitida" }), 403
    
    db.session.delete(meal)
    db.session.commit()
    return jsonify({ "message": f"Refeição {id} deletada com sucesso" })

if __name__ == "__main__":
    app.run(debug=True)