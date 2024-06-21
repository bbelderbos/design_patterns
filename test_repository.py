import pytest

from repository import Item, SQLModelRepository, CsvRepository, IRepository


@pytest.fixture
def repo_sql():
    return SQLModelRepository(db_string="sqlite:///:memory:")


@pytest.fixture
def repo_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    return CsvRepository(file_path=csv_file)


def test_add_and_get_sqlmodel(repo_sql):
    item = Item(name="Test Item")
    repo_sql.add(item)
    fetched_item = repo_sql.get("Test Item")
    assert fetched_item.name == "Test Item"


def test_add_and_get_csv(repo_csv):
    item = Item(id=1, name="Test Item")
    repo_csv.add(item)
    fetched_item = repo_csv.get("Test Item")
    assert fetched_item.name == "Test Item"


def test_add_two_items_sqlmodel(repo_sql):
    item1 = Item(name="Test Item 1")
    item2 = Item(name="Test Item 2")
    repo_sql.add(item1)
    repo_sql.add(item2)
    fetched_item1 = repo_sql.get("Test Item 1")
    fetched_item2 = repo_sql.get("Test Item 2")
    assert fetched_item1.name == "Test Item 1"
    assert fetched_item2.name == "Test Item 2"


def test_add_two_items_csv(repo_csv):
    item1 = Item(id=1, name="Test Item 1")
    item2 = Item(id=2, name="Test Item 2")
    repo_csv.add(item1)
    repo_csv.add(item2)
    fetched_item1 = repo_csv.get("Test Item 1")
    fetched_item2 = repo_csv.get("Test Item 2")
    assert fetched_item1.name == "Test Item 1"
    assert fetched_item2.name == "Test Item 2"


def test_get_non_existing_item_sqlmodel(repo_sql):
    fetched_item = repo_sql.get("Non Existing Item")
    assert fetched_item is None


def test_get_non_existing_item_csv(repo_csv):
    # need to add an item for the csv file to spring into existence
    repo_csv.add(Item(id=1, name="Test Item"))
    fetched_item = repo_csv.get("Non Existing Item")
    assert fetched_item is None


def test_abstract_methods_enforcement():
    class IncompleteRepository(IRepository):
        pass

    with pytest.raises(TypeError):
        IncompleteRepository()
