from typing import List

from sqlalchemy import and_

from utils.db_api.dataBase import db
from utils.db_api.models import Item


async def add_item(**kwargs):
    # Добавление товара
    new_item = await Item(**kwargs).create()
    return new_item


async def get_categories() -> List[Item]:
    return await Item.query.distinct(Item.category_code).gino.all()


async def get_subcategories(category) -> List[Item]:
    return await Item.query.distinct(Item.subcategory_code).where(Item.category_code == category).gino.all()


async def count_items(category_code, subcategory_code=None):
    # показывает количество товара оставшегося
    conditions = [Item.category_code == category_code]

    if subcategory_code:
        conditions.append(Item.subcategory_code == subcategory_code)

    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total


async def get_items(category_code, subcategory_code) -> List[Item]:
    items = await Item.query.where(
        and_(Item.category_code == category_code,
             Item.subcategory_code == subcategory_code)
    ).gino.all()
    return items


async def get_item(item_id) -> Item:
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item
