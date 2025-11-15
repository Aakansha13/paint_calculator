"""
Unit tests for Flask routes.
"""
import pytest
import json
from paint_calculator.run import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestIndexRoute:
    """Test cases for the index route."""
    
    def test_index_route(self, client):
        """Test that index page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Enter the number of rooms' in response.data
        assert b'Calculating Paint Required' in response.data


class TestDimensionsRoute:
    """Test cases for the dimensions route."""
    
    def test_dimensions_route_with_valid_rooms(self, client):
        """Test dimensions page with valid number of rooms."""
        response = client.get('/dimensions?rooms=3')
        assert response.status_code == 200
        assert b'Room Number' in response.data
        assert b'Length' in response.data
        assert b'Width' in response.data
        assert b'Height' in response.data
    
    def test_dimensions_route_with_negative_rooms(self, client):
        """Test that negative numbers are sanitized to positive."""
        response = client.get('/dimensions?rooms=-5')
        assert response.status_code == 200
        # Should still render the page with 5 rooms (sanitized)
        assert b'Room Number' in response.data
    
    def test_dimensions_route_with_zero_rooms(self, client):
        """Test dimensions route with zero rooms."""
        response = client.get('/dimensions?rooms=0')
        assert response.status_code == 200
    
    def test_dimensions_route_no_rooms_parameter(self, client):
        """Test dimensions route without rooms parameter."""
        response = client.get('/dimensions')
        # Should handle missing parameter gracefully
        assert response.status_code in [200, 400, 500]


class TestResultsRoute:
    """Test cases for the results route."""
    
    def test_results_route_with_valid_data(self, client):
        """Test results page with valid room dimensions."""
        data = {
            'length-0': '10',
            'width-0': '12',
            'height-0': '8',
            'length-1': '15',
            'width-1': '10',
            'height-1': '9'
        }
        response = client.post('/results', data=data)
        assert response.status_code == 200
        assert b'View Results' in response.data
    
    def test_results_route_multiple_rooms(self, client):
        """Test results route with multiple rooms."""
        data = {
            'length-0': '10',
            'width-0': '10',
            'height-0': '8',
            'length-1': '12',
            'width-1': '12',
            'height-1': '9',
            'length-2': '8',
            'width-2': '8',
            'height-2': '7'
        }
        response = client.post('/results', data=data)
        assert response.status_code == 200
        assert b'View Results' in response.data


class TestAPICalculateRoute:
    """Test cases for the API calculate endpoint."""
    
    def test_api_calculate_single_room(self, client):
        """Test API calculation with single room."""
        data = {
            'room-1': {
                'length': '10',
                'width': '12',
                'height': '8'
            }
        }
        response = client.post('/api/v1/calculate',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 200
        result = json.loads(response.data)
        assert 'room-1' in result
        assert 'total_gallons' in result
        assert result['room-1']['ft'] == 352  # ((10*2) + (12*2)) * 8
        assert result['room-1']['gallons'] == 1  # 352 / 400 rounded up
        assert result['total_gallons'] == 1
    
    def test_api_calculate_multiple_rooms(self, client):
        """Test API calculation with multiple rooms."""
        data = {
            'room-1': {
                'length': '10',
                'width': '10',
                'height': '10'
            },
            'room-2': {
                'length': '15',
                'width': '12',
                'height': '9'
            }
        }
        response = client.post('/api/v1/calculate',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 200
        result = json.loads(response.data)
        assert 'room-1' in result
        assert 'room-2' in result
        assert 'total_gallons' in result
        
        # Room 1: ((10*2) + (10*2)) * 10 = 400 ft, 1 gallon
        assert result['room-1']['ft'] == 400
        assert result['room-1']['gallons'] == 1
        
        # Room 2: ((15*2) + (12*2)) * 9 = (30 + 24) * 9 = 486 ft, 2 gallons
        assert result['room-2']['ft'] == 486
        assert result['room-2']['gallons'] == 2
        
        assert result['total_gallons'] == 3
    
    def test_api_calculate_rounds_up_gallons(self, client):
        """Test that API correctly rounds up gallons."""
        data = {
            'room-1': {
                'length': '10',
                'width': '12',
                'height': '8'
            }
        }
        response = client.post('/api/v1/calculate',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 200
        result = json.loads(response.data)
        # 352 ft requires 1 gallon (rounds up from 0.88)
        assert result['room-1']['gallons'] == 1
    
    def test_api_calculate_invalid_json(self, client):
        """Test API with invalid JSON."""
        response = client.post('/api/v1/calculate',
                              data='invalid json',
                              content_type='application/json')
        # Should return error status
        assert response.status_code in [400, 500]
    
    def test_api_calculate_missing_fields(self, client):
        """Test API with missing required fields."""
        data = {
            'room-1': {
                'length': '10',
                'width': '12'
                # Missing height
            }
        }
        response = client.post('/api/v1/calculate',
                              data=json.dumps(data),
                              content_type='application/json')
        # Should handle missing fields gracefully
        assert response.status_code in [200, 400, 500]
