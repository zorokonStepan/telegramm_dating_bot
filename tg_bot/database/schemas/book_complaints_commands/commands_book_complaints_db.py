from asyncpg import UniqueViolationError
from sqlalchemy import and_

from tg_bot.database.schemas.book_complaints.book_complaints_db import ComplaintDB


# создание новой записи
async def add_record(manager_user_id: int = None, manager_username: str = None, banned_user_id: int = None,
                     banned_username: str = None, banned_reason: str = None, send_claim_user_id: int = None,
                     send_claim_username: str = None, send_claim_message: str = None, claim_user_id: int = None,
                     claim_username: str = None):
    try:
        record = ComplaintDB(manager_user_id=manager_user_id, manager_username=manager_username,
                             banned_user_id=banned_user_id, banned_username=banned_username,
                             banned_reason=banned_reason, send_claim_user_id=send_claim_user_id,
                             send_claim_username=send_claim_username, send_claim_message=send_claim_message,
                             claim_user_id=claim_user_id, claim_username=claim_username)
        await record.create()
    except UniqueViolationError:
        pass


# получение записей с жалобами
async def select_claim_records():
    records = await ComplaintDB.query.where(ComplaintDB.claim_user_id != None).gino.all()
    return records


# получение конкретной жалобы/если один и тот же жаловался на клиента несколько раз, то получим первую из этих записей
async def select_claim_record(claim_user_id: int, send_claim_user_id: int):
    record = await ComplaintDB.query.where(and_(
        ComplaintDB.claim_user_id == claim_user_id,
        ComplaintDB.send_claim_user_id == send_claim_user_id)).gino.first()
    return record


# удаление конкретной жалобы/если один и тот же жаловался на клиента несколько раз, то удаленим первую из этих записей
async def delete_claim_record(claim_user_id: int, send_claim_user_id: int):
    try:
        record = await ComplaintDB.query.where(and_(
            ComplaintDB.claim_user_id == claim_user_id,
            ComplaintDB.send_claim_user_id == send_claim_user_id)).gino.first()
        await record.delete()
        return record
    except AttributeError:
        print("*****Такой записи нет*****")
