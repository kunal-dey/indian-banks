from typing import Optional
from exceptions.db_connection_exceptions import DbConnectionException

from utils.db_connection import read_from_db

from schemas.input_schemas.ifsc import Ifsc
from schemas.output_schemas.bank import Bank


class BankModel:

    def __init__(self, bank:Bank):
        self.bank = bank

    @staticmethod
    def find_by_ifsc(
            ifsc: Ifsc,
            limit: Optional[int] = None, 
            offset:Optional[int] = None
        ):
        try:
            with read_from_db() as c:
                query = """
                            SELECT branch, address, city, district, state, bank_name
                            FROM bank_branches 
                            WHERE ifsc=%s
                        """
                data = [ifsc.ifsc_code]
                if limit:
                    query += "LIMIT %s"
                    data.append(limit)
                if offset:
                    query += "OFFSET %s"
                    data.append(offset)
                c.execute(query, tuple(data))
                result = c.fetchall()
        except:
            raise DbConnectionException()
        return [
            Bank.from_db(*result[i]) for i in range(len(result))
            ] if result else None
