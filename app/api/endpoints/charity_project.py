from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_name_is_exist, check_project_is_closed,
    check_project_is_exist, check_money_amount
)
from app.api.utils import investing_process
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_project_name_is_exist(
        project_name=charity_project.name,
        session=session
    )
    new_project = await charity_project_crud.create(charity_project, session)
    new_project = await investing_process(session, new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_is_exist(project_id, session)
    project = check_money_amount(project)
    project = await charity_project_crud.delete(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_is_exist(project_id, session)
    check_project_is_closed(project)
    if obj_in.name is not None:
        await check_project_name_is_exist(
            project_name=obj_in.name,
            project_id=project_id,
            session=session)
    if obj_in.full_amount is not None:
        check_money_amount(project, obj_in.full_amount)
    project = await charity_project_crud.update(obj_in, project, session)
    return project
