import logging

from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv

from .database import database, engine
from . import models, crud, auth
from .schemas import *

logger = logging.getLogger(__name__)

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Barbershop API")


@app.on_event("startup")
async def on_startup():
    """Connect to the database when the app starts."""
    await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    """Disconnect from the database when the app stops."""
    await database.disconnect()


@app.post("/signup", response_model=UserOut)
async def signup(payload: UserCreate):
    """Register a new user."""
    existing_user = await crud.get_user_by_email(payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await crud.create_user(
        email=payload.email, password=payload.password, name=payload.name
    )
    return user


@app.post("/login", response_model=Token)
async def login(payload: UserLogin):
    """Login user and return JWT token."""
    user = await crud.get_user_by_email(payload.email)
    if not user or not auth.verify_password(payload.password, user["hashed_password"]):
        logger.warning(f"Failed login attempt for {payload.email}")
        if not user:
            logger.warning(f"User {payload.email} does not exist")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/establishments", response_model=EstablishmentOut)
async def create_establishment(payload: EstablishmentCreate):
    """Create a new establishment."""
    return await crud.create_estabelecimento(payload.dict())


@app.get("/establishments", response_model=list[EstablishmentOut])
async def list_establishments():
    """Get all establishments."""
    return await crud.list_estabelecimentos()


@app.post("/professionals", response_model=ProfessionalOut)
async def create_professional(payload: ProfessionalCreate):
    """Create a new professional."""
    return await crud.create_profissional(payload.dict())


@app.get("/professionals", response_model=list[ProfessionalOut])
async def list_professionals():
    """Get all professionals."""
    return await crud.list_profissionais()


@app.post("/clients", response_model=ClientOut)
async def create_client(payload: ClientCreate):
    """Create a new client."""
    return await crud.create_cliente(payload.dict())


@app.get("/clients", response_model=list[ClientOut])
async def list_clients():
    """Get all clients."""
    return await crud.list_clientes()


@app.post("/agenda", response_model=AgendaOut)
async def create_schedule(payload: AgendaCreate):
    """Create a new schedule/event."""
    return await crud.create_agenda(payload.dict())


@app.get("/agenda/{professional_id}", response_model=list[AgendaOut])
async def list_schedule_by_professional(professional_id: int):
    """Get agenda for a specific professional."""
    return await crud.list_agenda_by_profissional(professional_id)
