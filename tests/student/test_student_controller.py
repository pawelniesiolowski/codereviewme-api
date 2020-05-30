def test_index(client):
    response = client.get('/students')
    assert response.status_code == 200
