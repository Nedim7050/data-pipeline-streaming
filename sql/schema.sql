CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS raw_transactions (
    transaction_id UUID PRIMARY KEY,
    event_ts TIMESTAMPTZ NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transactions_flat (
    transaction_id UUID PRIMARY KEY,
    event_ts TIMESTAMPTZ NOT NULL,
    event_date DATE NOT NULL,
    event_hour SMALLINT NOT NULL,
    event_dayofweek TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    amount_bucket TEXT NOT NULL,
    merchant TEXT,
    category TEXT,
    city TEXT,
    status TEXT,
    payment_method TEXT,
    currency TEXT,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transactions_flat_user_id ON transactions_flat (user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_flat_event_ts ON transactions_flat (event_ts);
CREATE INDEX IF NOT EXISTS idx_transactions_flat_category ON transactions_flat (category);

DROP MATERIALIZED VIEW IF EXISTS daily_summary;
CREATE MATERIALIZED VIEW daily_summary AS
SELECT
    event_date,
    city,
    category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    SUM(CASE WHEN status = 'APPROVED' THEN amount ELSE 0 END) AS approved_amount
FROM transactions_flat
GROUP BY event_date, city, category;

CREATE INDEX IF NOT EXISTS idx_daily_summary_date ON daily_summary (event_date);

-- Refresh helper function (optional, can be called from Airflow or manually)
CREATE OR REPLACE FUNCTION refresh_daily_summary()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY daily_summary;
END;
$$ LANGUAGE plpgsql;

