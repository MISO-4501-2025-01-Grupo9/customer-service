import time
from safrs import SAFRSBase
from app import db

# --------------------- MODELO: CUSTOMER_SEGMENTS ---------------------
class CustomerSegment(SAFRSBase, db.Model):
    __tablename__ = "customer_segments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))
    updated_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))

    assignments = db.relationship("CustomerSegmentAssignment", back_populates="segment", cascade="all, delete-orphan")
