from fastapi import APIRouter

router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)


@router.get("/test")
async def github_test():

    return {
        "message": "GitHub API route working"
    }