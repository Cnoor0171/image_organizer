import pytest
from hashing import dir_hasher


@pytest.fixture
def sample_dir_path(tmp_path):
    file1 = tmp_path / "file1"
    file1.touch()

    file2 = tmp_path / "file2"
    file2.write_text("sample content")

    dir1 = tmp_path / "dir1"
    dir1.mkdir()

    file3 = dir1 / "file3"
    file3.write_text("sample content 2")

    return tmp_path


def dir_hash_test(sample_dir_path):
    hash1 = dir_hasher.dir_hash(sample_dir_path)
    hash2 = dir_hasher.dir_hash(sample_dir_path)
    assert hash1 == hash2


def dir_hash_rename_file_test(sample_dir_path):
    hash1 = dir_hasher.dir_hash(sample_dir_path)
    (sample_dir_path / "file1").rename(sample_dir_path / "filex")
    hash2 = dir_hasher.dir_hash(sample_dir_path)
    assert hash1 == hash2


def dir_hash_move_file_test(sample_dir_path):
    hash1 = dir_hasher.dir_hash(sample_dir_path)
    (sample_dir_path / "file1").rename(sample_dir_path / "dir1" / "file1")
    hash2 = dir_hasher.dir_hash(sample_dir_path)
    assert hash1 == hash2


def dir_hash_swap_files_test(sample_dir_path):
    hash1 = dir_hasher.dir_hash(sample_dir_path)
    (sample_dir_path / "file1").rename(sample_dir_path / "filex")
    (sample_dir_path / "file2").rename(sample_dir_path / "file1")
    (sample_dir_path / "filex").rename(sample_dir_path / "file2")
    hash2 = dir_hasher.dir_hash(sample_dir_path)
    assert hash1 == hash2
