import db

def get_outgoing_events(user_id):
    sql = """SELECT E.*, U.username killer_username, T.username target_username
             FROM Events E
             LEFT JOIN users U ON E.user_id = U.id 
             LEFT JOIN users T  ON E.target_id = T.id
             WHERE E.user_id = ? AND confirm_status = 0
             ORDER BY id DESC """
    return db.query(sql, [user_id])
#Näissä 2:ssa vielä kehitettävää! mahd. yhdistäminen?
def get_incoming_events(user_id):
    sql = """SELECT E.*, U.username killer_username, T.username target_username
             FROM Events E
             LEFT JOIN users U ON E.user_id = U.id 
             LEFT JOIN users T  ON E.target_id = T.id
             WHERE E.target_id = ? AND confirm_status = 0
             ORDER BY id DESC"""
    return db.query(sql, [user_id])

def get_event(event_id):
    sql = """SELECT E.*, U.username killer_username, T.username target_username
                FROM Events E
                LEFT JOIN Users U ON E.user_id = U.id 
                LEFT JOIN Users T  ON E.target_id = T.id
                WHERE E.id = ? """
    result = db.query(sql, [event_id])
    return result[0] if result else None

def get_murders():
    sql = """SELECT e.id, u.username killer_username, t.username target_username, e.zip
            FROM Events e
             LEFT JOIN users u ON e.user_id = u.id 
             LEFT JOIN users t  ON e.target_id = t.id
             WHERE confirm_status = 1
             ORDER BY e.id DESC
             """
    return db.query(sql)


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
    sql = "INSERT INTO events (user_id, target_id, zip, weapon_type, confirm_status) VALUES (?, ?, NULL, NULL, 0)"
    db.execute(sql, [user_id, target_id])
    event_id = db.last_insert_id()
    return event_id

def edit_event(event_id, zip_code, weapon_type):
    if zip_code != None:
        sql = "UPDATE Events SET zip = ? WHERE id = ?"
        db.execute(sql, [zip_code, event_id])
    if weapon_type != None:
        sql = "UPDATE Events SET weapon_type = ? WHERE id = ?"
        db.execute(sql, [weapon_type, event_id])

def confirm(event_id, confirm_status):
    sql = "UPDATE Events SET confirm_status = ? WHERE id = ?"
    db.execute(sql, [confirm_status, event_id])

def delete_event(event_id):
    sql = "DELETE FROM Events WHERE id = ?"
    db.execute(sql, [event_id])


