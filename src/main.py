# from rag import read_doc,chat
from data.sqldb import create_db_and_tables,get_session
import uvicorn
import os
from api.app import app

if not os.path.exists("/statics"):
    os.mkdir("/statics")

def start():
    create_db_and_tables()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    start()
