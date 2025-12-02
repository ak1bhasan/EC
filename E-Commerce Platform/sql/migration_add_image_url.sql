-- Migration: add image_url column to products table (if not present)
-- Run this against your MySQL database when migrating schema.

ALTER TABLE products
ADD COLUMN IF NOT EXISTS image_url VARCHAR(255) NULL;

-- If your MySQL version doesn't support IF NOT EXISTS for ALTER COLUMN,
-- you can guard it manually in SQL or use a migration tool like Alembic.
