# Fotógaléria Webalkalmazás (MVP)

Ez egy egyszerű, könnyűsúlyú Python és Flask alapú webalkalmazás, amely lehetővé teszi fényképek feltöltését, listázását, megtekintését és törlését. Az alkalmazás jelenlegi verziója egy Minimum Viable Product (MVP), amely már felhőben fut és PostgreSQL adatbázist használ.

## 🚀 Funkciók

* **Fényképek feltöltése:** Képek feltöltése tetszőleges névvel (maximum 40 karakter).
* **Automatikus dátumozás:** A rendszer automatikusan rögzíti a feltöltés pontos idejét.
* **Listázás és rendezés:** A feltöltött képek listázása. A lista rendezhető:
  * Név szerint (A-Z és Z-A)
  * Feltöltési dátum szerint (legújabb vagy legrégebbi elöl)
* **Megtekintés:** A listában a kép nevére kattintva a fotó eredeti méretben megtekinthető.
* **Törlés:** Képek végleges törlése (mind az adatbázisból, mind a szerver háttértáráról).

## ☁️ Deployment

Az alkalmazás publikus felhő környezetben fut:

* **Platform:** Render (PaaS)
* **Web Service:** Flask alkalmazás deployolva mint web app
* **Adatbázis:** PostgreSQL (Render által biztosított managed database)

A backend a Render infrastruktúráján fut, és egy külön PostgreSQL adatbázishoz csatlakozik környezeti változókon keresztül.

## 🛠️ Használt technológiák

* **Backend:** Python 3, Flask
* **Adatbázis:** PostgreSQL (Flask-SQLAlchemy ORM)
* **Frontend:** HTML5, CSS, Jinja2 sablonmotor
* **Deployment:** Render (PaaS)

## ⚙️ Környezeti változók

A futtatáshoz az alábbi környezeti változók szükségesek:

* `DATABASE_URL` – PostgreSQL kapcsolat string (Render automatikusan biztosítja)
