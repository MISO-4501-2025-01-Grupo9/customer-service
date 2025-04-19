import time
from safrs import SAFRSBase
from app import db

# --------------------- MODELO: CUSTOMERS ---------------------
class Customer(SAFRSBase, db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    salesperson_id = db.Column(db.Integer, nullable=False, default=0)
    business_name = db.Column(db.String(255), nullable=False)
    business_type = db.Column(db.String(100))
    tax_id = db.Column(db.String(100))
    credit_limit = db.Column(db.Numeric(10, 2))
    payment_terms = db.Column(db.Text)
    address = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(100), nullable=False, default="Colombia")
    created_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))
    updated_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))

    # Relaciones
    segment_assignments = db.relationship("CustomerSegmentAssignment", back_populates="customer",
                                          cascade="all, delete-orphan")
    visits = db.relationship("CustomerVisit", back_populates="customer", cascade="all, delete-orphan")
