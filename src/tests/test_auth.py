
def test_me_without_token(test_app):
    response = test_app.get("/me")
    assert response.status_code == 401
