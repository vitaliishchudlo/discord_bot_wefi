import os
import sys
from pathlib import Path

if not str(Path().absolute().parent) in sys.path:
    sys.path.append(str(Path().absolute().parent))

import create_database as db_creator
from test_file import go_test
from test_structure.database import DATABASE_NAME

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        db_creator.create_database()
    go_test()
