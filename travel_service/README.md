# VisiTour - Travel Agency Hub API

A clean and simple Python + PostgreSQL API for travel agencies and travelers to manage tours, visa applications, and bookings.

---

## ?? Project Structure Explained

```text
visitour/
+-- app/
�   +-- config/
�   �   +-- database.py       # Connects to PostgreSQL using SQLAlchemy
�   +-- models/               # Database tables (defines how data is stored in PostgreSQL)
�   �   +-- user.py           # Users table (travelers and agencies)
�   �   +-- tour.py           # Tours table (tour, price, capacity)
�   �   +-- visa.py           # Visa applications table (country, status)
�   �   +-- booking.py        # Bookings table (traveler_id, tour_id, total_price)
�   +-- schemas/              # Pydantic models (validates incoming & outgoing JSON data)
�   �   +-- user.py
�   �   +-- tour.py
�   �   +-- visa.py
�   �   +-- booking.py
�   +-- repositories/         # Database queries (CRUD operations: Create, Read, Update, Delete)
�   �   +-- base.py
�   �   +-- user.py
�   �   +-- tour.py
�   �   +-- visa.py
�   �   +-- booking.py
�   +-- routes/               # API Endpoints (URL paths that clients call)
�   �   +-- user.py           # /users
�   �   +-- tour.py           # /tours
�   �   +-- visa.py           # /visas
�   �   +-- booking.py        # /bookings
�   +-- main.py               # Starts FastAPI, creates tables, and registers routes
+-- .env                      # Database credentials and settings
+-- .env.example              # Blueprint for environment variables
+-- requirements.txt          # Python dependencies
```

---

## ?? How the 4 Folders Work Together

When a traveler or agency makes an API request:

1. **`routes/` (The Door)**: Receives the HTTP request (e.g. `POST /tours`).
2. **`schemas/` (The Inspector)**: Checks that the sent JSON data has the right fields and types.
3. **`repositories/` (The Worker)**: Performs the actual database query (e.g., `db.add()`, `db.query()`).
4. **`models/` (The Blueprint)**: Represents the PostgreSQL table structure where the data lives.

---

## ?? How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure `.env`
Update your PostgreSQL connection string in `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/visitour
```

### 3. Run the development server
```bash
uvicorn app.main:app --reload
```

### 4. Interactive API Documentation
Open your browser and navigate to:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
