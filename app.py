import csv
import codecs
import pprint

import tornado.ioloop
import tornado.web
import tornado.database

####


def broj_slobodnih_mjesta(db, D):
    C = dict()
    for k in D.keys():
        C[k] = 0

    try:
        # povuci iz baze broj studenata po terminu
        count = db.query("select opcija, count(opcija) as 'broj' from raspored group by opcija;")
        for r in count:
            C[ str(r['opcija']) ] = r['broj']
    except Exception as e:
        print e

    S = dict()
    for k,v in D.items() :
        S[k] = int(v['mjesta']) - int(C[k])

    return S


class ProtoHandler(tornado.web.RequestHandler):
    def initialize(self, db, S, D):
        self.db = db
        self.S = S
        self.D = D

    def get_current_user(self):
        return self.get_secure_cookie("id")


class RasporedHandler(ProtoHandler):
    def get(self):
        try:
            raspored = db.query("select * from raspored")
        except Exception as e:
            print e
            self.write("pogreska --07")

        R = list()
        for r in raspored :
            if r.opcija != 0 :
                R.append( {'ime':self.S[str(r.jmbag)]["ime"],
                    'prezime':self.S[str(r.jmbag)]["prezime"],
                    'termin': self.D[str(r.opcija)]["termin"]
                } )

        R = sorted(R, key=lambda x: x['termin'])

        if self.current_user :
            self.render("html/index.html", raspored=R, logged_in=True,
                Ime=self.S[self.current_user]["ime"],
                Prezime=self.S[self.current_user]["prezime"])
        else:
            self.render("html/index.html", raspored=R, logged_in=False)



class IzaberiRasporedHandler(ProtoHandler):
    @tornado.web.authenticated
    def get(self):

        if float(self.S[str(self.current_user)]["b"]) < 10 :
            self.render("html/pricekajte.html", logged_in=True,
                Ime=self.S[self.current_user]["ime"],
                Prezime=self.S[self.current_user]["prezime"])
            return

        S = broj_slobodnih_mjesta(self.db, self.D)

        opcije = list()
        for k,v in self.D.items() :
            if S[k] > 0 :
                opcije.append( { 'opcija': k, 'termin': self.D[k]["termin"] })

        opcije = sorted(opcije, key=lambda x: x['termin'])

        jmbag = self.get_secure_cookie("id")

        try:
            r = db.query("select * from raspored where jmbag='%s'" % (jmbag,))
        except Exception as e:
            print e
            self.write("pogreska --06")

        if r != [] :
            if int(r[0].opcija) > 0:
                moj_termin = self.D[str(r[0].opcija)]["termin"]
            else:
                moj_termin = ""
        else :
            moj_termin = ""

        self.render("html/izaberi.html", opcije=opcije, moj_termin=moj_termin,
            logged_in=True,
            Ime=self.S[self.current_user]["ime"],
            Prezime=self.S[self.current_user]["prezime"])

    @tornado.web.authenticated
    def post(self):
        if float(self.S[str(self.current_user)]["b"]) <0 :
            self.render("html/pricekajte.html",
                Ime=self.S[self.current_user]["ime"],
                Prezime=self.S[self.current_user]["prezime"],
				logged_in=True)
            return

        S = broj_slobodnih_mjesta(self.db, self.D)

        try:
            if self.get_argument("opcija"):
                opcija = str(self.get_argument("opcija"))

                S = broj_slobodnih_mjesta(self.db, self.D)
                pprint.pprint(S)

                if int(opcija) > 0 :
                    if S[opcija] < 1 :
                        self.write("pogresan unos --08")
                        return

                jmbag = self.get_secure_cookie("id")
                r = db.query("select * from raspored where jmbag='%s'" % (jmbag,))
                if r != [] :
                    db.execute("update raspored set opcija='%s' where jmbag='%s'" % (opcija, jmbag))
                else:
                    db.execute("insert into raspored values ('%s', '%s')" % (jmbag, opcija))

                self.redirect("/change")
            else:
                self.write("pogresan unos --12")
        except Exception as e:
            print e
            self.write("pogresan unos --11")


class LoginHandler(ProtoHandler):
    def get(self):
        if self.get_secure_cookie("id") :
            self.redirect("/change")

        self.render("html/login.html", logged_in=False)

    def post(self):
        "Request user profile authorization"
        try:
            if self.get_argument("jmbag") and self.get_argument("b") :
                jmbag = str(self.get_argument("jmbag"))
                b = str(self.get_argument("b"))

                if self.S.get(jmbag) != None :
                    if b == self.S[jmbag]["b"]:
                        self.set_secure_cookie("id", jmbag)
                    else:
                        self.write("pogresan unos --10")
                else:
                    self.write("pogresan unos --09")
            self.redirect("/change")
        except Exception as e:
            print e


class LogoutHandler(ProtoHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")


if __name__ == "__main__":
    db = tornado.database.Connection( 'localhost',
        'grprakticni', 'grprakticni', '')

    # studenti
    csvfile = codecs.open("data/k1.csv", 'r')
    data = csv.reader(csvfile, delimiter=',')

    S = dict()
    for row in data:
        S[row[0]] = {'ime':row[1], 'prezime':row[2], 'b':row[3]}
    csvfile.close()

    # moguci termini
    csvfile = codecs.open("data/datumi.csv", 'r')
    data = csv.reader(csvfile, delimiter=',')

    D = dict()
    for row in data:
        D[row[0]] = {'mjesta':row[1], 'termin':row[2]}
    csvfile.close()

    # tornado stuff
    settings = dict(
      debug=True,
      cookie_secret="123asdffff",
      login_url="/login",
      static_path="./html/bootstrap",
    )

    application = tornado.web.Application([
        (r"/", RasporedHandler, dict(db=db, S=S, D=D)),
        (r"/login", LoginHandler, dict(db=db, S=S, D=D)),
        (r"/logout", LogoutHandler, dict(db=db, S=S, D=D)),
        (r"/change", IzaberiRasporedHandler, dict(db=db, S=S, D=D)),
        ], **settings
    )

    application.listen(8880)
    ioloop = tornado.ioloop.IOLoop().instance()
    ioloop.start()

