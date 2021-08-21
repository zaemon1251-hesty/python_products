import psycopg2
connection = psycopg2.connect("host=127.0.0.1 port=5432 dbname=shop user=postgres password=h711838")
cur = connection.cursor()
cur.execute("select shohin_id, shohin_mei from shohin")
for row in cur:
     print(*row)