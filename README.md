# DriftDater 

A date matching web application built with Vue 3 and Flask that allows registered users to create detailed profiles, discover compatible matches, and initiate connections with other users.


## Group Members
Tramonique Wellington - Project Manager and Integration Support (Backend)| 
Romaine Dixon - Backend Lead|
Britnie-Ann Gray - Frontend Lead|
Amanda Miller - QA / Testing Lead|
Donjae Marsh - Deployment Lead (Assist Frontend)|

## Setup Instructions

### Prerequisites
- Python 3.x
- Node.js and npm
- PostgreSQL

### Backend Setup

1. Clone the repository
    ```bash
    git clone -b dev https://github.com/Tramonique/info3180-driftdater.git
    cd info3180-driftdater
    ```

2. Create and activate a virtual environment
    ```bash
    python -m venv venv
    .\venv\Scripts\activate        # Windows
    source venv/bin/activate       # Mac/Linux
    ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables
    ```bash
    copy .env.sample .env          # Windows
    cp .env.sample .env            # Mac/Linux
    ```

    Fill in your local values in `.env`:
    ```
    FLASK_DEBUG=True
    FLASK_RUN_HOST=0.0.0.0
    FLASK_RUN_PORT=5000
    SECRET_KEY=your_secret_key
    DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/driftdater
    ```

5. Create the PostgreSQL database

    Create a database called `driftdater` in PostgreSQL, then run migrations:
    ```bash
    flask db upgrade
    ```

6. Start the backend
    ```bash
    flask --app app --debug run
    ```
    Backend runs at: http://localhost:5000

## Frontend Setup 

7. Open a new terminal and install frontend dependencies
    ```bash
    npm install
    ```

8. Start the frontend
    ```bash
    npm run dev
    ```
    Frontend runs at: http://localhost:5173 



## API DOCUMENTATION 

Base URL: `http://localhost:5000`

### Authentication

#### Register
- **POST** `/api/register`
- **Body:** `{ "email": "user@example.com", "password": "password123" }`
- **Success:** `201` – User registered successfully
- **Errors:** `400` bad request, `409` email already exists

#### Login
- **POST** `/api/login`
- **Body:** `{ "email": "user@example.com", "password": "password123" }`
- **Success:** `200` – Login successful + user object
- **Errors:** `400` bad request, `401` invalid credentials

#### Logout
- **POST** `/api/logout`
- **Success:** `200` – Logout successful

#### Check Auth
- **GET** `/api/check-auth`
- **Success:** `200` – `{ "authenticated": true/false }`

---

### Profiles

#### Create Profile
- **POST** `/api/profiles`
- **Auth required:** Yes
- **Body:**
    ```json
    {
        "full_name": "John Doe",
        "age": 25,
        "bio": "About me...",
        "location": "Kingston, Jamaica",
        "interests": "music, travel, food",
        "visibility": "public",
        "preferred_age_min": 20,
        "preferred_age_max": 30,
        "preferred_location": "Kingston",
        "custom_field_1": "value",
        "custom_field_2": "value"
    }
    ```
- **Success:** `201` – Profile created successfully
- **Errors:** `400` missing fields, `401` unauthorized, `409` profile already exists

#### Get Profile
- **GET** `/api/profiles/<user_id>`
- **Auth required:** Yes
- **Success:** `200` – Profile JSON object
- **Errors:** `401` unauthorized, `403` private profile, `404` not found

#### Edit Profile
- **PUT** `/api/profiles/<user_id>`
- **Auth required:** Yes (own profile only)
- **Body:** Any profile fields to update
- **Success:** `200` – Profile updated successfully
- **Errors:** `401` unauthorized, `403` forbidden, `404` not found

#### Upload Profile Photo
- **POST** `/api/profiles/<user_id>/photo`
- **Auth required:** Yes (own profile only)
- **Body:** `form-data` with key `photo` and image file (png, jpg, jpeg, gif)
- **Success:** `200` – Photo uploaded successfully + filename
- **Errors:** `400` no file/invalid type, `401` unauthorized, `403` forbidden

---

### Matching

#### Discover Users
- **GET** `/api/discover`
- **Auth required:** Yes
- **Success:** `200` – List of profiles sorted by match score
- **Errors:** `400` no profile, `401` unauthorized

#### Like a User
- **POST** `/api/profiles/<user_id>/like`
- **Auth required:** Yes
- **Success:** `200` – `{ "matched": true/false }`
- **Errors:** `400` can't like yourself, `401` unauthorized, `404` user not found, `409` already interacted

#### Pass a User
- **POST** `/api/profiles/<user_id>/pass`
- **Auth required:** Yes
- **Success:** `200` – Passed
- **Errors:** `400` invalid, `401` unauthorized, `409` already interacted

#### Get Matches
- **GET** `/api/matches`
- **Auth required:** Yes
- **Success:** `200` – List of matched users
- **Errors:** `401` unauthorized

---

### Messages

#### Send Message
- **POST** `/api/messages`
- **Auth required:** Yes (must be matched with receiver)
- **Body:** `{ "receiver_id": 2, "content": "Hello!" }`
- **Success:** `201` – Message sent + message_id
- **Errors:** `400` missing fields, `401` unauthorized, `403` not matched

#### Get Messages
- **GET** `/api/matches/<match_id>/messages`
- **Auth required:** Yes (must be part of match)
- **Success:** `200` – List of messages with timestamps
- **Errors:** `401` unauthorized, `403` not in match, `404` match not found

---

### Search

#### Search Profiles
- **GET** `/api/search`
- **Auth required:** Yes
- **Query Parameters:**
    - `location` – filter by location (partial match)
    - `age_min` – minimum age
    - `age_max` – maximum age
    - `interests` – filter by interests (partial match)
- **Example:** `/api/search?location=Kingston&age_min=18&age_max=30&interests=music`
- **Success:** `200` – List of matching profiles
- **Errors:** `401` unauthorized

---

## Known Issues / Limitations

- Messaging is only available between mutually matched users
- Profile pictures are stored locally and will not persist on redeployment without cloud storage
- No real-time messaging (page refresh required to see new messages)

---

## Deployed Application

- **App URL:** [Add Render URL here]
- **GitHub Repository:** https://github.com/Tramonique/info3180-driftdater
