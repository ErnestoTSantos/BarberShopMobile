from .models import User, Estabelecimento, Profissional, Cliente, Agenda
from .database import database
from .auth import get_password_hash


async def create_user(email, password, name=None, role="client"):
    hashed = get_password_hash(password)
    query = User.__table__.insert().values(
        email=email, hashed_password=hashed, name=name, role=role
    )
    user_id = await database.execute(query)
    return {"id": user_id, "email": email, "name": name, "role": role}


async def get_user_by_email(email):
    query = User.__table__.select().where(User.__table__.c.email == email)
    return await database.fetch_one(query)


async def create_estabelecimento(data):
    query = Estabelecimento.__table__.insert().values(**data)
    id_ = await database.execute(query)
    return {**data, "id": id_}


async def list_estabelecimentos():
    query = Estabelecimento.__table__.select()
    return await database.fetch_all(query)


async def create_profissional(data):
    query = Profissional.__table__.insert().values(**data)
    id_ = await database.execute(query)
    return {**data, "id": id_}


async def list_profissionais():
    query = Profissional.__table__.select()
    return await database.fetch_all(query)


async def create_cliente(data):
    query = Cliente.__table__.insert().values(**data)
    id_ = await database.execute(query)
    return {**data, "id": id_}


async def list_clientes():
    query = Cliente.__table__.select()
    return await database.fetch_all(query)


async def create_agenda(data):
    query = Agenda.__table__.insert().values(**data)
    id_ = await database.execute(query)
    return {**data, "id": id_}


async def list_agenda_by_profissional(profissional_id):
    query = Agenda.__table__.select().where(
        Agenda.__table__.c.profissional_id == profissional_id
    )
    return await database.fetch_all(query)
