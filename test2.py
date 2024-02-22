import sshtunnel
import pymysql
# 開啟一個通道穿越REMOTE SERVER直到REMOTE PRIVATE SERVER
# 並且將他和local端的port綁定
server = sshtunnel.SSHTunnelForwarder(
    ('ec2-18-179-45-131.ap-northeast-1.compute.amazonaws.com'),
    ssh_username="ec2-user",
    ssh_pkey="/home/ec2-user/ab3/tokyo_keypair.pem",
    remote_bind_address=('ab3-rds.ctvrgbztahch.ap-northeast-1.rds.amazonaws.com', 3306)
)
print("****SSH Tunnel Established****")
server.start()
# 使用已和local端綁定的port 去遠端連線MySQL
conn = pymysql.connect(
        host='127.0.0.1', user="admin",
        password="ab3rdsmysql", port=server.local_bind_port
    )

with conn.cursor() as cur:
    cur.execute('select * from AB3.ab3_orders;')
    for order in cur:
        print(order)

server.stop()