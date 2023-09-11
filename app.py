from flask import Flask, jsonify, request
import os
import psycopg2

app = Flask(__name__)

# Define your PostgreSQL database credentials
db_host = os.environ.get("DATABASE_HOST")
db_port = os.environ.get("DATABASE_PORT")
db_name = os.environ.get("DATABASE_NAME")
db_user = os.environ.get("DATABASE_USER")
db_password = os.environ.get("DATABASE_PASS")


@app.route('/get_otp', methods=['GET'])
def get_data():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()

        # nick = request.args.get('nick')
        status = "no"

        # Execute a SELECT query to retrieve data with the specific id
        cursor.execute(
            "SELECT msisdn, code, waktu_buat, status FROM confirmcode WHERE status = %s ORDER BY waktu_buat DESC",
            (status,)
        )

        data = cursor.fetchmany(5)

        if data:
            print(data)
            # Return the data as a JSON response
            return jsonify({'data OTP': data})
        else:
            return jsonify({'message': 'Data not found'})
    except (Exception, psycopg2.Error) as error:
        return jsonify({'error': str(error)})


if __name__ == '__main__':
    app.run()
