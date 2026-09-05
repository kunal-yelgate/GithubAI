from itsdangerous import URLSafeSerializer
from app.config import GITHUB_CLIENT_SECRET


serializer = URLSafeSerializer(
    GITHUB_CLIENT_SECRET,
    salt="github-ai-analyzer-session"
)


def create_session(access_token: str):

    return serializer.dumps({
        "access_token": access_token
    })


def read_session(session: str):

    return serializer.loads(session)








# Instead, after getting the token, the backend should use it to obtain the user's GitHub information and create a session.

# For the first implementation, we can use a signed session cookie.