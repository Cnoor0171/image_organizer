from types import SimpleNamespace

import pytest

from organizer import Organizer
from organizer.hashing import file_hasher


@pytest.fixture
def mocks(mocker, sample_root_path):
    mock_db_inst = mocker.Mock()
    mock_db_inst_class = mocker.patch("organizer.DBInstance", return_value=mock_db_inst)
    org = Organizer(sample_root_path, "dummy_db_path")

    return SimpleNamespace(
        org=org,
        mock_db_inst=mock_db_inst,
        mock_db_inst_class=mock_db_inst_class,
    )


def test_db_path(mocks):
    mocks.mock_db_inst_class.assert_called_once_with("dummy_db_path")


def test_analyze_root(mocks):
    mocks.org.analyze_root()
    expected_filenames = {
        "file1",
        "file2.txt",
        "file3.jpg",
        "file4.gif",
        "file5.mp4",
        "file6.png",
        "sub1",
        "sub2file1",
        "sub2file2.flv",
    }

    assert len(mocks.org._hash_to_file_path) == 9
    file_names = {file_path.name for file_path in mocks.org._hash_to_file_path.values()}
    assert file_names == expected_filenames

    assert mocks.mock_db_inst.add_enitity.call_count == 9
    file_names = {
        call_args.args[2] for call_args in mocks.mock_db_inst.add_enitity.call_args_list
    }
    assert file_names == expected_filenames


def test_get_all_entities(mocks):
    mocks.org.get_all_entities()
    assert mocks.mock_db_inst.get_all_entities.call_count == 1
    assert mocks.mock_db_inst.get_all_entities.call_args == ((), {'get_groups': False})


def test_get_entity_by_id(mocks):
    mocks.org.get_entity_by_id(1234)
    assert mocks.mock_db_inst.get_entity_by_id.call_count == 1
    assert mocks.mock_db_inst.get_entity_by_id.call_args == ((1234,), {'get_groups': False})


def test_get_entity_by_hash(mocks):
    mocks.org.get_entity_by_hash("abcd")
    assert mocks.mock_db_inst.get_entity_by_hash.call_count == 1
    assert mocks.mock_db_inst.get_entity_by_hash.call_args == (("abcd",), {})


def test_get_all_entity_types(mocks):
    mocks.org.get_all_entity_types()
    assert mocks.mock_db_inst.get_all_entity_types.call_count == 1
    assert mocks.mock_db_inst.get_all_entity_types.call_args == ((), {})


def test_get_entity_type_by_id(mocks):
    mocks.org.get_entity_type_by_id(1234)
    assert mocks.mock_db_inst.get_entity_type_by_id.call_count == 1
    assert mocks.mock_db_inst.get_entity_type_by_id.call_args == ((1234,), {})


def test_get_all_groupings(mocks):
    mocks.org.get_all_groupings()
    assert mocks.mock_db_inst.get_all_groupings.call_count == 1
    assert mocks.mock_db_inst.get_all_groupings.call_args == ((), {})


def test_get_grouping_by_id(mocks):
    mocks.org.get_grouping_by_id(1234)
    assert mocks.mock_db_inst.get_grouping_by_id.call_count == 1
    assert mocks.mock_db_inst.get_grouping_by_id.call_args == ((1234,), {})


def test_get_all_groups(mocks):
    mocks.org.get_all_groups()
    assert mocks.mock_db_inst.get_all_groups.call_count == 1
    assert mocks.mock_db_inst.get_all_groups.call_args == ((), {})


def test_get_group_by_id(mocks):
    mocks.org.get_group_by_id(1234)
    assert mocks.mock_db_inst.get_group_by_id.call_count == 1
    assert mocks.mock_db_inst.get_group_by_id.call_args == ((1234,), {})


def test_get_file_name(mocks, sample_root_path):
    hash1 = file_hasher.file_hash(sample_root_path / "file1")
    assert mocks.org.get_file_name_by_hash(hash1) is None

    mocks.org.analyze_root()

    assert mocks.org.get_file_name_by_hash(hash1) is not None
