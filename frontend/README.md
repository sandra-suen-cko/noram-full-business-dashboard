# NORAM Business Dashboard - Frontend

React SPA frontend for NORAM Business Dashboard.

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

Create `.env.local` (optional, defaults to localhost backend):

```
VITE_API_URL=http://localhost:8000
```

### 3. Development Server

```bash
npm run dev
```

Visit `http://localhost:5173`

## Building for Production

```bash
npm run build
npm run preview
```

## Testing

```bash
npm run test
npm run test:ui  # With UI
```

## Project Structure

```
src/
├── pages/        # Page components
├── components/   # Reusable UI components
├── api/          # API client and types
├── hooks/        # Custom React hooks
├── store/        # Zustand state management
└── utils/        # Utility functions
```

## Docker

```bash
docker build -t noram-frontend .
docker run -p 5173:5173 noram-frontend
```
