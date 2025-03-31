import time
from safrs import SAFRSBase
from app import db

# --------------------- MODELO: CUSTOMER_SEGMENT_ASSIGNMENTS ---------------------
class CustomerSegmentAssignment(SAFRSBase, db.Model):
    __tablename__ = "customer_segment_assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Se agregan las claves foráneas para que SQLAlchemy pueda determinar la unión.
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    segment_id = db.Column(db.Integer, db.ForeignKey("customer_segments.id"), nullable=False)
    assigned_at = db.Column(db.BigInteger, nullable=False)

    # Relaciones
    customer = db.relationship("Customer", back_populates="segment_assignments", foreign_keys=[customer_id])
    segment = db.relationship("CustomerSegment", back_populates="assignments", foreign_keys=[segment_id])
