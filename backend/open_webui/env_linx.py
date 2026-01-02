import os

SSO_DB_URL = os.environ.get(
    "SSO_DB_URL", "mysql+pymysql://wansheng:wansheng@192.168.50.201:3306/wansheng"
)
SSO_SQL = os.environ.get(
    "SSO_SQL",
    "SELECT id,user_name,email FROM chatgpt_client where user_type=2 and `status`=1 and expire_time > NOW() and `deleted_at` is NULL and email={email}",
)
