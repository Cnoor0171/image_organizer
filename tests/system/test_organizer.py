from organizer import Organizer


def test_organizer(sample_root_path, sample_db_path):
    assert sample_root_path.exists()
    Organizer(sample_root_path, sample_db_path)
