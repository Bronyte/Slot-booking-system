import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vlthU*W_Fr94o=Eme6Re',
    database='car_wash_db'
)

class BookingManager:
    def __init__(self):
        self.cursor = db.cursor()

    def _get_time_slots(self, dow):
        self.cursor.execute("SELECT * FROM appointment WHERE day_of_week = %s", (dow,))
        records = self.cursor.fetchall()

        slots = []
        for record in records:
            slot = {
                'idappointment': record[0],
                'day_of_week': record[1],
                'start_time': record[2],
                'end_time': record[3]
            }
            slots.append(slot)

        return slots

    def _time_to_slot(self, t, dow):
        slots = self._get_time_slots(dow)
        for slot in slots:
            if slot['start_time'] <= t <= slot['end_time']:
                return slot['idappointment']
            
    def _find_booked_slots(self, d, dow):
        self.cursor.execute("SELECT idappointment FROM booking WHERE DATE(datetime_of_appointment) = %s", (d,))
        records = self.cursor.fetchall()

        slots = []
        for record in records:
            slot = {
                'idappointment': record[0],
            }
            slots.append(slot)
        return slots
            
    def _find_available_slots(self, d, dow):
        booked_slots = self._find_booked_slots(d, dow)
        all_available_slots = self._get_time_slots(dow)

        available_slots = []
        for booked_slot in booked_slots:
            for available_slot in all_available_slots:
                if booked_slot['idappointment'] == available_slot['idappointment']:
                    available_slots.append(available_slot)
        return available_slots
    
    def get_date(self, datetime):
        parsed_datetime = datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S')
        return  parsed_datetime.date()
    
    def get_time(self, datetime):
        parsed_datetime = datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S')
        return parsed_datetime.time()

    def get_dow(self, datetime):
        parsed_datetime = datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S')
        return parsed_datetime.strftime('%a')
    
    def _book(self, iduser, datetime_order, datetime_appointment, cars, requests):
        time = self.get_time(datetime_appointment)
        date = self.get_date(datetime_appointment)
        day_of_week = self.get_dow(datetime_appointment)

        slot = self.time_to_slot(time, day_of_week)

        sql = "INSERT INTO booking (iduser, idappointment, datetime_of_order, datetime_of_appointment, cars, requests) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (iduser, slot, datetime_order, datetime_appointment, cars, requests)
        self.cursor.execute(sql, values)
        db.commit()
