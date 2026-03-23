# AI-Driven HR, L&D & Talent Intelligence

> Intelligent talent management platform with automated skill extraction, certification mapping, and personalized learning recommendations.

## 🎯 Features

1. **CV Skill Extraction** - Upload CV and automatically extract technical skills
2. **Certification Sync** - Map certifications to skill profiles automatically
3. **Personalized Learning Paths** - Generate customized upskilling journeys with curated resources
4. **Employee Search** - Find employees by name with rich profile views
5. **Visual Skill Tracking** - Interactive skill meters with proficiency levels

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python 3.11)
- SQLAlchemy ORM
- SQLite database
- Pydantic validation

**Frontend:**
- React 18
- Vite build tool
- Modern CSS with responsive design
- Toast notifications

**Infrastructure:**
- Docker & Docker Compose
- Multi-stage builds
- Nginx for frontend serving

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git

### Run with Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-hr-talent-intelligence

# Start all services
docker compose up --build
```

**Access:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### Run Locally (Development)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

### Core Endpoints
- `GET /health` - Health check
- `GET /employees/{id}` - Get employee profile
- `GET /employees/search?name={name}` - Search employees by name
- `POST /employees/{id}/cv/upload` - Upload CV for skill extraction
- `POST /employees/{id}/certifications` - Add certification
- `POST /employees/{id}/recommendations` - Generate learning path

### Utility Endpoints
- `GET /certifications/available` - List all certifications
- `GET /employees/skills/suggestions` - Get skill suggestions

## 🎮 Demo Flow

1. **Open Frontend**: Navigate to `http://localhost:3000`
2. **Search Employee**: Search for "Ava" or "John"
3. **Upload CV**: Paste text like "Python AWS Docker Kubernetes" and process
4. **Add Certification**: Select "AWS Certified Solutions Architect Associate"
5. **Generate Learning Path**: Enter "kubernetes" with 6-week timeline

## 📊 Sample Data

The system comes pre-seeded with:
- **10 diverse employees** across different roles and geographies
- **7 certifications** (AWS, Azure, GCP, Kubernetes)
- **15+ learning resources** covering cloud, DevOps, AI, and more
- **24 skills** mapped across categories

## 📁 Project Structure

```
ai-hr-talent-intelligence/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # API endpoints
│   │   ├── db/              # Database models & seed
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── main.jsx         # Entry point
│   │   └── styles.css       # Styling
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🔧 Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

## 🧪 Testing

```bash
# Health check
curl http://localhost:8000/health

# Get employee
curl http://localhost:8000/employees/1

# Search employees
curl "http://localhost:8000/employees/search?name=Ava"
```

## 📦 Submission Package

For evaluation submission:

```bash
# Create ZIP with proper structure
cd ..
zip -r ai-hr-talent-intelligence.zip ai-hr-talent-intelligence/
```

Ensure:
- ✅ Single top-level folder
- ✅ `docker-compose.yml` at root
- ✅ `/health` endpoint returns 200
- ✅ All endpoints implemented

## 🚧 Future Enhancements

- [ ] PostgreSQL for production
- [ ] Authentication & authorization
- [ ] Async CV parsing with AI models
- [ ] Advanced skill taxonomy
- [ ] Role-based analytics dashboard
- [ ] Team skill gap analysis
- [ ] Integration with LMS platforms

## 📄 License

MIT License

## 👥 Contributors

Built for AI-driven HR transformation.
