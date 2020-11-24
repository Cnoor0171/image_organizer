import pytest
from hashing import file_hasher


@pytest.fixture
def sample_file_path(tmp_path):
    file1 = tmp_path / "sample_file"
    file1.write_text("sample content")

    return file1


def dir_hash_test(sample_file_path):
    hash1 = file_hasher.file_hash(sample_file_path)
    hash2 = file_hasher.file_hash(sample_file_path)
    assert hash1 == hash2


def dir_hash_rename_file_test(sample_file_path):
    hash1 = file_hasher.file_hash(sample_file_path)
    renamed = sample_file_path.parent / "filex"
    sample_file_path.rename(renamed)
    hash2 = file_hasher.file_hash(renamed)
    assert hash1 == hash2


def dir_hash_edit_file_test(sample_file_path):
    hash1 = file_hasher.file_hash(sample_file_path)
    sample_file_path.write_text("edited content")
    hash2 = file_hasher.file_hash(sample_file_path)
    assert hash1 != hash2
