CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    date DATE,
    open FLOAT,
    close FLOAT,
    volume BIGINT
);
