"""Test main script""" 

from organizer import Organizer
from rest_api.app import get_flask_app


def main():
    # db_file_name = input("DB filename: ").strip() or ".temp.db"
    # organizer_root = input("Gallery root: ").strip() or "data"
    db_file_name = ".temp.db"
    organizer_root = "data"
    # os.remove(db_file_name)
    organizer = Organizer(organizer_root, db_file_name)
    organizer.analyze_root()
    # print(organizer.get_entities())
    # print(organizer.get_types())
    # print(organizer.get_groupings())
    # print(organizer.get_groups())
    # print(organizer.get_file_name("0d5a577a45c97e9741182c062cef189a5c852964"))
    # print(organizer.get_file_name("72ee847ea13f7fe0f15a577868855d7e4a5f4000"))

if __name__ == '__main__':
    # main()
    db_file_name = "tmp-data/sample.db"
    organizer_root = "tmp-data/sample_root"
    organizer = Organizer(organizer_root, db_file_name)
    # print("analyzing root")
    # organizer.analyze_root()
    # print("analyzed root")
    app = get_flask_app(organizer)
    app.run(debug=False, port=9001)
