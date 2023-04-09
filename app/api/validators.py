from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_name_is_exist(
    *,
    project_name: str,
    project_id: int = None,
    session: AsyncSession
) -> None:
    id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if id and id != project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_is_exist(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Не найден благотворительный проект с id {project_id}'
        )
    return project


def check_money_amount(obj, new_amount=None):
    invested = obj.invested_amount
    if new_amount:
        if invested > new_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f'Сумма не может быть меньше вложенной: {invested}'
            )
    elif invested > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return obj


def check_project_is_closed(obj):
    if obj.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
