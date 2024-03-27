import redis

class Jatek():
    
    def __init__(self):
        redis_host='172.22.233.176'
        redis_port=6379
        
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True) 
        
    def uj_jatek(self, kezdobetu):
        for i in self.r.zrevrange('z_osszjatek_rangsor',
                                   0, -1, withscores=False):
            self.r.delete('s_szavak_'+i)
            
        self.r.delete('z_jatek_rangsor')
        self.r.setex('jatek', kezdobetu[0], 60)
    
    def bekuld(self, szo, jatekos):
        if not(self.r.exists('jatek')):
            print("nincs jatek")
            return
        if szo[0] != self.r.get('jatek'):
            print('rossz kezdobetu')
            return
        
        self.r.sismember('s_szavak_'+jatekos, szo)
        
        self.r.sadd('s_szavak_'+jatekos,szo)
        self.r.zincrby('z_jatekrangsor', jatekos, 1)
        self.r.zincrby('z_osszjatekrangsor', jatekos, 1)
        return
    
    def jatek_rangsor(self):
        print(self.r.zrevrange('z_jatekrangsor',
                                0, -1, withscores=True,))
        
    def ossz_jatek_rangsor(self):
        for i in self.r.zrevrange('z_osszjatekrangsor',
                                   0, -1, withscores=True):
            print(i)
        