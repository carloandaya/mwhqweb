INSERT INTO DimCategory(CategoryName)
VALUES
('Accessory'),
('Phone');

INSERT INTO DimSubcategory(SubcategoryName, CategoryKey)
VALUES
('Postpaid', 2),
('Prepaid', 2),
('Case', 1),
('Screen Protector', 1),
('Power', 1),
('Cable', 1);

SET IDENTITY_INSERT DimManufacturer ON;
INSERT INTO DimManufacturer(ManufacturerKey, ManufacturerName)
VALUES
(-1, 'N/A'),
(1, 'Apple'),
(2, 'Samsung'),
(3, 'LG Electronics');
SET IDENTITY_INSERT DimManufacturer OFF;

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
('AT&T - Azusa', 2, 'XIL3Y', 'AZUSA', 1);

INSERT INTO DimProduct(ProductKey, ManufacturerKey, CategoryKey, ProductName, SubcategoryKey)
VALUES
('AEDEPB000159', 1,	2, 'Apple iPhone 11 Pro Max 512GB Midnight Green', 1),
('AEINPB000022', 1,	2, 'Apple iPhone 7 32GB Black',	1),
('AEINPB000023', -1, 2, 'Apple iPhone 7 32GB Silver', 1);

