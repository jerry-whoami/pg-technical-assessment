# Postgres Supplements: Food Delivery Demo

This folder contains schema and seed data to create a Postgres test database for the SQL queries in the assessment.

## Files

- `schema_postgres.sql` — DDL to create tables in Postgres (with foreign keys, adapted types).
- `seed_postgres.sql` — INSERT statements with synthetic data (120 deliveries, 18 delivery persons, 22 restaurants, 120 orders).

## Quick start

Setup Database in a postgres shell

```sql
CREATE DATABASE your_db;
CREATE USER your_user WITH ENCRYPTED PASSWORD 'your_pass';
GRANT ALL PRIVILEGES ON DATABASE your_db TO your_user;
ALTER DATABASE your_db OWNER TO your_user;
```

Create the schema and seed the database from a normal shell

```bash
psql -U your_user -d your_db -f schema_postgres.sql
psql -U your_user -d your_db -f seed_postgres.sql
```

Login into the database for testing queries

```bash
psql -d your_db 
```

Verify:

```sql
\dt
SELECT COUNT(*) FROM deliveries;
```

Notes:
- `is_active` is BOOLEAN in Postgres (TRUE/FALSE).
- Data covers ~120 days, so "last 30 days" and "last 3 months" filters are testable.
