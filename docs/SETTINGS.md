|             Setting            |         Default        |      Env. variable     |                      Description                     |
|:------------------------------:|:----------------------:|:----------------------:|:----------------------------------------------------:|
|       DEFAULT_CATEGORIES       |       See config.      |                        |                Default link categories               |
|        DEFAULT_CATEGORY        |         'Other'        |                        |     Category for link creation when not specified    |
|         ITEMS_PER_PAGE         |           10           |                        |             Max. displayed links per page            |
|        ATOM_LINKS_COUNT        |           50           |                        |              Max. links included in feed             |
|         DATETIME_FORMAT        | '%b %d %Y at %H:%M:%S' |                        |                  Date display format                 |
|              DEBUG             |          False         |       FLASK_DEBUG      |                   Enable debug mode                  |
|             TESTING            |          False         |      FLASK_TESTING     |                  Enable testing mode                 |
|           SECRET_KEY           |       'CHANGEME'       |    FLASK_SECRET_KEY    |       Secret key for session cookies encryption      |
|         REVERSE_PROXIED        |          False         |     REVERSE_PROXIED    | Enable if served in subfolder behind a reverse proxy |
|       SECURITY_URL_PREFIX      |         '/user'        |                        |                Sub-path for user views               |
|     SECURITY_PASSWORD_HASH     |     'pbkdf2_sha512'    |                        |         Hash algorithm for passwords storage         |
|     SECURITY_PASSWORD_SALT     |       'CHANGEME'       | SECURITY_PASSWORD_SALT |               Salt for password hashing              |
| SECURITY_AUTHENTICATION_HEADER |         'Auth'         |                        |          Header where API token is expected          |
|      SECURITY_RECOVERABLE      |          True          |  SECURITY_RECOVERABLE  |         Enable self-service password recovery        |
|        DATABASE['name']        |        'waikup'        |      DATABASE_NAME     |                     Database name                    |
|        DATABASE['user']        |        'waikup'        |      DATABASE_USER     |          User to use to connect to database          |
|      DATABASE['password']      |        'waikup'        |    DATABASE_PASSWORD   |        Password to use to connect to database        |
|        DATABASE['host']        |       '127.0.0.1'      |      DATABASE_HOST     |            Database server hostname or IP            |
|        DATABASE['port']        |          5432          |      DATABASE_PORT     |                 Database server port                 |
|       DATABASE['engine']       |       See config.      |                        |                 Database engine class                |
|           MAIL_SERVER          |       '127.0.0.1'      |       MAIL_SERVER      |              SMTP server hostname or IP              |
|            MAIL_PORT           |           25           |        MAIL_PORT       |                   SMTP server port                   |
|          MAIL_USE_TLS          |          False         |      MAIL_USE_TLS      |           Use TLS to connect to SMTP server          |
|          MAIL_USE_SSL          |          False         |      MAIL_USE_SSL      |           Use SSL to connect to SMTP server          |
|          MAIL_USERNAME         |        'waikup'        |      MAIL_USERNAME     |         User to use to connect to SMTP server        |
|          MAIL_PASSWORD         |        'waikup'        |      MAIL_PASSWORD     |       Password to use to connect to SMTP server      |
|       MAIL_DEFAULT_SENDER      |  'waikup@example.com'  |   MAIL_DEFAULT_SENDER  |       Sender address to use when sending emails      |
