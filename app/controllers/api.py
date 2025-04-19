from flask import Blueprint, jsonify, request
from app.models.customer_visits import CustomerVisit
from app.models.customer import Customer   # para la dirección
import time, datetime

from app import db

api_bp = Blueprint("api", __name__)

@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "UP"}), 200

# 1️⃣  Cambio de estado de una visita
@api_bp.route("/visit/<int:visit_id>/status", methods=["PATCH"])
def change_visit_status(visit_id):
    data = request.json or {}
    new_status = data.get("status")
    if not new_status:
        return jsonify({"error": "status required"}), 400

    visit = CustomerVisit.query.get_or_404(visit_id)
    visit.status = new_status
    visit.updated_at = int(time.time())
    db.session.commit()
    return jsonify({"id": visit.id, "status": visit.status}), 200


# 2️⃣  Listar visitas de un vendedor
@api_bp.route("/visits", methods=["GET"])
def list_visits():
    salesperson_id = request.args.get("salespersonId", type=int)
    customer_id    = request.args.get("customerId", type=int)

    if not salesperson_id:
        return jsonify({"error": "salespersonId is required"}), 400

    query = CustomerVisit.query.filter_by(salesperson_id=salesperson_id)

    if customer_id:
        cust = Customer.query.get_or_404(customer_id)
        if cust.salesperson_id != salesperson_id:
            return jsonify({"error": "forbidden"}), 403
        query = query.filter_by(customer_id=customer_id)

    visits = query.order_by(CustomerVisit.visit_date.desc()).all()

    return jsonify([{
        "id": v.id,
        "customer_id": v.customer_id,
        "visit_date": v.visit_date,
        "status": v.status,
        "notes": v.notes
    } for v in visits]), 200


# 3️⃣  Ruta de visitas por fecha (con direcciones reales)
@api_bp.route("/visits/route", methods=["GET"])
def visit_route():
    salesperson_id = request.args.get("salespersonId", type=int)
    date_str       = request.args.get("date")      # formato YYYY-MM-DD

    if not salesperson_id or not date_str:
        return jsonify({"error": "salespersonId and date are required"}), 400

    try:
        day_start = int(datetime.datetime.strptime(date_str, "%Y-%m-%d")
                        .replace(tzinfo=datetime.timezone.utc)
                        .timestamp())
        day_end   = day_start + 86400
    except ValueError:
        return jsonify({"error": "date must be YYYY-MM-DD"}), 400

    visits = (CustomerVisit.query
              .filter(CustomerVisit.salesperson_id==salesperson_id,
                      CustomerVisit.visit_date>=day_start,
                      CustomerVisit.visit_date<day_end)
              .order_by(CustomerVisit.visit_date)
              .all())

    # Unir con la dirección del cliente
    results = []
    for v in visits:
        customer = Customer.query.get(v.customer_id)
        results.append({
            "visit_id"   : v.id,
            "visit_time" : v.visit_date,
            "status"     : v.status,
            "customer"   : {
                "id"      : customer.id,
                "name"    : customer.business_name,
                "address" : customer.address,
                "country" : customer.country
            }
        })
    return jsonify(results), 200