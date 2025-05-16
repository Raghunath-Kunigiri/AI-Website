from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aisources-front.onrender.com"],  # Update with frontend URL after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://harshithathota2000:ERuvTNydZF4E6Os7@clusterrk.fgfpg5w.mongodb.net/?retryWrites=true&w=majority&appName=ClusterRK")
client = MongoClient(MONGO_URI)
db = client["ai_sources_db"]
collection = db["sources"]

# Pydantic models
class AISource(BaseModel):
    name: str
    category: str
    url: str
    description: str
    tags: Optional[str] = ""
    featured: Optional[bool] = False

class AISourceInDB(AISource):
    id: str

# Convert MongoDB document to dict
def source_to_dict(source):
    return {
        "id": str(source["_id"]),
        "name": source["name"],
        "category": source["category"],
        "url": source["url"],
        "description": source["description"],
        "tags": source["tags"],
        "featured": source["featured"]
    }

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to AI Sources API. Visit /api/sources to view resources."}

# Existing endpoints
@app.get("/api/sources", response_model=List[AISourceInDB])
async def get_sources():
    sources = collection.find()
    return [source_to_dict(source) for source in sources]

@app.get("/api/sources/{source_id}", response_model=AISourceInDB)
async def get_source(source_id: str):
    try:
        source = collection.find_one({"_id": ObjectId(source_id)})
        if source:
            return source_to_dict(source)
        raise HTTPException(status_code=404, detail="Source not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid source ID")

@app.post("/api/sources", response_model=AISourceInDB)
async def create_source(source: AISource):
    source_dict = source.dict()
    result = collection.insert_one(source_dict)
    source_dict["_id"] = result.inserted_id
    return source_to_dict(source_dict)

@app.put("/api/sources/{source_id}", response_model=AISourceInDB)
async def update_source(source_id: str, source: AISource):
    try:
        source_dict = source.dict()
        result = collection.update_one(
            {"_id": ObjectId(source_id)},
            {"$set": source_dict}
        )
        if result.matched_count:
            source_dict["_id"] = ObjectId(source_id)
            return source_to_dict(source_dict)
        raise HTTPException(status_code=404, detail="Source not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid source ID")

@app.delete("/api/sources/{source_id}")
async def delete_source(source_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(source_id)})
        if result.deleted_count:
            return {"message": "Source deleted successfully"}
        raise HTTPException(status_code=404, detail="Source not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid source ID")

@app.get("/api/stats")
async def get_stats():
    total_sources = collection.count_documents({})
    categories = len(collection.distinct("category"))
    featured = collection.count_documents({"featured": True})
    return {
        "totalSources": total_sources,
        "totalCategories": categories,
        "featuredSources": featured
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))