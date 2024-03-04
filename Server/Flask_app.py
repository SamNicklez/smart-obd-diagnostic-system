from flask import Flask
from flask_cors import CORS
from supabase import create_client, Client
import os

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    response = supabase.table('users').select("*").execute()
    print (response)
    return "Home"

if __name__ == '__main__':
    app.run(debug=True)