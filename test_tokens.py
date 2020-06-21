from config import TestingConfig
from app.auth.auth_token import create_auth_header_with_permissions

if __name__ == '__main__':
    auth_header_with_all_permissions = create_auth_header_with_permissions(
        domain=TestingConfig.AUTH0_DOMAIN,
        api_audience=TestingConfig.API_AUDIENCE,
        client_id=TestingConfig.CLIENT_ID,
        client_secret=TestingConfig.CLIENT_SECRET
    )
    print(
        'authorization header with all permissions: ',
        auth_header_with_all_permissions,
        '\n'
    )

    auth_header_with_reviewer_permissions = (
        create_auth_header_with_permissions(
            domain=TestingConfig.AUTH0_DOMAIN,
            api_audience=TestingConfig.API_AUDIENCE,
            client_id=TestingConfig.REVIEWER_CLIENT_ID,
            client_secret=TestingConfig.REVIEWER_CLIENT_SECRET
        )
    )

    print(
        'authorization header with reviewer permissions: ',
        auth_header_with_reviewer_permissions,
        '\n'
    )

    auth_header_with_author_permissions = create_auth_header_with_permissions(
        domain=TestingConfig.AUTH0_DOMAIN,
        api_audience=TestingConfig.API_AUDIENCE,
        client_id=TestingConfig.AUTHOR_CLIENT_ID,
        client_secret=TestingConfig.AUTHOR_CLIENT_SECRET
    )

    print(
        'authorization header with author permissions: ',
        auth_header_with_author_permissions,
        '\n'
    )

    auth_header_with_codereviewme_admin_permissions = (
        create_auth_header_with_permissions(
            domain=TestingConfig.AUTH0_DOMAIN,
            api_audience=TestingConfig.API_AUDIENCE,
            client_id=TestingConfig.CODEREVIEWME_ADMIN_CLIENT_ID,
            client_secret=TestingConfig.CODEREVIEWME_ADMIN_CLIENT_SECRET
        )
    )

    print(
        'authorization header with codereview admin permissions: ',
        auth_header_with_codereviewme_admin_permissions,
        '\n'
    )
