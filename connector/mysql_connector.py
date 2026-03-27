"""
MySQL Database Connector Module
Provides centralized database connection management for the Healthcare Management System.
"""

import mysql.connector as sqltor
from config import SQL


class MySQLConnector:
    """
    Singleton class to manage MySQL database connections.
    Ensures a single connection instance is reused across the application.
    """
    
    _instance = None
    _connection = None
    _cursor = None
    
    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super(MySQLConnector, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """
        Get or create a database connection.
        
        Returns:
            tuple: (connection, cursor) objects
        """
        if self._connection is None or not self._connection.is_connected():
            self._connection = sqltor.connect(
                host=SQL.host,
                user=SQL.user,
                passwd=SQL.password,
                database=SQL.database
            )
            self._cursor = self._connection.cursor()
        
        return self._connection, self._cursor
    
    def close_connection(self):
        """Close the database connection and cursor"""
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None
    
    def commit(self):
        """Commit the current transaction"""
        if self._connection and self._connection.is_connected():
            self._connection.commit()
    
    def rollback(self):
        """Rollback the current transaction"""
        if self._connection and self._connection.is_connected():
            self._connection.rollback()


def get_db_connection():
    """
    Convenience function to get database connection and cursor.
    
    Returns:
        tuple: (connection, cursor) objects
    
    Example:
        con, cursor = get_db_connection()
        cursor.execute("SELECT * FROM patients")
        results = cursor.fetchall()
    """
    connector = MySQLConnector()
    return connector.get_connection()


def close_db_connection():
    """
    Convenience function to close the database connection.
    
    Example:
        close_db_connection()
    """
    connector = MySQLConnector()
    connector.close_connection()


def commit_transaction():
    """
    Convenience function to commit the current transaction.
    
    Example:
        commit_transaction()
    """
    connector = MySQLConnector()
    connector.commit()


def rollback_transaction():
    """
    Convenience function to rollback the current transaction.
    
    Example:
        rollback_transaction()
    """
    connector = MySQLConnector()
    connector.rollback()
