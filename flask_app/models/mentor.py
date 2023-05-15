import re
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Mentor:

    dB = "socialwave_data"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO mentors (first_name, last_name, username, email, password) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s);
        """
        result = MySQLConnection(cls.dB).query_db(query)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM mentors;
        """
        results = MySQLConnection(cls.dB).query_db(query)
        return cls(results)
    
    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT * FROM mentors WHERE id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return cls(results[0]) if results else None
    
    @classmethod
    def get_by_username(cls, username):
        query = """
            SELECT * FROM mentors WHERE username = %(username)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"username": username})
        return cls(results[0]) if results else None
    
    @classmethod
    def get_by_email(cls, email):
        query = """
            SELECT * FROM mentors WHERE email = %(email)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"email": email})
        return cls(results[0]) if results else None
    
    @classmethod
    def update_email(cls, id):
        query = """
            UPDATE mentors SET email = %{email}s WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return cls(result[0]) if result else None
    
    @classmethod
    def update_password(cls, id):
        query = """
            UPDATE mentors SET password = %{password}s WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return cls(result[0]) if result else None
    
    @staticmethod
    def validate_registration(mentor):
        is_valid = True

        if len(mentor["first_name"]) < 1:
            is_valid = False
            flash("First Name is required", "registration")
        if len(mentor["last_name"]) < 3:
            is_valid = False
            flash("Last Name is required", "registration")
        if Mentor.get_by_username(mentor["username"]):
            is_valid = False
            flash("Username is already taken", "registration")
        if len(mentor["username"]) < 1:
            is_valid = False
            flash("Username is required", "registration")
        if len(mentor["password"]) < 1:
            is_valid = False
            flash("Password is required", "registration")
        if len(mentor["password"]) <= 4:
            is_valid = False
            flash("Password must contain at least 5 characters", "registration")
        if mentor["password"] != mentor["confirm_password"]:
            is_valid = False
            flash("Password does not match", "registration")
        if Mentor.get_by_email(mentor["email"]):
            is_valid = False
            flash("Email address already used", "registration")
        if not EMAIL_REGEX.match(mentor["email"]):
            is_valid = False
            flash("Invalid Email Address", "registration")

        return is_valid