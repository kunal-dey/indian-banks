from typing import Optional
from exceptions.db_connection_exceptions import DbConnectionException

from utils.db_connection import read_from_db

from schemas.output_schemas.branch import Branch


class BranchModel:

    def __init__(self, branch:Branch):
        self.branch = branch

    @staticmethod
    def find_by_bank_and_city(
                    bank_name: str,
                    city: str, 
                    limit: Optional[int] = None, 
                    offset:Optional[int] = None
                ):
        try:
            with read_from_db() as c:
                query = """
                            SELECT branch, ifsc, district, state, address
                            FROM bank_branches 
                            WHERE city=%s AND bank_name=%s
                        """
                data = [city,bank_name]
                if limit:
                    query += "LIMIT %s"
                    data.append(limit)
                if offset:
                    query += "OFFSET %s"
                    data.append(offset)
                c.execute(query, tuple(data))
                result = c.fetchall()
        except Exception as e:
            print(e)
            raise DbConnectionException()
        return [
            Branch.from_db(*result[i]) for i in range(len(result))
            ] if result else None