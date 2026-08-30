import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Testing Task API Endpoints")
print("=" * 60)

# Test 1: GET /
print("\n1. GET /")
resp = requests.get(f"{BASE_URL}/")
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 2: GET /health
print("\n2. GET /health")
resp = requests.get(f"{BASE_URL}/health")
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 3: GET /tasks
print("\n3. GET /tasks")
resp = requests.get(f"{BASE_URL}/tasks")
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 4: GET /tasks/1
print("\n4. GET /tasks/1")
resp = requests.get(f"{BASE_URL}/tasks/1")
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 5: GET /tasks/99 (404)
print("\n5. GET /tasks/99 (expect 404)")
resp = requests.get(f"{BASE_URL}/tasks/99")
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 6: POST /tasks with valid data (201)
print("\n6. POST /tasks with valid data (expect 201)")
resp = requests.post(f"{BASE_URL}/tasks", json={"title": "Buy milk"})
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 7: POST /tasks with empty title (400)
print("\n7. POST /tasks with empty title (expect 400)")
resp = requests.post(f"{BASE_URL}/tasks", json={"title": ""})
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 8: POST /tasks with missing title (400)
print("\n8. POST /tasks with missing title (expect 400)")
resp = requests.post(f"{BASE_URL}/tasks", json={})
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 9: POST /tasks with whitespace title (400)
print("\n9. POST /tasks with whitespace title (expect 400)")
resp = requests.post(f"{BASE_URL}/tasks", json={"title": "   "})
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 10: PUT /tasks/1 (update title)
print("\n10. PUT /tasks/1 (update title)")
resp = requests.put(f"{BASE_URL}/tasks/1", json={"title": "Learn FastAPI Properly"})
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 11: PUT /tasks/1 (update done)
print("\n11. PUT /tasks/1 (update done)")
resp = requests.put(f"{BASE_URL}/tasks/1", json={"done": True})
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 12: PUT /tasks/99 (404)
print("\n12. PUT /tasks/99 (expect 404)")
resp = requests.put(f"{BASE_URL}/tasks/99", json={"title": "Test"})
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 13: PUT /tasks/1 with empty body (400)
print("\n13. PUT /tasks/1 with empty/invalid body (expect 400)")
resp = requests.put(f"{BASE_URL}/tasks/1", json={})
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 14: DELETE /tasks/2
print("\n14. DELETE /tasks/2")
resp = requests.delete(f"{BASE_URL}/tasks/2")
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text if resp.text else '(empty body - correct for 204)'}")

# Test 15: DELETE /tasks/99 (404)
print("\n15. DELETE /tasks/99 (expect 404)")
resp = requests.delete(f"{BASE_URL}/tasks/99")
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# Test 16: GET /tasks to verify deletions and updates
print("\n16. GET /tasks (final state)")
resp = requests.get(f"{BASE_URL}/tasks")
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
