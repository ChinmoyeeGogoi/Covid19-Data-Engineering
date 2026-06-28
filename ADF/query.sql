-- Top 10 countries by total cases
SELECT TOP 10 location, total_cases, total_deaths, total_vaccinations
FROM covid_summary
ORDER BY total_cases DESC;

-- Basic data quality check
SELECT COUNT(*) as total_rows,
       SUM(CASE WHEN total_cases = 0 THEN 1 ELSE 0 END) as zero_case_rows
FROM covid_summary;