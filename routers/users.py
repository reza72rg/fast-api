from fastapi import APIRouter

router = APIRouter(
    # prefix = "/users"
         )

@router.post("/register")
async def register():
    pass

@router.post("/login")
async def login():
    pass

@router.get("/")
async def get_user_profile():
    pass

@router.put("/")
async def user_update_profile():
    pass
