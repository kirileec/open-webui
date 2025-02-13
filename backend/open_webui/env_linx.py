import os

SSO_DB_URL = os.environ.get(
    "SSO_DB_URL", "mysql+pymysql://root:root@10.10.0.16:3306/cool"
)
SSO_SQL = os.environ.get(
    "SSO_SQL",
    "SELECT id,user_name,email FROM chatgpt_client where user_type=2 and `status`=1 and expire_time > NOW() and email={email}",
)
