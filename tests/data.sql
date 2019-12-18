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
