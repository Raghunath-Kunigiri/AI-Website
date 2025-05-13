AI Website
AI Website is a web application for browsing and managing a directory of AI tools and resources. It features a responsive frontend for viewing sources and an admin panel for adding and editing sources, powered by a FastAPI backend with MongoDB Atlas storage and styled with Tailwind CSS.
How to Run

Clone the Repository:
git clone https://github.com/Raghunath-Kunigiri/AI-Website.git
cd AI-Website


Set Up Python Environment:
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
pip install python-dotenv


Configure MongoDB:

Create a .env file:MONGO_URI=mongodb+srv://<your-username>:<your-password>@<your-cluster>.mongodb.net/?retryWrites=true&w=majority


Update main.py and insert_sources.py:from dotenv import load_dotenv
import os
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")




Populate Sample Data:
python insert_sources.py


Install Node.js Dependencies:
npm install


Generate Tailwind CSS:
npm run build


Run the Backend:
python main.py


Run the Frontend:
npx http-server .


Access the Application:

Main page: http://127.0.0.1:8080
Admin panel: http://127.0.0.1:8080/admin.html



