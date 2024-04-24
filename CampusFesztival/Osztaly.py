import redis
from test.test_idle import tk

class Osztaly():
    
    def __init__(self):
        redis_host='172.22.233.176'
        redis_port=6379
        
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True) 
            
    
    def uj_helyszin(self, hsz):
        self.r.sadd("s_helyszinek", hsz)
        
        
    def helyszin_lista(self):
        print(self.r.smembers("s_helyszinek"))
        
        
    def uj_esemeny(self, hsz, kezdet, veg, megnevezes, fnev, ftel):
        if not (self.r.sismember("s_helyszinek", hsz)):
            print("nincs ilyen helyszin")
            return
        if self.r.zscore("z_esemenyek", megnevezes)!=None:
            print("Ilyen nevu esemeny mar letezik.")
        
        if kezdet>veg:
            print("hibas idopont (elobb vegzodik)")
            return 
        
        for e in self.r.zrange("Z_esemenyek", 0, -1, withscores=False):
            if self.r.hget("h_esemeny_"+e, "helyszin")!=hsz:
                continue
            tk=self.r.hget(("h_esemeny_"+e), kezdet)
            tv=self.r.hget(("h_esemeny_"+e), veg)
            
            if not(veg<tk or tv < kezdet):
                print("a helyszinen mar van esemeny")
                return
            
            
        
        
        self.r.hmset("h_esemeny_"+megnevezes, {"helyszin:":hsz,
                                               "kezdet:":kezdet,
                                                "veg:":veg,
                                                "megnevezes:":megnevezes,
                                                "felelos nev:":fnev, 
                                                "felelos telefon:":ftel})
        self.r.zadd("z_esemenyek", {megnevezes: kezdet})
        
    def esemeny_lista_idopont(self, idopont):
        for e in self.r.zrangebyscore("z_esemenyek", 0, idopont, withscores=False):
            if self.rhget("h_esemeny"+e, "veg")>idopont:
                print(self.r.hgetall("h_esemeny_"+e))
                
    def esemeny_lista(self):
        for e in self.r.zrange("z_esemenyek", 0, -1, withscores=False):
            print(self.r.hgetall("h_esemeny_"+e))
                
    def uj_jegytipus(self, nev, ar, erv_kezdet, erv_veg):
        if self.r.sismember("s_jegytipusok", nev):
            print("mar van ilyen")
            return
        self.r.hmset("h_jegytipus_"+nev,{"nev:" : nev,
                                         "ar:": ar,
                                         "ervenyesseg kezdete:": erv_kezdet,
                                         "ervenyesseg vege:": erv_veg})
        self.r.sadd("s_jegytipusok", nev)
        
        
    def jegytipus_lista(self):
        for j in self.r.smembers("s_jegytipusok"):
            print(self.r.hgetall("h_jegytipus_"+j))
            
    def uj_vendeg(self, email, nev, szul_dat):
        if self.r.sismember("s_vendegek", email):
            print("az alabbi email-el mar regisztraltak.")
            return
        
        self.r.hmset("h_vendeg_"+email, {"nev":nev,
                                          "szul_dat:":szul_dat,})
        self.r.sadd("s_vendegek",email)
        
        
    def vendeg_lista(self):
        for v in self.r.smembers("s_vendegek"):
            print(self.r.hgetall("h_vendeg_"+v))
            
    def vendeg_jegyet_vasarol(self,email,jegytipus):
        if not(self.r.sismember("s_vendegek", email)):
            print("nincs ilyen email-el rendelkezo vendeg.")
            return
        if not(self.r.sismember("s_jegytipusok", jegytipus)):
            print("nincs ilyen jegytipus")
            return
        self.r.sadd("s_vendeg_jegyei_"+email, jegytipus)
        
    def vendeg_lista_idopont(self, idopont):
        for v in self.r.smembers("s_vendegek"):
            for jt in self.r.smembers("s_vendeg_jegyei_"+v):
                kezdet=self.r.hget("h_jegytipus"+jt, "erv_kezdet")
                veg=self.r.hget("h_jegytipus_"+jt, "erv_veg")
                if kezdet<idopont and idopont<veg:
                    print(v)
                    print(self.r.hgetall("h_vendeg_"+v))
                    
    
    def like(self, email, esemeny):
        if not(self.r.sismember("s_vendegek", email)):
            print("nincs ilyen emaillel rendelkezo vendeg.")
            return
        if not (self.r.exists("h_esemeny_"+esemeny)):
            print("nincs ilyen esemeny")
            return 
        if self.r.sismember("s_likeok_"+email, esemeny):
            print("az esemenyt mar likeolta.")
            return
        
        self.r.sadd("s_likeok_"+email, esemeny)
        self.r.zincrby("z_likeok", 1, esemeny)
        
        
    def esemeny_lista_by_like(self):
        for e in self.r.zrevrange("z_likeok", 0, -1, withscores=False):
            print(self.r.hgetall("h_esemeny_"+e))
            print("likeok:" + self.r.zscore("z_likeok", e))
            
    def vendeg_like_lista(self, email):
        for e in self.r.smembers("s_likeok_"+email):
            print(e)