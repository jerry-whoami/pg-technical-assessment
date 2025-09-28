# Postgres Supplements: Food Delivery Demo

This folder contains schema and seed data to create a Postgres test database for the SQL queries in the assessment.

## Files

- `schema_postgres.sql` — DDL to create tables in Postgres (with foreign keys, adapted types).
- `seed_postgres.sql` — INSERT statements with synthetic data (120 deliveries, 18 delivery persons, 22 restaurants, 120 orders).
- CSVs can also be reused from the SQLite version.

## Quick start

In a local Postgres shell:

```bash
psql -U your_user -d your_db -f schema_postgres.sql
psql -U your_user -d your_db -f seed_postgres.sql
```

Verify:
```sql
\dt
SELECT COUNT(*) FROM deliveries;
```

Notes:
- `is_active` is BOOLEAN in Postgres (TRUE/FALSE).
- Data covers ~120 days, so "last 30 days" and "last 3 months" filters are testable.
