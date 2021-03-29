# Usage steps

## Setup environment

- install virtual environment ( $ virtualenv venv )
- activate environment ( $ source venv/bin/activate )
- install packages ( $ pip install -r requirements.txt )
- export flask app ( $ export FLASK_APP=app.py )

## SQL Alchemy migrations

- Init (first time only)
  - flask db init
- Create migration (after each model change)
  - flask db migrate
- Apply migration (after migration created)
  - flask db upgrade
    