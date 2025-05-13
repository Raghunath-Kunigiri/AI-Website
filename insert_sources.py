from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection details
MONGO_URI = "mongodb+srv://harshithathota2000:ERuvTNydZF4E6Os7@clusterrk.fgfpg5w.mongodb.net/?retryWrites=true&w=majority&appName=ClusterRK"
DB_NAME = "ai_sources_db"
COLLECTION_NAME = "sources"

# Sample data from your initial code
ai_sources = [
    {
        "id": 1,
        "name": "OpenAI GPT-4",
        "category": "Text Generation",
        "url": "https://openai.com/gpt-4",
        "description": "The latest language model from OpenAI with improved capabilities in understanding and generating natural language.",
        "tags": "chatbot,writing,assistant",
        "featured": True
    },
    {
        "id": 2,
        "name": "Stable Diffusion",
        "category": "Image Generation",
        "url": "https://stablediffusionweb.com",
        "description": "Open source text-to-image model that can generate detailed images from text descriptions.",
        "tags": "art,design,creative",
        "featured": True
    },
    {
        "id": 3,
        "name": "GitHub Copilot",
        "category": "Code Assistance",
        "url": "https://github.com/features/copilot",
        "description": "AI pair programmer that helps you write code faster and with less work.",
        "tags": "programming,developer,productivity",
        "featured": True
    },
    {
        "id": 4,
        "name": "ElevenLabs",
        "category": "Voice Synthesis",
        "url": "https://elevenlabs.io",
        "description": "AI voice generator that produces natural sounding speech in any voice and style.",
        "tags": "audio,podcast,voiceover",
        "featured": False
    },
    {
        "id": 5,
        "name": "Runway ML",
        "category": "Video Generation",
        "url": "https://runwayml.com",
        "description": "Creative toolkit that makes content creation and editing accessible to everyone.",
        "tags": "video,editing,effects",
        "featured": False
    },
    {
        "id": 6,
        "name": "Anthropic Claude",
        "category": "Text Generation",
        "url": "https://www.anthropic.com",
        "description": "Next-generation AI assistant focused on being helpful, harmless, and honest.",
        "tags": "chatbot,research,assistant",
        "featured": False
    }
]

def connect_to_mongodb():
    """Connect to MongoDB and return the collection object."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        logger.info("Successfully connected to MongoDB")
        return collection
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def insert_sources(collection):
    """Insert AI sources into MongoDB, avoiding duplicates based on 'id'."""
    inserted_count = 0
    skipped_count = 0

    for source in ai_sources:
        try:
            # Check if a source with the same 'id' already exists
            existing_source = collection.find_one({"id": source["id"]})
            if existing_source:
                logger.info(f"Skipping source with id {source['id']} (already exists)")
                skipped_count += 1
                continue

            # Insert the source
            collection.insert_one(source)
            logger.info(f"Inserted source: {source['name']}")
            inserted_count += 1
        except DuplicateKeyError:
            logger.warning(f"Duplicate key error for source: {source['name']}")
            skipped_count += 1
        except Exception as e:
            logger.error(f"Error inserting source {source['name']}: {e}")
            continue

    return inserted_count, skipped_count

def main():
    """Main function to execute the insertion process."""
    try:
        collection = connect_to_mongodb()
        inserted, skipped = insert_sources(collection)
        logger.info(f"Insertion complete: {inserted} sources inserted, {skipped} sources skipped")
    except Exception as e:
        logger.error(f"Script execution failed: {e}")

if __name__ == "__main__":
    main()