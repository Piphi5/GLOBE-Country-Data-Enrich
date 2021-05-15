import pytest
from autoupdater.countryscript.country_updater import Country_Updater


@pytest.fixture(scope="module")
def updater(username, password):
    updater = Country_Updater(
        "MosquitoHabitatMapper",
        "2793f3d9c4d4447ea4f21b3ad74965d4",
        "02e3c448f42e4c35a2dd0c6cbbf42d85",
        username,
        password,
    )
    yield updater

    # make sure temp_layer gets deleted if anything fails
    print("Running teardown")
    try:
        result = updater.temp_layer.delete()
        if result:
            print("Successfully deleted temp layer")
    except Exception:
        return


def test_data_collection(updater):
    data = updater.get_data()
    assert not data.empty


def test_upload_data(updater):
    overwrite, delete = updater.update_layers()
    assert overwrite and delete
