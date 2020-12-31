-- CREATE TABLE stocks(
--     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
--     ticker TEXT NOT NULL,
--     company TEXT NOT NULL,
--     price_change FLOAT NOT NULL,
--     buys INT NOT NULL,
--     sells INT NOT NULL,
--     time DATETIME DEFAULT CURRENT_TIMESTAMP
-- )

-- SELECT ticker, COUNT(*) AS frequency FROM stocks GROUP BY ticker ORDER BY frequency DESC 


-- SELECT ticker, time FROM stocks WHERE time BETWEEN '20-12-24' AND '20-12-27'

SELECT * FROM stocks