# migrate.py
from config import engine, Base
import utils.models  # ensures models are imported

print("Dropping and recreating tables...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Migration complete.")
