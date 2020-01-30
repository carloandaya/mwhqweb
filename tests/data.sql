INSERT INTO DimCategory(CategoryName)
VALUES
('Accessory'),
('Phone');

INSERT INTO DimManufacturer(ManufacturerName)
VALUES
('Apple'),
('Samsung'),
('LG Electronics');

SET IDENTITY_INSERT DimEmployee ON;
INSERT INTO DimEmployee(EmployeeKey, EmployeeName, ATTUID)
VALUES
('101098', 'Carlo Andaya', 'ca941g');
SET IDENTITY_INSERT DimEmployee OFF;

SET IDENTITY_INSERT DimRegion ON;
INSERT INTO DimRegion(RegionKey, RegionName)
VALUES (2, 'CAGLA Market')
SET IDENTITY_INSERT DimRegion OFF;

INSERT INTO DimStore(StoreName, RegionKey, DealerCode, RQAbbreviation, IsActive)
VALUES
('AT&T - Azusa', 2, 'XIL3Y', 'AZUSA', 1)
