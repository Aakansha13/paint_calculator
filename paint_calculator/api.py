import math
import re

from flask import Blueprint, request, jsonify

api = Blueprint('api', 'api', url_prefix='/api')


@api.route('/v1/calculate', methods=['POST'])
def calculate():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400
    formatted_data = {}
    total_gallons_required = 0

    for room_number, room_data in data.items():
        # Validate required fields
        try:
            _ = room_data['length']
            _ = room_data['width']
            _ = room_data['height']
        except (TypeError, KeyError):
            return jsonify({"error": f"Missing required fields for {room_number}"}), 400

        formatted_data[room_number] = {}
        try:
            formatted_data[room_number]['ft'] = calculate_feet(room_data)
            formatted_data[room_number]['gallons'] = calculate_gallons_required(formatted_data[room_number])
            formatted_data[room_number]['room'] = re.search(r'(\d+)$', room_number).group(0)
        except (ValueError, TypeError):
            return jsonify({"error": f"Invalid numeric values for {room_number}"}), 400
        total_gallons_required += formatted_data[room_number]['gallons']
    formatted_data['total_gallons'] = total_gallons_required
    return jsonify(formatted_data)


def calculate_feet(formatted_data):
    """
    Calculate the number of feet required to paint the surface area of a single room
    :param formatted_data: dict of L/W/H information
    :return: integer for the number of feet required by performing `((Length * 2) + (Width * 2)) * Height`
    """
    length = int(formatted_data['length'])
    width = int(formatted_data['width'])
    height = int(formatted_data['height'])
    return ((length * 2) + (width * 2)) * height


def calculate_gallons_required(formatted_data):
    """
    Number of feet to paint divided by the amount of feet the paint will cover, rounded up
    :param formatted_data: An integer for the number of feet required to paint
    :return: feet / paint coverage, rounded up
    """
    # 1 gallon covers 400 square feet (per footer specification)
    return math.ceil(formatted_data['ft'] / 400)


def sanitize_input(input):
    """
    This universe doesn't allow for negative numbers of rooms or feet
    :param input: Any number (int/float/str) or None
    :return: The absolute, floored integer number (floats will be floored). None/invalid -> 0
    """
    try:
        if input is None:
            return 0
        # Allow strings like '10.5' and numbers
        value = float(input)
        # Floor then abs to match expectations (e.g., 10.9 -> 10)
        # abs is applied to ensure non-negative
        from math import floor
        return abs(int(floor(value)))
    except (ValueError, TypeError):
        return 0
