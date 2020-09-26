from fastapi import FastAPI

from .apis import users_router, auth_router, services_router, tickets_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(services_router, prefix="/api/services", tags=["Services"])
app.include_router(tickets_router, prefix="/api/tickets", tags=["Tickets"])
