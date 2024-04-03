import redis

class Dolgozok():
    
    def __init__(self):
        redis_host='172.22.233.176'
        redis_port=6379
        
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True) 
            
            
            
#   1. Egy dolgozo hozzaadasa a hash-hez, es a hash inicializalasa, ha az nem letezik.
#   szarul mukszik, spameli hogy "mar van ilyen email" xD
    def uj_dolgozo(self, email, nev):
        if self.r.hexists('h_dolgozok', email):
            print('mar van ilyen email.')
            return;
        self.r.hset('h_dolgozok', email, nev)
    
    
#   2. kiadja az emailhez tartozo nevet
    def dolgozo_emailhez_nev(self, email):
        print(self.r.hget('h_dolgozok', email))
    
#   3. kiadja a nevhez tartozo emailt.
    def dolgozo_nevhez_email(self, name):
        print('nevhez email:')
        for d in self.r.hkeys('h_dolgozok'):
            if self.r.hget('h_dolgozok', d )== name:
                print(d)
                
#   4. feladat generalasa. Kiirja ki irja ki (email), egy leiras, es egy prioritas. ezenkivul egy egyedi azonosito.
#   hash megint vszleg, 
    def uj_feladat(self, kiiro_email, leiras, prioritas):
        #ha nincs ugy is letrehozza az incr
        f_azon=str(self.r.incr('feladat_azon'))
        
#       beleraktuk a pipeline-t rak se tudja m ez :DDDDDDDDDDDDDDDDD
        p = self.r.pipeline(transaction=True)
        #hmset: tobb kulcs-ertek part rak be egy hashben.
        p.hmset('h_feladat_'+f_azon,{'kiiro_email':kiiro_email, 'leiras':leiras})
        p.zadd('z_feladatok', {f_azon:prioritas})
        return f_azon
        
#   5. lehetseges munkavegzo hozzaadasa egy feladathoz.
    def lehetseges_munkavegzo(self, f_azon, email):
        self.r.sadd('s_lehetseges_munkavegzok_'+f_azon, email)

#   6. kiirja egy feladathoz megengedett munkavegzoket
    def lehetseges_munkavegzok_listaja(self, f_azon):
        for l in self.r.smembers('s_lehetseges_munkavegzok_'+f_azon):
            print(l)

#   7. kiirja a prioritasi listat.
    def prioritas_lista(self):
        for p in self.r.zrange('z_feladatok', 0, -1, withscores=True):
            print(p)
    
#   8. kiirja egy feladatnak a leirasat
    def feladat_leirasa(self, f_azon):
        print(self.r.hget('h_feladat_'+f_azon, 'leiras'))
        
#   9. elvegez egy feladatot, es kitorli azt.
    def munka_elvegzese(self, f_azon, email):
        
        if self.r.zscore('z_feladatok', f_azon)==None:
            print('Nincs ilyen feladat')
            return
        
        if not(self.r.hexists('h_dolgozok', email)):
            print('Nincs ilyen dolgozo.')
            return
        
        if not(self.r.sismember('s_lehetseges_munkavegzok_'+f_azon, email)):
            print('Nincs a lehetseges munkavegzok kozott.')
            return
        
        print('f_azon:', f_azon)
        print(self.r.hgetall('h_feladat_'+f_azon))
        print(self.r.zscore('z_feladatok', f_azon))
        
        
        
        p=self.r.pipeline()
        #novekszik a megoldott feladatok szama
        p.zincrby('z_elvegzett_feladatok', 1, email)
        #torlesek
        p.delete('s_lehetseges_munkavegzok_'+f_azon)
        p.zrem('z_feladatok', f_azon)
        p.delete('h_feladat_'+f_azon)
        
        #ezzel meg imitaljuk hogy midnen egyszerre fusson le.
        #pipeline a zh-ban = +1 pont 
        p.execute()

#   10. kiirja a munkavegzok listajat.
    def munkavegzok_listaja(self):
        for munkavegzo in self.r.zrevrange('z_elvegzett_feladatok', 0, -1, withscores=True):
            print(munkavegzo)
            
