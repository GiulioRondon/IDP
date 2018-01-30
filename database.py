import psycopg2 as p
import math

class Database:
    def __init__(self):
        self.con = p.connect("dbname='IDP' user='postgres' password='D247vDqerty'")
        self.cur = self.con.cursor()

    def select(self):
        self.cur.execute("SELECT * FROM gebruiker")
        self.gebruiker = self.cur.fetchall()


    def nearestLoc(self):
        self.cur.execute("SELECT * FROM locations")
        locatie = self.cur.fetchall()
        locLST = []
        for i in locatie:
            x = math.sqrt((i[1] - self.gebruiker[0][0])**2 + (i[2] - self.gebruiker[0][1])**2)
            locLST.append(x)
            print('De afstand tussen', self.gebruiker[0], 'en ', i ,'is', x)
        print('The nearest locationn is:',locatie[locLST.index(min(locLST))][0], 'and is: ', min(locLST), 'away from user')


if __name__ == '__main__':
    database = Database()
    database.select()
    database.nearestLoc()