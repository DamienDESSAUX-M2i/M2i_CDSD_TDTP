import pickle
from pathlib import Path
from typing import Generator

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import Base, SessionLocal, engine
from models import Prediction
from schemas import PredictionHistoryItem, PredictionRequest, PredictionResponse

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "intent_model.pkl"

with MODEL_PATH.open("rb") as file:
    model = pickle.load(file)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI ML + SQLite Demo",
    description="API de démonstration avec modèle PKL et sauvegarde SQLite",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"message": "API ML + SQLite opérationnelle"}


@app.post("/predict-intent", response_model=PredictionResponse)
def predict_intent(payload: PredictionRequest, db: Session = Depends(get_db)) -> PredictionResponse:
    probabilities = model.predict_proba([payload.text])[0]
    labels = model.classes_

    scores = {
        label: round(float(score), 4)
        for label, score in zip(labels, probabilities)
    }

    predicted_label = str(model.predict([payload.text])[0])
    confidence = round(float(max(probabilities)), 4)

    prediction = Prediction(
        first_name=payload.first_name.strip(),
        message=payload.text.strip(),
        predicted_label=predicted_label,
        confidence=confidence,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return PredictionResponse(
        id=prediction.id,
        first_name=prediction.first_name,
        text=prediction.message,
        predicted_label=prediction.predicted_label,
        confidence=prediction.confidence,
        all_scores=scores,
        created_at=prediction.created_at,
    )


@app.get("/predictions", response_model=list[PredictionHistoryItem])
def list_predictions(db: Session = Depends(get_db)) -> list[PredictionHistoryItem]:
    return db.query(Prediction).order_by(Prediction.created_at.desc()).all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
