Házi címe:
----------
Github Pull Request lifecycle test


Feladat rövid leírása:
----------------------

A github Pull request rendszerenek tesztelese a cel. A fobb allapotok (amit a gui direktben jelez is): draft, open, merged es closed.
Ezek kozett az allapotok kozott tobbe szabad az atmenet (closed es merged-bol nincs tovabb), az atmenet azonban komplex feltetelektol fugghet, amit a github feluleten lehet koniguralni.
Pelda: open -> merged eseten:
* Approve szugseges
* CI sikeres lefutasa szukseges
* Megfelelo felhasznaloi jogosultsag szuksegs (tobb felhasznalos eseteket nem tervezem megnezni)
* A git merge/rebase/squash muveletek lehetsegesek (nincs konfliktus)



Mi lesz a SUT (System Under Test)?:
-----------------------------------

A SUT alapvetoen a https://github.com/ lesz, ez azonban valoszinuleg konnyen kiterjesztheto lehetne gitlab alapo webloldalakra is, hiszen a ketto nagyban megegyezik.


Kapcsolódik korábbi/párhuzamos témához, ha igen mihez és mi ehhez képest az új?:
--------------------------------------------------------------------------------

Nem kapcsolodik.



Felhasznált tool-okra van-e már elképzelés, ha igen, mi?:
---------------------------------------------------------

* fMBT
* python/selenium


Megjegyzés (opcionális):
------------------------




