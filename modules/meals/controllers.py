from flask_login import login_required, current_user
from flask import jsonify, request, Blueprint
from database import db

from models.meal import Meal

meals = Blueprint('meals', __name__)

@meals.route('/', methods=["POST"])
@login_required
def create_meal():
  data = request.json

  name = data.get("name")
  description = data.get("description")
  datetime = data.get("datetime")
  in_diet = data.get("in_diet")

  if name and datetime and in_diet is not None:
    from datetime import datetime as dt
    
    try:
        datetime_parsed = dt.fromisoformat(datetime)
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use ISO 8601."}), 400

    if not isinstance(in_diet, bool):
        return jsonify({"message": "O campo 'in_diet' deve ser booleano."}), 400

    try:
        meal = Meal(
            name=name,
            description=description,
            datetime=datetime_parsed,
            in_diet=in_diet,
            id_user=current_user.get_id()
        )
        
        db.session.add(meal)
        db.session.commit()

        return jsonify({"message": "Refeição cadastrada com sucesso", "meal_id": meal.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao cadastrar refeição: {str(e)}"}), 500

  return jsonify({"message": "Campos obrigatórios não preenchidos"}), 400
