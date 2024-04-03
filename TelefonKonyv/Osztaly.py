import redis

class TelefonKonyv():
    
    def __init__(self):
        redis_host='172.22.233.176'
        redis_port=6379
        
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True) 
            
    
    def uj_kapcsolat(self, nev):
        # amikor 0-t hasznalunk az lrem-nel minden nevet kitorol.
        self.r.lrem('l_kapcsolatok', 0,nev)
        self.r.lpush('l_kapcsolatok',nev)
        
        # csak az elso 5ot irjuk ki.
        self.r.ltrim('l_kapcsolatok', 0, 4)
        
    def kapcs_lista(self):
        print(self.r.lrange('l_kapcsolatok', 0, -1))
        
    
    def kapcsolat_kezdet(self, kezdet):
        for i in self.r.lrange('l_kapcsolatok', 0, -1):
            if i[0:len(kezdet)] == kezdet:
                print(i)
        n b 