def test_create_user(test_client):
    """Test creating a new user via POST request."""
    response = test_client.post('/create_user', json={'phone': '12345672290'})
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'
