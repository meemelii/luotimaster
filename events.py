import db

def get_outgoing_events(user_id):
    sql = """SELECT E.*, U.username killer_username, T.username target_username
             FROM Events E
             LEFT JOIN users U ON E.user_id = U.id 
             LEFT JOIN users T  ON E.target_id = T.id
             WHERE E.user_id = ? AND confirm_status = 0
             ORDER BY id DESC """
    return db.query(sql, [user_id])
#Incomings and outgoings need still to be improved
def get_incoming_events(user_id):
    sql = """SELECT E.*, U.username killer_username, T.username target_username
             FROM Events E
             LEFT JOIN users U ON E.user_id = U.id 
             LEFT JOIN users T  ON E.target_id = T.id
             WHERE E.target_id = ? AND confirm_status = 0
             ORDER BY id DESC"""
    return db.query(sql, [user_id])

def get_event(event_id):
    sql = """SELECT E.id, E.user_id, E.target_id, E.zip, E.confirm_status, U.username killer_username, T.username target_username
                FROM Events E
                LEFT JOIN Users U ON E.user_id = U.id 
                LEFT JOIN Users T  ON E.target_id = T.id
                WHERE E.id = ? """
    result = db.query(sql, [event_id])
    return result[0] if result else None

def get_details(event_id):
    sql = """SELECT ED.title title, ED.info info, D.describe describe
            FROM Event_details ED
            LEFT JOIN Details D ON ED.info = D.info
            WHERE ED.event_id = ?
    """
    result = db.query(sql, [event_id])
    return result[0] if result else None

def get_weapontypes():
    sql = """SELECT title, info
            FROM details
            WHERE title = 'weapontype' """
    return db.query(sql)

def get_murder_count():
    sql = """SELECT COUNT(E.id)
            FROM Events E
            WHERE confirm_status =1
            """
    return db.query(sql)[0][0]

def get_murders(page, page_size):
    sql = """SELECT E.id, U.username killer_username, T.username target_username, E.zip, D.describe describe
            FROM Events E
             LEFT JOIN Users U ON E.user_id = U.id 
             LEFT JOIN Users T  ON E.target_id = T.id
             LEFT JOIN Event_details ED ON E.id = ED.event_id
             LEFT JOIN details D ON ED.info = D.info
             WHERE confirm_status = 1
             ORDER BY E.id DESC
             LIMIT ? OFFSET ?
             """
    limit = page_size
    offset = page_size * (page -1)
    return db.query(sql, [limit, offset])

def get_user_murders(user_id):
    sql = """SELECT e.id, u.username killer_username, t.username target_username, e.zip,  D.describe describe
            FROM Events e
             LEFT JOIN users u ON e.user_id = u.id 
             LEFT JOIN users t  ON e.target_id = t.id
             LEFT JOIN Event_details ED ON E.id = ED.event_id
             LEFT JOIN Details D ON ED.info = D.info
             WHERE confirm_status = 1 AND e.user_id = ?
             ORDER BY e.id DESC
             """
    return db.query(sql, [user_id])

def get_user_deaths(user_id):
    sql = """SELECT e.id, u.username killer_username, t.username target_username, e.zip
            FROM Events e
             LEFT JOIN users u ON e.user_id = u.id 
             LEFT JOIN users t  ON e.target_id = t.id
             WHERE confirm_status = 1 AND e.target_id = ?
             ORDER BY e.id DESC
             """
    return db.query(sql, [user_id])

def search(query):
    sql = """SELECT e.id, u.username killer_username, t.username target_username, e.zip
             FROM events e 
             LEFT JOIN users u ON e.user_id = u.id 
             LEFT JOIN users t  ON e.target_id = t.id 
             WHERE confirm_status = 1 AND
                (u.username LIKE ? OR t.username LIKE ? OR e.zip == ?)
                GROUP BY e.id ORDER BY e.id ASC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%", "%" + query + "%"])


def add_event(user_id, target_id):
    sql = "INSERT INTO events (user_id, target_id, zip, confirm_status) VALUES (?, ?, NULL, 0)"
    db.execute(sql, [user_id, target_id])
    event_id = db.last_insert_id()
    sql = "INSERT INTO Event_details (event_id, title, info) VALUES (?, 'weapontype', 'Luokittelematon') "
    db.execute(sql, [event_id])
    
    return event_id

def edit_event(event_id, zip_code, weapontype):
    if zip_code != None:
        sql = "UPDATE Events SET zip = ? WHERE id = ?"
        db.execute(sql, [zip_code, event_id])
    sql = "DELETE FROM Event_details WHERE event_id = ?"
    db.execute(sql, [event_id])
    sql = "INSERT INTO Event_details (event_id, title, info) VALUES (?, 'weapontype', ?) "
    db.execute(sql, [event_id, weapontype])

def confirm(event_id, confirm_status):
    sql = "UPDATE Events SET confirm_status = ? WHERE id = ?"
    db.execute(sql, [confirm_status, event_id])

def delete_event(event_id):
    sql = "DELETE FROM Events WHERE id = ?"
    db.execute(sql, [event_id])
    sql = "DELETE FROM Event.details WHERE id = ?"
    db.execute(sql, [event_id])

