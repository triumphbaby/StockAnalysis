-- Database Initialization Script for Stock Analysis Platform
-- This script creates the initial database schema

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS public;

-- Set search path
SET search_path TO public;

-- Comments
COMMENT ON SCHEMA public IS 'Stock Analysis Platform - Main Schema';

-- Create initial tables (basic structure)
-- More tables will be created via SQLAlchemy models

-- Example: Create a simple health check table
CREATE TABLE IF NOT EXISTS system_health (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message TEXT
);

COMMENT ON TABLE system_health IS 'System health check records';

-- Insert initial health check record
INSERT INTO system_health (service_name, status, message)
VALUES ('database', 'healthy', 'Database initialized successfully')
ON CONFLICT DO NOTHING;

-- Grant permissions (if needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO stockuser;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO stockuser;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Stock Analysis Platform database initialized successfully';
END $$;
