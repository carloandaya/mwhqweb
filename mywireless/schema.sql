DROP TABLE IF EXISTS DimProduct;

CREATE TABLE [dbo].[DimProduct](
	[ProductKey] [nvarchar](50) NOT NULL,
	[ManufacturerKey] [int] NOT NULL,
	[CategoryKey] [int] NULL,
	[ProductName] [nvarchar](100) NOT NULL,
	[SubcategoryKey] [int] NULL,
PRIMARY KEY CLUSTERED
(
	[ProductKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

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

DROP TABLE IF EXISTS DimSubcategory;

CREATE TABLE [dbo].[DimSubcategory](
	[SubcategoryKey] [int] IDENTITY(1,1) NOT NULL,
	[SubcategoryName] [nvarchar](50) NOT NULL,
	[CategoryKey] [int] NOT NULL,
PRIMARY KEY CLUSTERED
(
	[SubcategoryKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

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

--Subcategory

ALTER TABLE [dbo].[DimSubcategory]  WITH CHECK ADD  CONSTRAINT [FK_DimSubcategory_DimCategory] FOREIGN KEY([CategoryKey])
REFERENCES [dbo].[DimCategory] ([CategoryKey]);

ALTER TABLE [dbo].[DimSubcategory] CHECK CONSTRAINT [FK_DimSubcategory_DimCategory];

DROP TABLE IF EXISTS DimEmployee;

CREATE TABLE [dbo].[DimEmployee](
	[EmployeeKey] [int] IDENTITY(150000,1) NOT NULL,
	[EmployeeName] [nvarchar](50) NOT NULL,
	[ATTUID] [nvarchar](10) NULL,
	[Email] [nvarchar](50) NULL,
	[IsEmailCreated] [bit] NULL,
	[FirstName] [nvarchar](50) NULL,
	[LastName] [nvarchar](50) NULL,
PRIMARY KEY CLUSTERED
(
	[EmployeeKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE [dbo].[DimEmployee] ADD  DEFAULT ((0)) FOR [IsEmailCreated];


DROP TABLE IF EXISTS DimStore;
DROP TABLE IF EXISTS DimRegion;

CREATE TABLE [dbo].[DimRegion](
	[RegionKey] [int] IDENTITY(1,1) NOT NULL,
	[RegionName] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED
(
	[RegionKey] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY];

CREATE TABLE [dbo].[DimStore](
	[StoreKey] [int] IDENTITY(1,1) NOT NULL,
	[StoreName] [nvarchar](50) NOT NULL,
	[RegionKey] [int] NOT NULL,
	[DealerCode] [nvarchar](10) NULL,
	[RQAbbreviation] [nvarchar](10) NULL,
	[IsActive] [bit] NULL,
PRIMARY KEY CLUSTERED
(
	[StoreKey] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE [dbo].[DimStore] ADD  DEFAULT ((0)) FOR [IsActive];

ALTER TABLE [dbo].[DimStore]  WITH CHECK ADD  CONSTRAINT [FK_DimStore_DimRegion] FOREIGN KEY([RegionKey])
REFERENCES [dbo].[DimRegion] ([RegionKey]);

ALTER TABLE [dbo].[DimStore] CHECK CONSTRAINT [FK_DimStore_DimRegion];

--DimProduct

ALTER TABLE [dbo].[DimProduct] ADD  DEFAULT ((-1)) FOR [ManufacturerKey];

ALTER TABLE [dbo].[DimProduct]  WITH CHECK ADD  CONSTRAINT [FK_DimProduct_DimCategory] FOREIGN KEY([CategoryKey])
REFERENCES [dbo].[DimCategory] ([CategoryKey]);

ALTER TABLE [dbo].[DimProduct] CHECK CONSTRAINT [FK_DimProduct_DimCategory];

ALTER TABLE [dbo].[DimProduct]  WITH CHECK ADD  CONSTRAINT [FK_DimProduct_DimManufacturer] FOREIGN KEY([ManufacturerKey])
REFERENCES [dbo].[DimManufacturer] ([ManufacturerKey]);

ALTER TABLE [dbo].[DimProduct] CHECK CONSTRAINT [FK_DimProduct_DimManufacturer];

ALTER TABLE [dbo].[DimProduct]  WITH CHECK ADD  CONSTRAINT [FK_DimProduct_DimSubcategory] FOREIGN KEY([SubcategoryKey])
REFERENCES [dbo].[DimSubcategory] ([SubcategoryKey]);

ALTER TABLE [dbo].[DimProduct] CHECK CONSTRAINT [FK_DimProduct_DimSubcategory];
