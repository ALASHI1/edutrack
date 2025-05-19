#!/bin/bash
DB_NAME="something"
DB_USER="something"
DB_PASS="something"

echo "Creating database and user..."

# Create the database
psql -U postgres -c "CREATE DATABASE $DB_NAME;"

# Create the user
psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"

# Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
psql -U postgres -d $DB_NAME -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;"
psql -U postgres -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"

echo "✅ Done: Database '$DB_NAME' and user '$DB_USER' created and configured."
