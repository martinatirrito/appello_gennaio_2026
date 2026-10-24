from database.DB_connect import DBConnect
from model.Constructor import Constructor
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(year1, year2):

        conn = DBConnect.get_connection()
        if conn is None:
            print("Errore di connessione al database")
            return []
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select distinct c.*
                    from constructors c, results r, races ra
                    where c.constructorId = r.constructorId and r.raceId = ra.raceId 
                    and ra.`year` BETWEEN %s and %s
                    and r.`position` is not NULL """


        cursor.execute(query, (year1, year2, ) )

        for row in cursor:
            result.append(Constructor(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(year1, year2, idMapC):

        conn = DBConnect.get_connection()
        if conn is None:
            print("Errore di connessione al database")
            return []
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select c1.constructorId as c1, c2.constructorId as c2, count(distinct c1.pilota) as peso
                    from(select distinct c.constructorId, r.driverId as pilota, ra.raceId as gara
                            from constructors c, results r, races ra
                            where c.constructorId = r.constructorId and r.raceId = ra.raceId 
                            and ra.`year` BETWEEN %s and %s
                            and r.`position` is not NULL ) c1, (select distinct c.constructorId, r.driverId as pilota, ra.raceId as gara
                                from constructors c, results r, races ra
                                where c.constructorId = r.constructorId and r.raceId = ra.raceId 
                                and ra.`year` BETWEEN %s and %s
                                and r.`position` is not NULL ) c2
                    where c1.constructorId < c2.constructorId 
                    and c1.pilota = c2.pilota 
                    and c1.gara != c2.gara 
                    group by c1.constructorId , c2.constructorId """

        cursor.execute(query, (year1, year2, year1, year2, ))

        for row in cursor:
            result.append(Arco(idMapC[row["c1"]], idMapC[row["c2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result

