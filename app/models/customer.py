import time
from safrs import SAFRSBase
from app import db

# --------------------- MODELO: CUSTOMERS ---------------------
class Customer(SAFRSBase, db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    business_name = db.Column(db.String(255), nullable=False)
    business_type = db.Column(db.String(100))
    tax_id = db.Column(db.String(100))
    credit_limit = db.Column(db.Numeric(10, 2))
    payment_terms = db.Column(db.Text)
    created_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))
    updated_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))

    # Relaciones
    segment_assignments = db.relationship("CustomerSegmentAssignment", back_populates="customer",
                                          cascade="all, delete-orphan")
    visits = db.relationship("CustomerVisit", back_populates="customer", cascade="all, delete-orphan")
    videos = db.relationship("CustomerVideo", back_populates="customer", cascade="all, delete-orphan")
