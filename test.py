from sshtunnel import SSHTunnelForwarder
import pymysql
 
with SSHTunnelForwarder(
    ('ec2-18-179-45-131.ap-northeast-1.compute.amazonaws.com'),
    ssh_username="ec2-user",
    ssh_pkey="/home/ec2-user/ab3/tokyo_keypair.pem",
    remote_bind_address=('ab3-rds.ctvrgbztahch.ap-northeast-1.rds.amazonaws.com', 3306)
) as tunnel:
    print("****SSH Tunnel Established****")
 
    db = pymysql.connect(
        host='127.0.0.1', user="admin",
        password="ab3rdsmysql", port=tunnel.local_bind_port
    )
    # Run sample query in the database to validate connection
    try:
        # Print all the databases
        with db.cursor() as cur:
            cur.execute('select * from AB3.ab3_orders;')
            for order in cur:
                print(order)
    finally:
        db.close()
 
print("YAYY!!")