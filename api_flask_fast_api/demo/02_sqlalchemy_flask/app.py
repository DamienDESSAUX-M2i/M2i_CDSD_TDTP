from flask import Flask, jsonify, request
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, User

app = Flask(__name__)
# SQLITE
DATABASE_URL = "sqlite:///demo.db"

#MySQL
# pip install sqlalchemy pymysql
# DATABASE_URL = "mysql+pymysql://root:test@localhost:3306/demo_sqlalche?charset=utf8mb4" # Mysql

# Postgres
# pip install sqlalchemy "psycopg[binary]"
# DATABASE_URL = "postgresql+psycopg://mon_user:mon_mot_de_passe@localhost:5432/ma_base"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)



@app.get("/")
def home():
    return jsonify({"message": "Demo Flask + SQLAlchemy"})


@app.post("/users")
def create_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "name et email sont obligatoires"}), 400

    with SessionLocal() as session:
        existing_user = session.scalar(
            select(User).where(User.email == data["email"])
        )

        if existing_user:
            return jsonify({"error": "email déjà utilisé"}), 409

        user = User(name=data["name"], email=data["email"])
        session.add(user)
        session.commit()
        session.refresh(user)

        return jsonify(user.to_dict()), 201


@app.get("/users")
def list_users():
    with SessionLocal() as session:
        users = session.scalars(select(User).order_by(User.id)).all()
        return jsonify([user.to_dict() for user in users])


@app.get("/users/<int:user_id>")
def get_user(user_id: int):
    with SessionLocal() as session:
        user = session.get(User, user_id)

        if not user:
            return jsonify({"error": "utilisateur introuvable"}), 404

        return jsonify(user.to_dict())


@app.put("/users/<int:user_id>")
def update_user(user_id: int):
    data = request.get_json()

    with SessionLocal() as session:
        user = session.get(User, user_id)

        if not user:
            return jsonify({"error": "utilisateur introuvable"}), 404

        if "name" in data:
            user.name = data["name"]

        if "email" in data:
            existing_user = session.scalar(
                select(User).where(User.email == data["email"], User.id != user_id)
            )
            if existing_user:
                return jsonify({"error": "email déjà utilisé"}), 409
            user.email = data["email"]

        session.commit()
        session.refresh(user)

        return jsonify(user.to_dict())


@app.delete("/users/<int:user_id>")
def delete_user(user_id: int):
    with SessionLocal() as session:
        user = session.get(User, user_id)

        if not user:
            return jsonify({"error": "utilisateur introuvable"}), 404

        session.delete(user)
        session.commit()

        return jsonify({"message": "utilisateur supprimé"})


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")