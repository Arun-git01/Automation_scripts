import mysql.connector
import mysql


def connection_to_sql():
    conn = mysql.connector.connect(
        host='digitap-dev-db.chjy1zjdr74q.ap-south-1.rds.amazonaws.com',
        port='3306',
        user='qa.arunachalam',
        password='UbZ41V5D1PXS5gY',
        database='ocr')
    return conn
