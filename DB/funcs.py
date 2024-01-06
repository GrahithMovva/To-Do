import hashlib
import db
import secrets
import datetime

logged_in_user = ""

def add_user(username,password):
    db.cursor.execute("""
                      SELECT * FROM users
                      Where username = %s
                     """,(username,))
    
    number_of_users = db.cursor.fetchall()

    if(len(number_of_users) <= 0):

        hashed_pass = hashlib.sha512()
        hashed_pass.update(str(password).encode('utf-8'))
        db.cursor.execute("""
                            INSERT INTO users (username, password, logged)
                            VALUES (%s,%s,false);
                        """,(username,hashed_pass.hexdigest()))
        
        db.conn.commit()

        return("Created account")
    
    else:
        return("Username already exists")

def login(username, password):
    hashed_pass = hashlib.sha512()
    hashed_pass.update(str(password).encode('utf-8'))
    hashed_pass = hashed_pass.hexdigest()
    db.cursor.execute("""
                    SELECT * FROM users
                    WHERE username = %s
                    AND password = %s
                    """, (username,hashed_pass))
    
    number_of_users = db.cursor.fetchall()

    if(len(number_of_users) > 0 ):
        db.cursor.execute("""
                        UPDATE users
                        SET logged = true
                        WHERE username = %s
                        AND password = %s ;
                        """, (username,hashed_pass))

        db.conn.commit()
        logged_in_user = username
        return("Logged in successfully")
    
    else:
        return("Incorrect credentials")

def get_item_id(course_name,course_type,day,month,year,hour,minutes):
    time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minutes) + ':00'
    db.cursor.execute("""
                    SELECT id from items
                    WHERE course_name = %s
                    AND course_type = %s
                    AND due_date = to_timestamp(%s,'YYYY-MM-DD HH24:MI:SS')
                    """,(course_name,course_type,time))
    
    id = db.cursor.fetchall()
    return(id[0])
    
def add_item(username,day,month,year,hour,minutes,course_name,course_type):
    time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minutes) + ':00'
    db.cursor.execute("""
                    INSERT INTO items (course_name, type, due_date,user_name)
                    VALUES(%s,%s,to_timestamp(%s,'YYYY-MM-DD HH24:MI:SS'),%s)
                    """,(course_name,course_type,time,username))
    db.conn.commit()
    return("added successfully")

def update_item(id,day,month,year,hour,minutes,course_name,course_type):
    time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minutes) + ':00'
    db.cursor.execute("""
                    UPDATE items
                    SET course_name = %s,
                    type = %s, 
                    due_date = to_timestamp(%s,'YYYY-MM-DD HH24:MI:SS')
                    WHERE id = %s 
                     """,(course_name,course_type,time,id))

    db.conn.commit()
    return("updated Successfully")

def delete_item(id):

    db.cursor.execute(""" DELETE FROM items
                      WHERE id = %s
                    """,(id,))
    
    db.conn.commit()

    
def get_item(id):

    db.cursor.execute(""" SELECT course_name,type,due_date FROM items
                      WHERE id = %s
                    """, (id,))

    item = db.cursor.fetchall()
    return(item)

def get_item_by_user(uesrname):
    
    db.cursor.execute(""" SELECT course_name,type,due_date FROM items
                      WHERE user_name = %s
                    """, (uesrname,))

    items = db.cursor.fetchall()
    return(items)

def finish_item(id):

    db.cursor.execute(""" UPDATE items
                      SET status = true
                      WHERE id = %s
                    """,(id,))
    
    db.conn.commit()

def logout(username):

    db.cursor.execute(""" UPDATE users
                      SET logged = false
                      WHERE username = %s
                      """,(username,))

    logged_in_user = ""
    db.conn.commit()

def main():
    login("Grahith","hello")

main()