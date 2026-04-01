"""
Modèle ORM pour les matchs.
Un match peut être :
- single : joueur contre joueur
- team   : équipe contre équipe
"""

from sqlalchemy import CheckConstraint, Column, Integer, String

from app.core.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    match_type = Column(String(20), nullable=False, index=True)

    participant_1_id = Column(Integer, nullable=False)
    participant_2_id = Column(Integer, nullable=False)

    score_1 = Column(Integer, nullable=False)
    score_2 = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("score_1 >= 0", name="check_score_1_positive"),
        CheckConstraint("score_2 >= 0", name="check_score_2_positive"),
    )
