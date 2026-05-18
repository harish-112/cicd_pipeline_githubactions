from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Python CI/CD Pipeline Running Successfully!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
