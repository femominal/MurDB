import requests

url = "http://127.0.0.1:8000/export"
headers = {
    "x-api-key": "dev-secret-key",
    "Content-Type": "application/json"
}
json_data = {
    "db_path": "example.db"
}

response = requests.post(url, headers=headers, json=json_data)

with open("backup_http.sq", "wb") as f:
    f.write(response.content)

print("Downloaded:", response.status_code)
