-- Subscription Revenue Analytics
-- Analytics Warehouse Schema

IF DB_ID('SRWarehouse') IS NULL
BEGIN
    CREATE DATABASE SRWarehouse;
END;
GO

USE SRWarehouse;
GO