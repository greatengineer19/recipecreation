import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.post(
    "/recipes",
    json={"title":"Tomato Soup","making_time":"15 min","serves":"5 people","ingredients":"onion, tomato, seasoning, water","cost":450}
)
print("STATUS CODE:", response.status_code)
print("RESPONSE:", response.json())
