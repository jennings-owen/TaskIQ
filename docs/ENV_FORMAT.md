# Environment Variables Reference

This document defines all environment variables used in the project and serves as a template.

### Root .env (place in root directory)
```env
OPENAI_API_KEY=KEY_HERE # for AI generated responses
BACKEND_PORT=8000
BACKEND_URL=http://localhost:8000
FRONT_END_URL=http://localhost:3000
COMPOSE_PROJECT_NAME=synapsesquad
SECRET_KEY=SECRET_KEY_HERE
BACKEND_PORT=8000
```

### Frontend .env (place in `/frontend/` folder)
```env
REACT_APP_BACK_END_URL=http://localhost:8000  # should match backend url above
PORT=3000  # port to run front end on.
```

**Note:** React only exposes variables prefixed with `REACT_APP_` at build time.
