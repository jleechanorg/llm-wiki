# PR #2: Add CORS middleware to support frontend requests

**Repo:** jleechanorg/ai_universe
**Merged:** 2025-09-18
**Author:** jleechan2015
**Stats:** +49/-124 in 2 files

## Summary
- Add CORS middleware to Express server to allow browser requests from frontend
- Configure dynamic origin validation for development and production environments  
- Update deployment documentation with correct CORS environment variables

## Raw Body
## Summary
- Add CORS middleware to Express server to allow browser requests from frontend
- Configure dynamic origin validation for development and production environments  
- Update deployment documentation with correct CORS environment variables

## Changes Made
- **Added CORS middleware** in `/backend/src/server.ts`:
  - Import `cors` package and configure dynamic origin validation
  - Support `https://storage.googleapis.com` (production frontend)
  - Support `http://localhost:3000` (development)
  - Methods: `GET, POST, OPTIONS`
  - Headers: `Content-Type, Accept, Authorization`
  - Enable credentials support

- **Updated deployment documentation** in `CLAUDE.md`:
  - Include correct `CORS_ALLOWED_ORIGINS` in gcloud deployment command
  - Ensures CORS headers persist in future deployments

- **Removed manual CORS handling** from `/mcp-json` endpoint:
  - Global middleware now handles all endpoints consistently

## Test Results ✅
All endpoints now return proper CORS headers:
- ✅ `access-control-allow-origin: https://storage.googleapis.com`
- ✅ `access-control-allow-methods: GET,POST,OPTIONS`
- ✅ `access-control-allow-headers: Content-Type,Accept,Authorization`
- ✅ `access-control-allow-credentials: true`

## Testing
```bash
# Test CORS preflight
curl -X OPTIONS -H "Origin: https://storage.googleapis.com"   -H "Access-Control-Request-Method: POST"   -H "Access-Control-Request-Headers: Content-Type"   https://ai-universe-backend-114133832173.us-central1.run.app/health

# Test actual request  
curl -H "Origin: https://storage.googleapis.com"   https://ai-universe-backend-114133832173.us-central1.run.app/health
```

## Deployment Persistence
The CORS configuration will persist in future deployments because:
1. **Environment Variable**: `CORS_ALLOWED_ORIGINS` is set in deployment command
2. **Documentation Updated**: `CLAUDE.md` includes correct origins
3. **Example Configuration**: `.env.example` already includes CORS setup

🤖 Generated with [Claude Code](https://cl
