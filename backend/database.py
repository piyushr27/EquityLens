from pymongo import MongoClient
from pymongo.database import Database
from config import settings
from typing import Optional
import json
from bson import ObjectId

class MongoDBConnection:
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(
                settings.mongodb_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000
            )
            # Verify connection
            self.client.admin.command('ping')
            self.db = self.client[settings.database_name]
            # Create indexes
            self.db.cap_tables.create_index("company_name")
            self.db.queries.create_index("company_id")
            return self.db
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            print(f"Connection string: {settings.mongodb_url}")
            print("Make sure MongoDB is running and authentication credentials are correct.")
            raise
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
    
    def insert_cap_table(self, data: dict):
        """Insert a cap table"""
        result = self.db.cap_tables.insert_one(data)
        return str(result.inserted_id)
    
    def get_cap_table(self, table_id: str):
        """Get a cap table by ID"""
        return self.db.cap_tables.find_one({"_id": ObjectId(table_id)})
    
    def get_cap_table_by_name(self, company_name: str):
        """Get cap table by company name"""
        return self.db.cap_tables.find_one({"company_name": company_name})
    
    def save_query(self, query_data: dict):
        """Save a query and response"""
        result = self.db.queries.insert_one(query_data)
        return str(result.inserted_id)
    
    def get_query_history(self, company_id: str, limit: int = 10):
        """Get query history for a company"""
        return list(self.db.queries.find(
            {"company_id": company_id}
        ).sort("timestamp", -1).limit(limit))

# Global connection instance
db_connection = MongoDBConnection()
