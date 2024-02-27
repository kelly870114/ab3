from flask import Flask, jsonify, request
import pymysql
import sshtunnel
import os

app = Flask(__name__)

cur_path = os.getcwd()
print(cur_path)

server = sshtunnel.SSHTunnelForwarder(
    ('ec2-18-179-45-131.ap-northeast-1.compute.amazonaws.com'),
    ssh_username="ec2-user",
    ssh_pkey= cur_path + "/tokyo_keypair.pem",
    remote_bind_address=('ab3-rds.ctvrgbztahch.ap-northeast-1.rds.amazonaws.com', 3306)
)
print("****SSH Tunnel Established****")
server.start()
# 使用已和local端綁定的port 去遠端連線MySQL
conn = pymysql.connect(
        host='0.0.0.0', user="admin",
        password="ab3rdsmysql", port=server.local_bind_port
    )


@app.route('/getData')
def get_data():
    try:
        with conn.cursor() as cursor:
            sql_cmd = 'select * from AB3.ab3_orders LIMIT 0,1000;'  # Select all columns from the 'members' table
            cursor.execute(sql_cmd)
            data = cursor.fetchall()

            orders = []
            for row in data:
                order = {
                    'order_id': row[0],
                    'table_id': row[1],
                    'orders': row[2],
                    'order_time': row[3],
                    'order_status': row[4],
                    # Add other columns here if available in the 'orders' table
                }
                orders.append(order)
            print(orders)
            return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)})
   #  finally:
   #      server.stop()

@app.route('/postData',  methods=["POST"])
def post_data():
    try:
        with conn.cursor() as cursor:
            data = request.json
            # order_id = data.get('order_id')
            table_id = data.get('table_id')
            orders = data.get('orders')
            order_time = data.get('order_time')
            order_status = data.get('order_status')
            # Insert a new row into the 'members' table
            sql_cmd = 'INSERT INTO AB3.ab3_orders (table_id, orders, order_time, order_status) VALUES (%s, %s, %s, %s)'
            cursor.execute(sql_cmd, (table_id, orders, order_time, order_status))
            conn.commit()
            return jsonify({'message': 'Data inserted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    # finally:
    #     server.stop()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
