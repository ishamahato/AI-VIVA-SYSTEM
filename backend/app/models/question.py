from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func

from ..database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(120), nullable=False, index=True)
    text = Column(Text, nullable=False)
    difficulty = Column(String(20), default="medium")  # easy | medium | hard
    # Model answer / key points the AI uses as a reference when grading
    expected_answer = Column(Text, nullable=True)
    # Comma-separated keywords (optional, helps grading)
    keywords = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("faculty.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
