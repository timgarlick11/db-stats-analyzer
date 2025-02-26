# Postgres Database Insights Dashboard

A Python Dash application for visualizing and analyzing your PostgreSQL database usage. This project pulls metrics from various Postgres system views and extensions—such as `pg_stat_user_tables`, `pg_stat_statements`, `pg_locks`, and others—to help you identify bottlenecks, slow queries, table usage patterns, and more.

## Features

1. **Table Usage**  
   - Visualizes sequential scans, index scans, and live tuples from `pg_stat_user_tables`.

2. **Table Sizes**  
   - Displays total table size and a breakdown of table vs. index size.

3. **Index Usage**  
   - Shows index scan counts and sizes to reveal how effectively your indexes are being used.

4. **Slow Queries**  
   - Relies on `pg_stat_statements` to show the top queries by total/mean execution time.

5. **Locks**  
   - Pulls from `pg_locks` and `pg_stat_activity` to display any waiting locks in your database.

6. **Vacuum Stats**  
   - Shows when each table was last vacuumed/analyzed, plus dead tuple counts.

7. **Connection Stats**  
   - Reports on total and active connections (`pg_stat_activity`) for load monitoring.

8. **Recommendations**  
   - Provides simple tips on indexing, vacuuming, or slow queries based on retrieved stats.

---

## Prerequisites

1. **Python 3.9+** (Recommended)
2. **PostgreSQL** (Local or remote)
   - Make sure you have valid credentials for a user that can connect to your target database.
3. **pg_stat_statements Extension** (Optional but recommended)
   - Needed to see slow query data. Instructions below on enabling it.

---

## Quick Start

1. **Clone or Download** this repository to your local machine.
2. **Install Python dependencies** with:
   ```bash
   pip install -r requirements.txt
3. **Configure your database credentials in config/db_config.py.
4. **(Optional) Enable pg_stat_statements if you want slow query stats.
5. **Run the dashboard with python app.py
6. **Open http://127.0.0.1:8050 in your browser.


macOS specific:

1. Install Python (if needed): brew install python
2. check version: python3 --version
3. Create and activate a virtual environment (recommended): python3 -m venv venv
source venv/bin/activate
4. Install dependencies: pip install -r requirements.txt
5. Update db_config.py to match your environment:
DB_CONFIG = {
    "host": "your_db_host",
    "port": 5432,
    "database": "your_database",
    "user": "your_username",
    "password": "your_password"
}
6. Enable pg_stat_statements (Optional for slow query data):
   a: Locate and edit your postgresql.conf file (commonly found at /opt/homebrew/var/postgres/postgresql.conf for Apple Silicon): shared_preload_libraries = 'pg_stat_statements'
   b. Restart PostgreSQL.
   c. In psql or pgAdmin, run: CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
7. Run the dashboard in command line with: python app.py



WINDOWS:

1. Install Python 3:

      Download Python for Windows and run the installer.
      Make sure to check “Add Python to PATH” during the setup.
      
2. Create and activate a virtual environment (recommended): python -m venv venv
venv\Scripts\activate

3. install dependencies: pip install -r requirements.txt


4. Update db_config.py: DB_CONFIG = {
    "host": "your_db_host",
    "port": 5432,
    "database": "your_database",
    "user": "your_username",
    "password": "your_password"
}

5. Enable pg_stat_statements (Optional for slow queries):

   a. Locate and edit postgresql.conf (commonly in C:\Program Files\PostgreSQL\<version>\data\postgresql.conf): shared_preload_libraries = 'pg_stat_statements'
   b. Restart PostgreSQL from the Services panel.
   c. Run: CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

6. Run the dashboard: python app.py


7. Then open http://127.0.0.1:8050 in your browser.


Troubleshooting
1. Slow Queries Not Populating
      -Verify you enabled pg_stat_statements in postgresql.conf.
      -Ensure you ran: CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
      -Check that your user has permission. If needed, connect as a superuser.
2. Connection Errors
      -Double-check your database credentials in db_config.py.
      -If running Postgres in Docker, ensure ports are properly mapped (e.g., -p 5432:5432).
3. Vacuum/Analyze Stats Not Updating
      -Your database may not have been vacuumed recently. Manually run VACUUM or wait for autovacuum.
4. No Data
      -Certain views (like slow queries or locks) may be empty if no relevant activity is happening.





