
import logging
import sqlite3

path_to_db = "other/botBD.sqlite"


def logger(statement):
    logging.basicConfig(
        level=logging.INFO,
        filename="logs.log",
        format=f"[Executing] [%(asctime)s] | [%(filename)s LINE:%(lineno)d] | {statement}",
        datefmt="%d-%b-%y %H:%M:%S"
    )
    logging.info(statement)


def handle_silently(function):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            logger("{}({}, {}) failed with exception {}".format(
                function.__name__, repr(args[1]), repr(kwargs), repr(e)))
        return result

    return wrapped


def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())


def add_requestx(user_id, user_first_name, req_theme, req_id, req_txt, req_date):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_req "
                   "(user_id, user_first_name, req_theme, req_id, req_txt, req_date) "
                   "VALUES (?, ?, ?, ?, ?, ?)",
                   [user_id, user_first_name, req_theme, req_id, req_txt, req_date])
        db.commit()


def get_req(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_req WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


def update_requestx(user_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_req SET XXX WHERE user_id = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


def add_userx(user_id, user_status):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_users "
                   "(user_id, user_status) "
                   "VALUES (?, ?)",
                   [user_id, user_status])
        db.commit()


def get_userx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


def update_userx(user_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_users SET XXX WHERE user_id = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


def create_bdx():
    with sqlite3.connect(path_to_db) as db:
        # Создание БД с хранением данных пользователей
        check_sql = db.execute("PRAGMA table_info(storage_req)")
        check_sql = check_sql.fetchall()
        check_create_req = [c for c in check_sql]
        if len(check_create_req) == 7:
            print("DB was found(1/1)")
        else:
            db.execute("CREATE TABLE storage_req("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "user_id INTEGER, user_first_name TEXT, req_theme TEXT, "
                       "req_id TEXT, req_txt TEXT, req_date TIMESTAMP)")
            print("DB was not found(1/1) | Creating...")
        check_sql = db.execute("PRAGMA table_info(storage_users)")
        check_sql = check_sql.fetchall()
        check_create_users = [c for c in check_sql]
        if len(check_create_users) == 3:
            print("DB was found(2/2)")
        else:
            db.execute("CREATE TABLE storage_users("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "user_id INTEGER, user_status TEXT)")
            print("DB was not found(2/2) | Creating...")
        db.commit()
