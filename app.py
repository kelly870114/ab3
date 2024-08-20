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
            sql_cmd = 'SELECT * FROM AB3.ab3_catalog LIMIT 0,10;'  # Select all columns from the 'ab3_catalog' table
            cursor.execute(sql_cmd)
            data = cursor.fetchall()

            games = []
            for row in data:
                game = {
                    'game_id': row[0],
                    'game_title': row[1],
                    'game_description': row[2],
                    'release_date': row[3],
                    'game_price': row[4],
                }
                games.append(game)
            print(games)
            return jsonify(games)
    except Exception as e:
        return jsonify({'error': str(e)})
   #  finally:
   #      server.stop()

@app.route('/postData',  methods=["POST"])
def post_data():
    try:
        with conn.cursor() as cursor:
            data = request.json
            # game_id = data.get('game_id')
            game_title = data.get('game_title')
            game_description = data.get('game_description')
            release_date = data.get('release_date')
            game_price = data.get('game_price')
            
            sql_cmd = 'INSERT INTO AB3.ab3_catalog (game_id, game_title, game_description, release_date, game_price) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql_cmd, (game_title, game_description, release_date, game_price))
            conn.commit()
            return jsonify({'message': 'Game data inserted successfully'})
    except Exception as e:
        return "Record not found", 400
    # finally:
    #     server.stop()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)