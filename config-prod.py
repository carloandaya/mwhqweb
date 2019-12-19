SECRET_KEY = 'dev'
DW_DATABASE = 'DRIVER={SQL Server};SERVER=<server>;DATABASE=MyWirelessDW;Trusted_Connection=yes'
RAW_DATABASE = 'DRIVER={SQL Server};SERVER=<server>;DATABASE=MyWirelessRawData;Trusted_Connection=yes'
OAUTH_CREDENTIALS = {'CLIENT_ID': '<client_id>', 'CLIENT_SECRET': '<client_secret'}
OAUTH_PARAMETERS = {'REDIRECT_URI': 'http://localhost:5000/login/authorized',
                    'AUTHORITY_URL': 'https://login.microsoftonline.com/common',
                    'AUTH_ENDPOINT': '/oauth2/v2.0/authorize',
                    'TOKEN_ENDPOINT': '/oauth2/v2.0/token',
                    'RESOURCE': 'https://graph.microsoft.com/',
                    'API_VERSION': 'v1.0',
                    'SCOPES': ['User.Read', 'Directory.Read.All']}
