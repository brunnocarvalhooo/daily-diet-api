from database import db
from flask import jsonify
from sqlalchemy.orm import relationship

class Meal(db.Model):
  __tablename__ = "meals"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  description = db.Column(db.String(200), nullable=True)
  datetime = db.Column(db.DateTime, nullable=False)
  in_diet = db.Column(db.Boolean, nullable=False)
  id_user = db.Column(db.Integer, db.ForeignKey("users.id"))

  user = relationship("User", back_populates="meals")

  def create(self):
    if not self.name or not self.datetime or self.in_diet is None or not self.id_user:
      return jsonify({'Message': 'Campos obrigatórios não preenchidos'}), 400

    try:
      db.session.add(self)
      db.session.commit()

      return jsonify({'Message': 'Refeição criada com sucesso!'}), 201
    except Exception as e:
      db.session.rollback()

      return jsonify({'Message': f"Erro ao criar a refeição: {str(e)}"}), 500
    
  def get_meal(self, meal_id):
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
  
  def update(self, meal_id, id_user):
    if not self.name or not self.datetime or self.in_diet is None:
      return jsonify({'Message': 'Campos obrigatórios não preenchidos'}), 400

    selected_meal = Meal.query.get(meal_id)

    if not selected_meal:
      return jsonify({'Message': 'Refeição não encontrada'}), 404
    
    try:
      selected_meal.name = self.name
      selected_meal.description = self.description
      selected_meal.datetime = self.datetime
      selected_meal.in_diet = self.in_diet

      db.session.commit()

      return jsonify({'Message': 'Refeição atualizada com sucesso!'})
    except Exception as e:
      db.session.rollback()

      return jsonify({'Message': f"Erro ao atualizar a refeição: {str(e)}"}), 500
    
  def delete(self, meal_id):
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