import random
import string
from fastapi import FastAPI
import uvicorn

STRING_DIGITS = string.ascii_letters + string.digits
app = FastAPI()


def generate_random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


@app.get("/info")
async def info() -> dict:
    return {"random_string": (generate_random_string(50))}


if __name__ == "__main__":
    uvicorn.run("upstream_app:app", workers=20, host="0.0.0.0", port=8080, log_level="error")
