def test_index_route_exists(client):
    res = client.get("/")
    assert res is not None