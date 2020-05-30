def test_index(client):
    response = client.get('/reviewers')
    assert response.status_code == 200
