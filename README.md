# Fotógaléria Webalkalmazás (MVP)

Ez egy egyszerű, könnyűsúlyú Python és Flask alapú webalkalmazás, amely lehetővé teszi fényképek feltöltését, listázását, megtekintését és törlését. Az alkalmazás jelenlegi verziója egy Minimum Viable Product (MVP), amely lokális SQLite adatbázist használ.

## 🚀 Funkciók

* **Fényképek feltöltése:** Képek feltöltése tetszőleges névvel (maximum 40 karakter).
* **Automatikus dátumozás:** A rendszer automatikusan rögzíti a feltöltés pontos idejét.
* **Listázás és Rendezés:** A feltöltött képek listázása. A lista rendezhető:
    * Név szerint (A-Z és Z-A)
    * Feltöltési dátum szerint (Legújabb vagy Legrégebbi elöl)
* **Megtekintés:** A listában a kép nevére kattintva a fotó eredeti méretben megtekinthető.
* **Törlés:** Képek végleges törlése (mind az adatbázisból, mind a szerver/gép háttértáráról).

## 🛠️ Használt technológiák

* **Backend:** Python 3, Flask keretrendszer
* **Adatbázis:** SQLite (Flask-SQLAlchemy ORM-en keresztül)
* **Frontend:** HTML5, beépített CSS (Jinja2 sablonmotorral)


