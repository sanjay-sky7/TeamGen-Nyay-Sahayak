# Nyay Sahayak - AI Legal Assistant

This is a [Next.js](https://nextjs.org) project for Nyay Sahayak, an AI-powered legal assistant that helps citizens navigate legal procedures in India.

## Features

- 🤖 AI-powered legal roadmap generation using Google Gemini
- 🔍 Query backend API for legal advice and procedures
- 📋 Generate detailed legal roadmaps including:
  - Immediate actions to take
  - FIR filing steps
  - Evidence preservation guidelines
  - Relevant laws and statutes
- 🌐 Support for different states and jurisdictions
- 💾 Copy, download, and share legal roadmaps

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API server running on `http://localhost:8080` (or configure via environment variables)

### Installation

1. Install dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
# or
bun install
```

2. Configure environment variables (optional):

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8080
```

If not set, the app defaults to `http://localhost:8080`.

3. Start the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Backend Integration

The frontend integrates with the Nyay Sahayak backend API. The backend should be running on `http://localhost:8080` (or the URL specified in your environment variables).

### API Endpoints

The frontend uses the following backend endpoints:

- `GET /api/v1/health` - Health check endpoint
- `POST /api/v1/query` - Main query endpoint (uses Google Gemini)
  - Request body: `{ "query": "your legal query here" }`
  - Response: Legal roadmap with crime type, immediate actions, FIR steps, evidence to preserve, and relevant laws

### Backend Requirements

Make sure your backend server is:
- ✅ Running on the configured port (default: 8080)
- ✅ CORS enabled for `http://localhost:3000`
- ✅ Index built (run `python build_index.py` if needed)
- ✅ Google API key set in backend `.env` file

### Testing the Integration

You can test the API connection using curl:

```bash
# Health check
curl -X GET "http://localhost:8080/api/v1/health"

# Query endpoint
curl -X POST "http://localhost:8080/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "I was scammed online. Someone called me pretending to be from my bank and took my OTP."}'
```

## Project Structure

```
src/
├── app/
│   ├── page.tsx              # Main page component
│   └── api/                  # Next.js API routes (if needed)
├── components/
│   └── nyay-sahayak/         # Nyay Sahayak specific components
│       ├── header.tsx
│       ├── input-form.tsx
│       ├── result-card.tsx
│       └── theme-toggle.tsx
└── lib/
    └── api/
        └── nyay-sahayak.ts   # Backend API client
```

## Features

- **Offline Mode**: If the backend is unavailable, the app falls back to mock responses
- **Backend Status Indicator**: Visual indicator showing backend connection status
- **Error Handling**: Graceful error handling with user-friendly messages
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode**: Theme toggle for light/dark mode

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
