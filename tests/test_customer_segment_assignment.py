import time
import unittest
from unittest.mock import patch, MagicMock
from app.models.customer_segment_assigments import CustomerSegmentAssignment

class TestCustomerSegmentAssignment(unittest.TestCase):
    def test_customer_segment_assignment_defaults_and_query(self):
        # Creamos una instancia del modelo sin persistir en base de datos.
        assigned_at_val = int(time.time())
        assignment = CustomerSegmentAssignment(
            customer_id=1,
            segment_id=2,
            assigned_at=assigned_at_val
        )

        # Verificamos que el valor asignado en assigned_at sea el esperado.
        self.assertEqual(assignment.assigned_at, assigned_at_val)

        # Mockeamos el atributo query para simular la interacción con la base de datos.
        with patch.object(CustomerSegmentAssignment, 'query', new=MagicMock()) as mock_query:
            # Configuramos el mock para que, al llamar a filter_by(...).first(), devuelva nuestro objeto.
            mock_query.filter_by.return_value.first.return_value = assignment

            retrieved = CustomerSegmentAssignment.query.filter_by(customer_id=1).first()
            self.assertEqual(retrieved, assignment)

if __name__ == '__main__':
    unittest.main()
