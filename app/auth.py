from flask import Blueprint, render_template, request, flash, session

import hashlib

import mysql.connector

from db import BookingManager

from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/home', methods=['Get', 'Post'])
def home():
    if request.method == 'POST':
        try:
            # Fetch or determine the user ID
            iduser = session.get('user_id')  # Example: Get user ID from session

            full_name = request.form.get('name').strip()
            email = request.form.get('email').strip()

            date_time = request.form.get('datetime')
            datetime_order = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current datetime

            no_of_cars = request.form.get('select1')

            special_requests = request.form.get('message').strip()

            # Parse datetime string to appropriate format
            datetime_appointment = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

            # Book the appointment
            BookingManager()._book(iduser, datetime_order, datetime_appointment, no_of_cars, special_requests)

            flash("Booking successful")
        except Exception as e:
            flash("Invalid operation: " + str(e))
    return render_template("index.html")




