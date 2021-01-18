from organizer import Organizer
from organizer.db.schema import EntityTypeId


def test_organizer_entity_scanning(sample_root_path, tmp_path):
    organizer = Organizer(sample_root_path, tmp_path / "sample.db")
    organizer.analyze_root()

    assert len(organizer.get_all_entities()) == 9
    names = {
        (entity.name, entity.type_) for entity in organizer.get_all_entities().values()
    }
    assert names == {
        ("file1", EntityTypeId.Unkown),
        ("file2.txt", EntityTypeId.Unkown),
        ("file3.jpg", EntityTypeId.Image),
        ("file4.gif", EntityTypeId.Gif),
        ("file5.mp4", EntityTypeId.Video),
        ("file6.png", EntityTypeId.Image),
        ("sub1", EntityTypeId.Gallery),
        ("sub2file1", EntityTypeId.Unkown),
        ("sub2file2.flv", EntityTypeId.Video),
    }
