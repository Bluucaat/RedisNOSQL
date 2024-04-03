from Dolgozok import Dolgozok

d=Dolgozok();

d.uj_dolgozo('a@g.c', 'anna')
d.uj_dolgozo('b@g.c', 'bela')
d.uj_dolgozo('c@g.c', 'cili')


d.dolgozo_emailhez_nev('a@g.c')
d.dolgozo_nevhez_email('cili')

f_azon1 = d.uj_feladat('a@g.c', 'leiras', 5)
f_azon2 = d.uj_feladat('b@g.c', 'mosogat', 5)
f_azon3 = d.uj_feladat('b@g.c', 'felmos', 3)
f_azon4 = d.uj_feladat('a@g.c', 'mos', 5)


d.lehetseges_munkavegzo(f_azon1, 'a@a.c')
d.lehetseges_munkavegzo(f_azon2, 'c@a.c')
d.lehetseges_munkavegzo(f_azon3, 'c@a.c')

# egyhez tobbet is rendelhet
d.lehetseges_munkavegzo(f_azon1, 'a@a.c')
d.lehetseges_munkavegzo(f_azon1, 'b@a.c')
d.lehetseges_munkavegzo(f_azon1, 'a@a.c')
d.lehetseges_munkavegzo(f_azon2, 'c@a.c')

print('lehetseges munkavegzok az 1. feladathoz: ')
d.lehetseges_munkavegzok_listaja(f_azon1)

print('lehetseges munkavegzok a 2. feladathoz: ')
d.lehetseges_munkavegzok_listaja(f_azon2)
print()
d.prioritas_lista()
    
d.feladat_leirasa(f_azon2)
d.feladat_leirasa(f_azon1)

d.munka_elvegzese(f_azon1, 'c@g.c')
d.munka_elvegzese(f_azon1, 'a@g.c')
d.munka_elvegzese(f_azon2, 'c@g.c')

d.munkavegzok_listaja()




