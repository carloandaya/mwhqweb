DROP TABLE IF EXISTS DimManufacturer;

CREATE TABLE [dbo].[DimManufacturer](
	[ManufacturerKey] [int] IDENTITY(1,1) NOT NULL,
	[ManufacturerName] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED
(
	[ManufacturerKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE UNIQUE NONCLUSTERED INDEX [IX_DimManufacturer_ManufacturerName] ON [dbo].[DimManufacturer]
(
	[ManufacturerName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];

DROP TABLE IF EXISTS DimCategory;

CREATE TABLE [dbo].[DimCategory](
	[CategoryKey] [int] IDENTITY(1,1) NOT NULL,
	[CategoryName] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED
(
	[CategoryKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE UNIQUE NONCLUSTERED INDEX [IX_DimCategory_CategoryName] ON [dbo].[DimCategory]
(
	[CategoryName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];

DROP TABLE IF EXISTS DimEmployee;

CREATE TABLE [dbo].[DimEmployee](
	[EmployeeKey] [int] IDENTITY(200000,1) NOT NULL,
	[EmployeeName] [nvarchar](50) NOT NULL,
	[ATTUID] [nvarchar](10) NULL,
PRIMARY KEY CLUSTERED
(
	[EmployeeKey] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY];
