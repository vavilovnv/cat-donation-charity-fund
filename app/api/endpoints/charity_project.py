from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    return new_project
