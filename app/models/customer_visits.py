import time
from safrs import SAFRSBase
from app import db

# --------------------- MODELO: CUSTOMER_VISITS ---------------------
class CustomerVisit(SAFRSBase, db.Model):
    __tablename__ = "customer_visits"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    salesperson_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    visit_date = db.Column(db.BigInteger, nullable=False)  # Se recomienda enviar Unix timestamp
    notes = db.Column(db.Text)
    outcomes = db.Column(db.Text)
    created_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))
    updated_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))

    # Relación: referencia al cliente
    customer = db.relationship("Customer", back_populates="visits", foreign_keys=[customer_id])
