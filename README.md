# Social Networking API

## Installation Steps

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies using `pip install -r requirements.txt`
4. Run migrations using `python manage.py migrate`
5. Run the server using `python manage.py runserver`

## Docker Setup

1. Build and run the containers using `docker-compose up --build`

## API Endpoints

- **User Signup:** `/api/signup/` (POST)
- **User Login:** `/api/login/` (POST)
- **User Search:** `/api/users/` (GET)
- **Send Friend Request:** `/api/friend-request/` (POST)
- **Accept/Reject Friend Request:** `/api/friend-request/<id>/` (PUT)
- **List Friends:** `/api/friends/` (GET)
- **List Pending Friend Requests:** `/api/pending-requests/` (GET)
