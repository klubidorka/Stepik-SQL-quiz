import pymysql
from pymysql.cursors import DictCursor

tablename = "AIRTRANS"


def execute_statement(connection, stmt, commit=False, return_result=False):
    cursor = connection.cursor()
    cursor.execute(stmt)
    if commit:
        connection.commit()
    if return_result:
        return cursor.fetchall()


def run_query_from_file(path_to_file, connection):
    with open(path_to_file, mode='r') as sql_script:
        return execute_statement(connection, sql_script.read(), True, True)


def connect_to_airtrans_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        execute_statement(connection, f"CREATE DATABASE IF NOT EXISTS {tablename}")
        execute_statement(connection, f"USE {tablename}")
        with open('sql/INIT_DB.sql', mode='r') as initial_sql_script:
            sqlStatements = initial_sql_script.read().split(';')
            for statement in sqlStatements:
                if len(str.strip(statement)) != 0:
                    execute_statement(connection, statement)
            connection.commit()
            print("database is created and filled")

    except Exception as e:
        print("Exeception occured:{}".format(e))
    return connection


def release_resources(connection):
    execute_statement(connection, f"DROP DATABASE {tablename}", commit=True)
    connection.close()


def main():
    connection = connect_to_airtrans_db()
    try:
        result = run_query_from_file('sql/tasks/2.sql', connection)
        print(result)
    finally:
        release_resources(connection)


if __name__ == '__main__':
    main()
