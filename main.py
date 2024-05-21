from dotenv import load_dotenv
import uvicorn

load_dotenv()

if __name__=="__main__":
    uvicorn.run('api.app:app')