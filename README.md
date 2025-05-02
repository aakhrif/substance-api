// README.md
# Substance Database API

API for managing chemical substances and their physical properties.

## 🧪 Development Environment

### 🐳 Using Docker Compose (recommended):
```bash
docker-compose up --build
```
Then run the Prisma migration:
```bash
docker-compose exec api npx prisma migrate dev --name init
```

### 🧑‍💻 Alternatively (local setup):
```bash
chmod +x setup.sh
./setup.sh
```
Or manually:
```bash
npm install
npx prisma generate
npx prisma migrate dev --name init
npm run dev
```

## 📚 API Documentation
Once running, the API documentation is available at: [http://localhost:3000/docs](http://localhost:3000/docs)

## 📦 Technologies
- Node.js + TypeScript
- Fastify + Swagger
- Prisma + PostgreSQL
- Docker Compose

## 📂 Project Structure (excerpt)
```
├── server.ts
├── routes/
├── prisma/
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── .env (excluded from version control)
```