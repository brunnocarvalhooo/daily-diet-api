from flask_login import login_required, current_user
from flask import jsonify, request, Blueprint

from models.meal import Meal
from database import db

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


@meals.route('/<int:meal_id>', methods=["PUT"])
@login_required
def update_meal(meal_id):
    data = request.json

    name = data.get("name")
    description = data.get("description")
    datetime = data.get("datetime")
    in_diet = data.get("in_diet")

    if not name or not datetime or in_diet is None:
        return jsonify({"message": "Campos obrigatórios não preenchidos"}), 400

    from datetime import datetime as dt

    selected_meal = Meal.query.get(meal_id)

    if not selected_meal:
        return jsonify({'Message': 'Refeição não encontrada'}), 404

    try:
        datetime_parsed = dt.fromisoformat(datetime)
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)."}), 400

    if not isinstance(in_diet, bool):
        return jsonify({"message": "O campo 'in_diet' deve ser booleano (true ou false)."}), 400

    try:
        selected_meal.name = name
        selected_meal.description = description
        selected_meal.datetime = datetime_parsed
        selected_meal.in_diet = in_diet

        db.session.commit()

        return jsonify({'Message': 'Refeição atualizada com sucesso!'})
    except Exception as e:
        db.session.rollback()

        return jsonify({'Message': f"Erro ao atualizar a refeição: {str(e)}"}), 500


@meals.route('/<int:meal_id>', methods=["DELETE"])
@login_required
def delete_meal(meal_id):
    selected_meal = Meal.query.get(meal_id)

    if not selected_meal:
        return jsonify({'Message': 'Refeição não encontrada'}), 404

    try:
        db.session.delete(selected_meal)
        db.session.commit()

        return jsonify({'Message': 'Refeição deletada com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Message': f"Erro ao deletar a refeição: {str(e)}"}), 500


@meals.route('/', methods=["GET"])
@login_required
def get_meals():
    try:
        user_meals = Meal.query.filter_by(id_user=current_user.get_id()).all()

        meals_list = [
            {
                'id': meal.id,
                'name': meal.name,
                'description': meal.description,
                'datetime': meal.datetime.isoformat(),
                'in_diet': meal.in_diet
            }
            for meal in user_meals
        ]

        return jsonify({'meals': meals_list}), 200

    except Exception as e:
        return jsonify({'message': f"Erro ao buscar refeições: {str(e)}"}), 500


@meals.route('/<int:meal_id>', methods=["GET"])
@login_required
def get_meal(meal_id):
    selected_meal = Meal.query.get(meal_id)

    if selected_meal:
        return jsonify({
            'id': selected_meal.id,
            'name': selected_meal.name,
            'description': selected_meal.description,
            'datetime': selected_meal.datetime.isoformat(),
            'in_diet': selected_meal.in_diet,
            'id_user': selected_meal.id_user
        }), 200

    return jsonify({'Message': 'Refeição não encontrada'}), 404
