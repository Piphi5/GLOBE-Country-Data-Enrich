import pytest
from autoupdater.countryscript.country_updater import Country_Updater


updater = None


@pytest.fixture(scope="module")
def updater(username, password):
    global updater
    updater = Country_Updater(
        "LandCover",
        "ff0dda11e84141c0a630c47e2a8203bf",
        "c68acbfc68db4409b495fd4636646aa6",
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
