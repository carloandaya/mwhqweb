DROP TABLE IF EXISTS ATT_ShipmentDetailReport;

CREATE TABLE [dbo].[ATT_ShipmentDetailReport](
	[Region] [nvarchar](50) NULL,
	[Market] [nvarchar](50) NULL,
	[InvoiceNumber] [nvarchar](50) NOT NULL,
	[OrderNumber] [nvarchar](50) NULL,
	[PONumber] [nvarchar](50) NOT NULL,
	[ActualShipDate] [date] NOT NULL,
	[ItemNumber] [nvarchar](20) NOT NULL,
	[ItemDescription] [nvarchar](50) NULL,
	[ItemCategory] [nvarchar](20) NULL,
	[UnitPrice] [money] NULL,
	[ExtdPrice] [money] NULL,
	[QuantityOrdered] [int] NULL,
	[QuantityShipped] [int] NULL,
	[IMEI] [nvarchar](50) NOT NULL,
	[TrackingNumber] [nvarchar](50) NULL,
	[IsReceived] [bit] NULL DEFAULT (0),
	[DeliveryStatus] [nvarchar](3) NULL,
	[StatusDate] [date] NULL,
	[PickupDate] [date] NULL,
	[ScheduledDeliveryDate] [date] NULL,
	[SignedBy] [nvarchar](50) NULL,
PRIMARY KEY CLUSTERED
(
	[InvoiceNumber] ASC,
	[PONumber] ASC,
	[ActualShipDate] ASC,
	[ItemNumber] ASC,
	[IMEI] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY];
