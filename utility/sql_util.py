"""
SQL helpers: transactions and query execution.
Connection lifecycle is delegated to connector.mysql_connector (import only here).
"""

from mysql_connector import MySQLConnector


def _cursor():
    _, cur = MySQLConnector().get_connection()
    return cur


def execute_query(query, params=None):
    """Execute a SQL statement (writes or DDL) without returning rows."""
    cur = _cursor()
    if params is not None:
        cur.execute(query, params)
    else:
        cur.execute(query)


def fetch_all(query, params=None):
    """Execute a SELECT and return all rows."""
    cur = _cursor()
    if params is not None:
        cur.execute(query, params)
    else:
        cur.execute(query)
    return cur.fetchall()


def fetch_one(query, params=None):
    """Execute a SELECT and return a single row (or None)."""
    cur = _cursor()
    if params is not None:
        cur.execute(query, params)
    else:
        cur.execute(query)
    return cur.fetchone()


def close_db_connection():
    MySQLConnector().close_connection()


def commit_transaction():
    conn, _ = MySQLConnector().get_connection()
    if conn and conn.is_connected():
        conn.commit()


def rollback_transaction():
    conn, _ = MySQLConnector().get_connection()
    if conn and conn.is_connected():
        conn.rollback()
