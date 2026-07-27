# Frontend for Workout Logger

This is a Next.js frontend for the Flask backend in the parent repository.

## Setup

1. Open a terminal in `frontend`
2. Run `npm install`
3. Run the Flask backend on port `7010`
4. Run `npm run dev`
5. Open `http://localhost:3000`

## Notes

- API requests are proxied to `http://localhost:7010/api/...`
- Static images are proxied from the Flask backend at `/static/...`
