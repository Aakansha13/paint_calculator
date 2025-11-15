"""
Unit tests for the paint calculator API functions.
"""
import pytest
import math
from paint_calculator.api import calculate_feet, calculate_gallons_required, sanitize_input


class TestCalculateFeet:
    """Test cases for calculate_feet function."""
    
    def test_calculate_feet_basic(self):
        """Test basic calculation: ((Length * 2) + (Width * 2)) * Height"""
        room_data = {'length': '10', 'width': '12', 'height': '8'}
        result = calculate_feet(room_data)
        # ((10 * 2) + (12 * 2)) * 8 = (20 + 24) * 8 = 44 * 8 = 352
        assert result == 352
    
    def test_calculate_feet_square_room(self):
        """Test square room calculation."""
        room_data = {'length': '10', 'width': '10', 'height': '10'}
        result = calculate_feet(room_data)
        # ((10 * 2) + (10 * 2)) * 10 = (20 + 20) * 10 = 40 * 10 = 400
        assert result == 400
    
    def test_calculate_feet_large_dimensions(self):
        """Test calculation with large dimensions."""
        room_data = {'length': '20', 'width': '15', 'height': '9'}
        result = calculate_feet(room_data)
        # ((20 * 2) + (15 * 2)) * 9 = (40 + 30) * 9 = 70 * 9 = 630
        assert result == 630
    
    def test_calculate_feet_small_dimensions(self):
        """Test calculation with small dimensions."""
        room_data = {'length': '5', 'width': '4', 'height': '8'}
        result = calculate_feet(room_data)
        # ((5 * 2) + (4 * 2)) * 8 = (10 + 8) * 8 = 18 * 8 = 144
        assert result == 144


class TestCalculateGallonsRequired:
    """Test cases for calculate_gallons_required function."""
    
    def test_calculate_gallons_exact_match(self):
        """Test when feet exactly matches coverage."""
        formatted_data = {'ft': 400}
        result = calculate_gallons_required(formatted_data)
        assert result == 1
    
    def test_calculate_gallons_rounds_up(self):
        """Test that gallons are rounded up."""
        formatted_data = {'ft': 401}
        result = calculate_gallons_required(formatted_data)
        assert result == 2
    
    def test_calculate_gallons_less_than_one(self):
        """Test when feet is less than coverage, should round up to 1."""
        formatted_data = {'ft': 399}
        result = calculate_gallons_required(formatted_data)
        assert result == 1
    
    def test_calculate_gallons_multiple_gallons(self):
        """Test calculation requiring multiple gallons."""
        formatted_data = {'ft': 1200}
        result = calculate_gallons_required(formatted_data)
        assert result == 3
    
    def test_calculate_gallons_exact_multiple(self):
        """Test exact multiple of coverage."""
        formatted_data = {'ft': 800}
        result = calculate_gallons_required(formatted_data)
        assert result == 2
    
    def test_calculate_gallons_zero_feet(self):
        """Test with zero feet (edge case)."""
        formatted_data = {'ft': 0}
        result = calculate_gallons_required(formatted_data)
        assert result == 0


class TestSanitizeInput:
    """Test cases for sanitize_input function."""
    
    def test_sanitize_positive_integer(self):
        """Test with positive integer."""
        assert sanitize_input('5') == 5
    
    def test_sanitize_negative_number(self):
        """Test that negative numbers are converted to absolute value."""
        assert sanitize_input('-5') == 5
    
    def test_sanitize_zero(self):
        """Test with zero."""
        assert sanitize_input('0') == 0
    
    def test_sanitize_string_number(self):
        """Test with string representation of number."""
        assert sanitize_input('42') == 42
    
    def test_sanitize_float_string(self):
        """Test that float strings are converted to int."""
        assert sanitize_input('10.5') == 10
        assert sanitize_input('10.9') == 10
