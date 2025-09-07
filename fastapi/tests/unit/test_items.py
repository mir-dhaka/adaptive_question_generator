def test_read_items_unit(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert "message" in response.json()
