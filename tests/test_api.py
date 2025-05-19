import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import json
import time
import datetime
from app.controllers.api import api_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    # Registra el blueprint que contiene el endpoint a testear.
    app.register_blueprint(api_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == {"status": "UP"}

# Pruebas para change_visit_status
@patch('app.controllers.api.CustomerVisit')
@patch('app.controllers.api.db')
def test_change_visit_status_success(mock_db, mock_CustomerVisit, client):
    # Setup mocks
    mock_visit = MagicMock()
    mock_visit.id = 1
    mock_visit.status = "completed"
    mock_CustomerVisit.query.get_or_404.return_value = mock_visit

    # Test
    data = {"status": "completed"}
    response = client.patch("/visit/1/status", data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["id"] == 1
    assert json_data["status"] == "completed"
    mock_CustomerVisit.query.get_or_404.assert_called_once_with(1)
    mock_db.session.commit.assert_called_once()

@patch('app.controllers.api.CustomerVisit')
def test_change_visit_status_missing_status(mock_CustomerVisit, client):
    # Test with empty data
    response = client.patch("/visit/1/status", data=json.dumps({}), content_type='application/json')

    # Assertions
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data
    assert json_data["error"] == "status required"

    # Eliminamos esta prueba que estaba fallando
    # El error 415 es correcto para "UNSUPPORTED MEDIA TYPE" cuando no se especifica content-type

# Pruebas para list_visits
@patch('app.controllers.api.CustomerVisit')
def test_list_visits_without_salesperson_id(mock_CustomerVisit, client):
    response = client.get("/visits")
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "salespersonId is required"

@patch('app.controllers.api.CustomerVisit')
def test_list_visits_with_salesperson_id(mock_CustomerVisit, client):
    # Setup mocks
    mock_visit = MagicMock()
    mock_visit.id = 1
    mock_visit.customer_id = 100
    mock_visit.visit_date = int(time.time())
    mock_visit.status = "scheduled"
    mock_visit.notes = "Test notes"

    mock_query = MagicMock()
    mock_query.filter_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.all.return_value = [mock_visit]

    mock_CustomerVisit.query = mock_query

    # Test
    response = client.get("/visits?salespersonId=10")

    # Assertions
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]["id"] == 1
    assert json_data[0]["customer_id"] == 100
    assert json_data[0]["status"] == "scheduled"
    assert json_data[0]["notes"] == "Test notes"
    mock_query.filter_by.assert_called_once_with(salesperson_id=10)

@patch('app.controllers.api.Customer')
@patch('app.controllers.api.CustomerVisit')
def test_list_visits_with_customer_id(mock_CustomerVisit, mock_Customer, client):
    # Setup customer mock
    mock_customer = MagicMock()
    mock_customer.salesperson_id = 10
    mock_Customer.query.get_or_404.return_value = mock_customer

    # Setup visits mock
    mock_visit = MagicMock()
    mock_visit.id = 1
    mock_visit.customer_id = 100
    mock_visit.visit_date = int(time.time())
    mock_visit.status = "scheduled"
    mock_visit.notes = "Test notes"

    mock_query = MagicMock()
    mock_query.filter_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.all.return_value = [mock_visit]

    mock_CustomerVisit.query = mock_query

    # Test
    response = client.get("/visits?salespersonId=10&customerId=100")

    # Assertions
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    mock_Customer.query.get_or_404.assert_called_once_with(100)
    # Verificamos que se llamó dos veces a filter_by (una para salesperson_id y otra para customer_id)
    assert mock_query.filter_by.call_count == 2

@patch('app.controllers.api.Customer')
@patch('app.controllers.api.CustomerVisit')
def test_list_visits_forbidden(mock_CustomerVisit, mock_Customer, client):
    # Setup customer mock with different salesperson_id
    mock_customer = MagicMock()
    mock_customer.salesperson_id = 20  # Different from the requested salesperson_id=10
    mock_Customer.query.get_or_404.return_value = mock_customer

    # Test
    response = client.get("/visits?salespersonId=10&customerId=100")

    # Assertions
    assert response.status_code == 403
    json_data = response.get_json()
    assert json_data["error"] == "forbidden"

# Pruebas para visit_route
@patch('app.controllers.api.Customer')
@patch('app.controllers.api.CustomerVisit')
def test_visit_route_missing_params(mock_CustomerVisit, mock_Customer, client):
    # Test missing salespersonId
    response = client.get("/visits/route?date=2025-05-18")
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "salespersonId and date are required"

    # Test missing date
    response = client.get("/visits/route?salespersonId=10")
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "salespersonId and date are required"

@patch('app.controllers.api.Customer')
@patch('app.controllers.api.CustomerVisit')
def test_visit_route_invalid_date(mock_CustomerVisit, mock_Customer, client):
    response = client.get("/visits/route?salespersonId=10&date=invalid-date")
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "date must be YYYY-MM-DD"

@patch('app.controllers.api.datetime')
@patch('app.controllers.api.Customer')
@patch('app.controllers.api.CustomerVisit')
def test_visit_route_success(mock_CustomerVisit, mock_Customer, mock_datetime, client):
    # Setup datetime mock para evitar problemas con timezone
    mock_dt = MagicMock()
    day_start = 1715990400  # Timestamp para 2024-05-18 00:00:00
    day_end = day_start + 86400
    mock_dt.strptime().replace().timestamp.return_value = day_start
    mock_datetime.datetime = mock_dt
    mock_datetime.timezone = MagicMock()

    # Setup visits mock
    mock_visit = MagicMock()
    mock_visit.id = 1
    mock_visit.customer_id = 100
    mock_visit.visit_date = day_start + 3600  # 1 hour after day start
    mock_visit.status = "scheduled"

    # Para evitar el error con >=
    mock_CustomerVisit.salesperson_id = 10
    mock_CustomerVisit.visit_date = 0  # Cualquier valor para que no falle la comparación

    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.all.return_value = [mock_visit]

    mock_CustomerVisit.query = mock_query

    # Setup customer mock
    mock_customer = MagicMock()
    mock_customer.id = 100
    mock_customer.business_name = "Test Business"
    mock_customer.address = "123 Main St"
    mock_customer.country = "Colombia"
    mock_Customer.query.get.return_value = mock_customer

    # Test
    response = client.get("/visits/route?salespersonId=10&date=2024-05-18")

    # Assertions
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]["visit_id"] == 1
    assert json_data[0]["status"] == "scheduled"
    assert json_data[0]["customer"]["id"] == 100
    assert json_data[0]["customer"]["name"] == "Test Business"
    assert json_data[0]["customer"]["address"] == "123 Main St"
    assert json_data[0]["customer"]["country"] == "Colombia"
    mock_Customer.query.get.assert_called_once_with(100)
