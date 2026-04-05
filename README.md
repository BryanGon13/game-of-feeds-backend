# Game of Feeds – Backend API

[**Live API URL**](https://your-api-name.herokuapp.com)

---

## Project Documentation

The full project documentation, including design rationale, frontend features, wireframes, and user interface implementation, is available in the frontend repository:

👉 https://github.com/BryanGon13/game-of-feeds-frontend

This repository focuses exclusively on the backend API, including data models, serializers, views, permissions, and database structure.

---

## Overview

The Game of Feeds backend is a Django REST Framework API that supports a social media application inspired by Game of Thrones.

It provides all server-side functionality required for the frontend application, including authentication, CRUD operations, and relational data handling between users, posts, comments, and interactions.

---

## Core Features

- User authentication (registration and login)  
- Full CRUD functionality for posts, comments, and profiles  
- Like and unlike system  
- Follow and unfollow users  
- Profile management (bio, image, house selection)  
- Custom House model for user identity  
- Secure API endpoints with permission control  

---

## Custom Feature: House Model

A custom `House` model was implemented to extend the functionality beyond the course walkthrough project.

- Profiles are linked to a House via a ForeignKey relationship  
- Houses are retrieved via the `/houses/` endpoint  
- A safe multi-step migration was used to convert legacy data  
- Profiles can update their house through API requests  

This demonstrates custom model design and integration with frontend functionality.

---

## Database Structure

The backend uses a relational database with the following key models:

- **Profile** – Extends Django User model and stores additional user data  
- **Post** – Stores image-based user content  
- **Comment** – Linked to both posts and profiles  
- **Like** – Tracks user engagement with posts  
- **Follower** – Manages relationships between profiles  
- **House** – Custom model linked to Profile via ForeignKey  

This structure ensures scalable and efficient handling of social interactions.

---

## Technologies Used

- Python  
- Django  
- Django REST Framework  
- PostgreSQL (production)  
- SQLite (development)  
- Cloudinary (media storage)  
- Gunicorn (deployment)  

---

## Deployment

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/BryanGon13/game-of-feeds-backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
SECRET_KEY=<your-secret-key>
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_URL=<your-cloudinary-url>
DEBUG=True
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the server:
```bash
python manage.py runserver
```

---

### Heroku Deployment

1. Create the Heroku app:
```bash
heroku create your-api-name
```

2. Add Heroku Postgres:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

3. Set environment variables in Heroku:
```env
SECRET_KEY=<your-secret-key>
DATABASE_URL=<provided by Heroku>
CLOUDINARY_URL=<your-cloudinary-url>
DEBUG=False
ALLOWED_HOSTS=your-api-name.herokuapp.com
CLIENT_ORIGIN=https://your-frontend-name.herokuapp.com
```

4. Deploy:
```bash
git push heroku main
```

5. Run migrations:
```bash
heroku run python manage.py migrate
```

---

## Testing

### Backend Manual Testing

The backend API was tested using the Django REST Framework browsable API and through frontend integration.

| Endpoint / Feature | Test Performed | Expected Result | Result |
|--------------------|----------------|-----------------|--------|
| `/posts/` | Create post | Post saved correctly | Pass |
| `/posts/<id>/` | Edit post | Data updated | Pass |
| `/posts/<id>/` | Delete post | Post removed | Pass |
| `/comments/` | Create comment | Linked correctly | Pass |
| `/comments/<id>/` | Edit comment | Updated correctly | Pass |
| `/comments/<id>/` | Delete comment | Removed successfully | Pass |
| `/likes/` | Like post | Record created | Pass |
| `/likes/<id>/` | Unlike post | Record deleted | Pass |
| `/followers/` | Follow user | Relationship created | Pass |
| `/followers/<id>/` | Unfollow user | Relationship removed | Pass |
| `/profiles/<id>/` | Update bio | Bio updated correctly | Pass |
| `/profiles/<id>/` | Update image | Image uploaded to Cloudinary | Pass |
| `/profiles/<id>/` | Update house | Relationship saved | Pass |
| `/houses/` | Retrieve houses | List returned correctly | Pass |
| Authentication | Register user | User created successfully | Pass |
| Authentication | Login | Tokens returned | Pass |
| Permissions | Unauthorized edit | Access denied | Pass |

---

### Validation & Permissions Testing

- Serializer validation prevents invalid or empty submissions  
- Only authenticated users can create content  
- Only owners can edit or delete their own content  
- Profile updates are restricted to the profile owner  
- ForeignKey relationships validated at database level  

---

## Security Features

- Environment variables used to protect sensitive data  
- Token-based authentication system  
- Permission classes restrict access to resources  
- Debug mode disabled in production  

---

## Known Issues

No major backend issues currently identified.

---

## Credits & Acknowledgements

- Code Institute  
- Django REST Framework Documentation  
- Cloudinary Documentation  