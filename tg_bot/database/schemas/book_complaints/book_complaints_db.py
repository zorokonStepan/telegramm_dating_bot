from sqlalchemy import Column, BigInteger, String, sql, Integer

from tg_bot.database.db_gino import TimedBaseModel


class ComplaintDB(TimedBaseModel):
    __tablename__ = 'book_complaints'

    table_id = Column(Integer, primary_key=True)
    # кто забанил
    manager_user_id = Column(BigInteger)
    manager_username = Column(String(100))

    # кого забанили и за что
    banned_user_id = Column(BigInteger)
    banned_username = Column(String(100))
    banned_reason = Column(String(1000))

    # кто написал жалобу
    send_claim_user_id = Column(BigInteger)
    send_claim_username = Column(String(100))
    send_claim_message = Column(String(1000))

    # на кого написали жалобу
    claim_user_id = Column(BigInteger)
    claim_username = Column(String(100))

    query: sql.Select
