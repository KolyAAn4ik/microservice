import pytest


@pytest.mark.parametrize(
    "name, surname, age, rating, expected_code",
    [
        ("AA", "BB", 20, 30, 201),
        ("CC", "DD", 10, 20, 422),
    ],
)
def test_add_user(name, surname, age, rating, expected_code, client):
    form_data = {"name": name, "surname": surname, "age": age, "rating": rating}
    request = client.post("/new_user", data=form_data, follow_redirects=True)
    if expected_code != 201:
        assert request.status_code == expected_code
    else:
        response = client.get("/")
        users = response.json()
        for user in users:
            assert user == {
                "name": name,
                "surname": surname,
                "age": age,
                "rating": rating,
                "full_name": f"{name} {surname}",
            }
