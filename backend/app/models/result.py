from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from ..database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="SET NULL"), nullable=True)

    transcript = Column(Text, nullable=True)        # what the student said
    score = Column(Float, nullable=True)            # 0 - 10
    feedback = Column(Text, nullable=True)          # overall feedback
    strengths = Column(Text, nullable=True)
    improvements = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    question = relationship("Question", lazy="joined")
