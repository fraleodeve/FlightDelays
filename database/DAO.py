from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMap: dict):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, t.IATA_CODE, count(*) as N
                    from (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
                    from airports a, flights f 
                    where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID
                    group by a.ID, a.IATA_CODE, f.AIRLINE_ID) t
                    group by t.ID, t.IATA_CODE
                    having N >= %s
                    order by N asc"""

        # non devo prendere tutti i nodi, ma solo una parte
        cursor.execute(query, (n,))

        for row in cursor:
            result.append(idMap[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMap: dict):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as peso
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
            # result.append((idMap[row["ORIGIN_AIRPORT_ID"]],
                           # idMap[row["DESTINATION_AIRPORT_ID"]],
                           # row["peso"])) # in alternativa creo una dataclass apposta

            result.append(Tratta(
                            idMap[row["ORIGIN_AIRPORT_ID"]],
                            idMap[row["DESTINATION_AIRPORT_ID"]],
                            row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMap: dict):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, (coalesce(t1.n,0) + coalesce(t2.n1,0)) as peso
                    from (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID ) as t1
                    left join (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n1
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID ) as t2
                    on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID and t2.ORIGIN_AIRPORT_ID = t1.DESTINATION_AIRPORT_ID
                    where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is Null"""

        cursor.execute(query)

        for row in cursor:
            # result.append((idMap[row["ORIGIN_AIRPORT_ID"]],
            # idMap[row["DESTINATION_AIRPORT_ID"]],
            # row["peso"])) # in alternativa creo una dataclass apposta

            result.append(Tratta(
                idMap[row["ORIGIN_AIRPORT_ID"]],
                idMap[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))

        cursor.close()
        conn.close()
        return result