import time
from safrs import SAFRSBase
from app import db

# --------------------- MODEL: CUSTOMER_VIDEOS ---------------------
class CustomerVideo(SAFRSBase, db.Model):
    __tablename__ = "customer_videos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    salesperson_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    video_url = db.Column(db.String(255), nullable=False)
    recommendations = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))
    updated_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time()))

    # Relación: referencia al cliente
    customer = db.relationship("Customer", back_populates="videos", foreign_keys=[customer_id])
