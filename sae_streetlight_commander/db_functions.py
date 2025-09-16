import psycopg2

def connect(CONFIG):
    global conn;
    conn = psycopg2.connect(database=CONFIG.db.database,
                            host=CONFIG.db.hostname,
                            user=CONFIG.db.username,
                            password=CONFIG.db.password,
                            port=CONFIG.db.port)
    
def get_count_data(area_name):
    query = "SELECT ao.* FROM areaoccupancy ao JOIN metadata m ON ao.metadata_id = m.id WHERE m.name = %s ORDER BY ao.occupancy_time DESC LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(query, (area_name,))
    result = cursor.fetchone()
    return result[1]
