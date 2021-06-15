import pytest
from autoupdater.countryscript.country_updater import Country_Updater


updater = None


@pytest.fixture(scope="module")
def updater(username, password):
    global updater
    updater = Country_Updater(
        "MosquitoHabitatMapper",
        "2793f3d9c4d4447ea4f21b3ad74965d4",
        "02e3c448f42e4c35a2dd0c6cbbf42d85",
        username,
        password,
    )
    return updater


def teardown_test_data_collection(test_data_collection):
    updater.temp_layer.delete()


def test_data_collection(updater):
    data = updater.get_data()
    assert not data.empty
    overwrite, delete = updater.update_layers()
    assert overwrite and delete
