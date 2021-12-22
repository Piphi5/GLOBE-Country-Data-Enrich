import pytest
from autoupdater.countryscript.country_updater import Country_Updater


updater = None


@pytest.fixture(scope="module")
def updater(username, password):
    global updater
    updater = Country_Updater(
        "MosquitoHabitatMapper",
        "ae4990333e9f41f489550ddbe16a9d0f",
        "4e8bdb70b3d6424b8831e9cc621cf3b6",
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
