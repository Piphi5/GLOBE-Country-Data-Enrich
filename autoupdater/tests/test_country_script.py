import pytest
from autoupdater.countryscript.country_updater import Country_Updater


@pytest.fixture(scope="module")
def updater(username, password):
    updater = Country_Updater(username, password)
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
