-- Run these queries against data/crypto.db using SQLite.
-- Query 1: Count price observations for each coin.
SELECT
    c.coin_id,
    c.name,
    COUNT(p.timestamp_utc) AS price_points
FROM top_coins AS c
LEFT JOIN coin_prices AS p
    ON p.coin_id = c.coin_id
GROUP BY c.coin_id, c.name
ORDER BY price_points DESC, c.name;

-- Query 2: Find the latest observed price for each coin.
-- "Latest" means latest timestamp present in the downloaded CSV, not live market price.
SELECT
    c.coin_id,
    c.name,
    p.timestamp_utc,
    p.price
FROM top_coins AS c
JOIN coin_prices AS p
    ON p.coin_id = c.coin_id
WHERE p.timestamp_utc = (
    SELECT MAX(p2.timestamp_utc)
    FROM coin_prices AS p2
    WHERE p2.coin_id = c.coin_id
)
ORDER BY c.name;

-- Query 3: Calculate daily average price for each coin.
SELECT
    coin_id,
    date,
    ROUND(AVG(price), 4) AS avg_price
FROM coin_prices
GROUP BY coin_id, date
ORDER BY date DESC, coin_id
LIMIT 30;
