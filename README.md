## **Finance Tracker Backend (FastAPI)**

A backend system for managing financial records with role-based access control, authentication, and analytics APIs for dashboard insights.

## **Features:**
- Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Roles supported:
    - Admin → Full access
    - Analyst → Read + analytics
    - Viewer → Read-only (restricted scope)

## **Record Management:**
- Create financial records
- View records (with pagination)
- Update records
- Soft delete records
- Search & filter by:
    - Type (income/expense)
    - Category
    - Date range
    - Keywords

## **Dashboard & Analytics:**
- Total income
- Total expenses
- Net balance
- Category-wise summary
- Monthly trends
- Recent activity
- Per-user + overall summaries (for admin/analyst)

## **Security:**
- Password hashing using bcrypt
- JWT token authentication
- Token expiry handling
- Role-based endpoint protection
- Rate limiting (login & register)

## **Additional Features:**
- Soft delete support
- Pagination
- Input validation (Pydantic)
- Clean service-layer architecture

## **Project Structure**
```bash
project-root/
│
├── app/
│   ├── core/
│   │   ├── deps.py
│   │   ├── security.py
│   │   ├── enums.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── routes/
│   ├── database.py
│
├── main.py
├── requirements.txt
```

## **Installation & Setup**
Clone the repository
```bash
git clone <repo-url>
cd project-folder
```
## **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
## **Install dependencies**
```bash
pip install -r requirements.txt
```
## **Set environment variables:**
Create a .env file:

```bash
SECRET_KEY=your_secret_key_here
```
**Run the server:**
```bash
uvicorn main:app --reload
```

## **Access API docs**
- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc →   http://127.0.0.1:8000/redoc

## **Authentication Flow:**
- Register user → /register
- Login → /login
- Get JWT token
- Use token in Swagger

## **API Endpoints :**

## **Auth**
- POST /register → Register user
- POST /login → Login & get token
## **Records**
- POST /records/ → Create record
- GET /records/ → Get records
- PUT /records/{id} → Update record
- DELETE /records/{id} → Delete record
- GET /records/search → Filter/search records
## **Dashboard**
- GET /dashboard/summary?scope=self|all
## **Analytics**
- GET /records/category-summary?scope=self|all
- GET /records/monthly
- GET /records/recent
## **Users (Admin)**
- GET /users/ → Get all users
- DELETE /users/by-username/{username}
- PUT /users/activate/{username}
- PUT /users/deactivate/{username}
- GET /users/me

## **Access Control Rules:**
| Role    | Permissions                         |
| ------- | ----------------------------------- |
| Admin   | Full access                         |
| Analyst | Read + analytics                    |
| Viewer  | Read-only (no create/update/delete) |

## **Example Dashboard Response:**
```bash
{
  "scope": "all",
  "users": {
    "user1": {
      "income": 50000,
      "expense": 20000,
      "balance": 30000
    }
  },
  "overall": {
    "income": 80000,
    "expense": 30000,
    "balance": 50000
  }
}
```

## **Error Handling:**
- 400 → Bad request
- 401 → Unauthorized
- 403 → Forbidden
- 404 → Not found
- 429 → Rate limit exceeded

## **Design Highlights:**
- Clean separation:
- Routes → Services → DB
- Role-based access using dependencies
- Enum-based validation
- Secure JWT handling
- Scalable and maintainable structure

## **Future Improvements:**
- Unit & integration tests
- Refresh tokens
- Logging & monitoring
- Docker deployment
- PostgreSQL integration