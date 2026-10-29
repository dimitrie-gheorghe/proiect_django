from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import redirect
import datetime as dt
import locale

from .models import Categorie

locale.setlocale(locale.LC_ALL, 'ro_RO.UTF-8')

accesari = []
def actualizeaza_accesari(request):
    global accesari
    a = Accesare(request)
    accesari.append(a)

class Accesare:
    contor = 1
    def __init__(self, request, parametri={}):
        self.id = Accesare.contor
        Accesare.contor += 1
        self.ip_client = request.ip
        self.parametri = parametri
        self.url = request.get_full_path()
        self.data = dt.datetime.now()
        self.pg = request.path[len("/aplicatie_magazin"):]
        #self.request = request
        
    def __str__(self):
        return f"""<ul>
            <li>Accesare. ID: {self.id}</li>
            <li>string_url: {self.url}</li>
            <li>pagina: {self.pg}</li>
            <li>calculeaza_data: {self.data}</li>
            <li>accesari_afisate_parametri: {self.accesari_afisate_parametri()}</li></ul>
        """

    def get_id(self):
        return self.id

    def accesari_afisate_parametri(self):
        return [
            ("id", self.id),
            ("ip_client", self.ip_client),
            ("parametri", self.parametri),
            ("url", self.url),
            ("data", self.data),
        ]
    
    def string_url(self):
        """returneaza /aplicatie_magazin/pag1?a=1"""
        return self.url
    
    def pagina(self):
        """returneaza /pag1"""
        return self.pg
    
    def calculeaza_data(self, data=""):
        #locale.setlocale(locale.LC_ALL, 'ro_RO.UTF-8') Am adaugat asta la inceputul programului
        if data == "":
            return self.data.strftime("%A, %d %B %Y.") # Duminică, 18 Octombrie 2026.
        if data == "zi":
            return self.data.strftime("%d %B %Y.") # 18 Octombrie 2026.
        if data == "timp":
            return self.data.strftime("%H:%M:%S")
        return self.data.strftime("%A, %d %B %Y.") # Duminică, 18 Octombrie 2026.
        

def index(request):
    actualizeaza_accesari(request)
    a = request.proprietate_noua
    return HttpResponse(
        f"""<html><body>
                <h1>Magazin de electrocasnice</h1>
                <p>{request.GET.getlist("param")}</p>
            </body></html>
        """
    )

def pag1(request):
    actualizeaza_accesari(request)
    
    l = len("/aplicatie_magazin")
    p = request.path[l:]
    print(p)
    return HttpResponse(2+3)


l=[]
def pag2(request):
    actualizeaza_accesari(request)
    global l
    a = request.GET.get("a",10)
    print(request.GET)
    l.append(a)
    return HttpResponse(f"<b>Am primit</b>: {l}")

def info(request):
    actualizeaza_accesari(request)
    a = Accesare(request)

    descriere = "De la acest magazin online se pot cumpăra diverse electrocasnice (frigidere, mașini de spălat, televizoare, etc.). Site-ul pune la dispoziția utilizatorului diverse metode de căutare a categoriilor, precum și opțiuni de filtrare a rezultatelor. categoriile dorite se adaugă în coșul de cumpărături în vederea achiziționării."
    
    data = request.GET.get("data", "")
    return HttpResponse(
        f"""<html><body>
                <title>Informații despre server</title>
                <h1>Informații despre server</h1>
                <p>{descriere}</p>
                <p>{a.__str__()}</p>
                <section>
                    <h2>Data și ora</h2>
                    <p>{a.calculeaza_data(data)}</p>
                </section>
            </body></html>
        """
    )

def log(request):
    actualizeaza_accesari(request)
    
    iduri = request.GET.getlist("iduri")
    dubluri = request.GET.get("dubluri", False)
    
    eroare = ""
    accesari_afisate = []
    aux = []
    for id in iduri:
        aux.extend(id.split(","))
    iduri = list(map(int, aux.copy()))
    
    if dubluri is False:
        aux = []
        for id in iduri:
            if id not in aux:
                aux.append(id)
        iduri = aux.copy()
    
    try:
        accesari_afisate = [accesari[i - 1] for i in iduri]
    except IndexError:
        eroare = "EROARE: parametrii sunt gresiti"

    if accesari_afisate == []:
        n = request.GET.get("ultimele", "")
        numar = None
        if n == "":
            numar = len(accesari)
        else:
            try:
                n = int(n)
            except ValueError:
                eroare = "EROARE: parametrul 'ultimele' are valoare gresita"
            else:
                if n > 0:
                    numar = n
                else:
                    eroare = f"nu se pot afisa {n} accesari"
        if numar is not None:
            accesari_afisate = accesari[:numar]
            if n != "" and n > len(accesari):
                eroare = f"Exista doar {len(accesari)} accesari fata de {n} accesari cerute"
    
    param_accesari = request.GET.getlist("accesari", "")
    nr_accesari = f"""
    <div>numarul de accesari de cand a fost pornit serverul(in sesiunea curenta): {len(accesari)}</div>
    """ if "nr" in param_accesari else ""
    if "detalii" in param_accesari:
        detalii = f"""
            <div>
                <ul>
                    <li>{"</li><li>".join(acc.calculeaza_data() for acc in accesari_afisate)}
                    </li>
                </ul>
            </div>
        """
    else:
        detalii = ""

    tabel = []
    table_param = []
    for x in request.GET.getlist("tabel", ""):
        table_param.extend(x.split(","))

    if len(table_param) != 0:
        if "tot" in table_param:
            table_param = ("id", "url", "pg", "data")
        else:
            table_param = [x for x in ("id", "url", "pg", "data") if x in table_param] # pastram ordinea

        tabel.append("""
            <style>table, td, th { border: 1px solid black; border-collapse: collapse;}</style><table><tr>
        """)
        for p in table_param:
            tabel.append(f"<th>{p}</th>")
        tabel.append("</tr>")
        for acc in accesari_afisate:
            tabel.append("<tr>")
            for p in table_param:
                tabel.append("<td>")
                if p == "id":
                    tabel.append(str(acc.get_id()))
                elif p == "url":
                    tabel.append(acc.string_url())
                elif p == "pg":
                    tabel.append(acc.pagina())
                elif p == "data":
                    tabel.append(acc.calculeaza_data())
                tabel.append("</td>")
            tabel.append("</tr>")
        tabel.append("</table>")

    nume_accesari = [acc.pagina() for acc in accesari]
    dictionar_accesari = {}
    for pagina in set(nume_accesari):
        dictionar_accesari.update({nume_accesari.count(pagina): pagina})
    
    return HttpResponse(
        f"""
            <html><body>
                <title>log</title>
                <h1>log</h1>
                <div>
                    <ul>
                        <li>{"</li><li>".join(f"{acc.get_id()}. {acc.string_url()}" for acc in accesari_afisate)}
                        </li>
                    </ul>
                </div>
                <p>{eroare}<p>
                {nr_accesari}
                {detalii}
                <div>
                    <h2>Parametri</h2>
                    <ul>
                        <li>nr parametri: {len(request.GET)}</li>
                        <li>nume parametri: {", ".join(key for key in request.GET.keys())}</li>
                    </ul>
                </div>
                <div>{"".join(tabel)}</div>
                <div>
                    <h2>Pagina accesată cel mai mult și pagina accesată cel mai puțin</h2>
                    <p>Paginile care nu au fost accesate deloc nu se iau în calcul</p>
                    <ul>
                        <li>Pagina accesată cel mai puțin: {dictionar_accesari[min(dictionar_accesari.keys())]}</li>
                        <li>Pagina accesată cel mai mult: {dictionar_accesari[max(dictionar_accesari.keys())]}</li>
                    </ul>
                </div>
            </body></html>
        """
    )

def istoric(request):
    actualizeaza_accesari(request)
    return HttpResponse(
        f"""
            <html><body>
                <title>Istoric</title>
                <h1>Istoric</h1>
                <p>Aici sunt scrise informații despre istoricul aplicației</p>
            </body></html>
        """
    )

def despre(request):
    actualizeaza_accesari(request)
    return HttpResponse(
        f"""
            <html><body>
                <title>Despre</title>
                <h1>Despre</h1>
                <p>Aici sunt scrise informații despre aplicație</p>
            </body></html>
        """
    )

def pagina_accesare(request, id):
    actualizeaza_accesari(request)
    try:
        acc = accesari[int(id) - 1]
        response = f"""
            <p>Informații despre accesarea cu id-ul {id}</p>
            <ul>
                <li>id: {acc.get_id()}</li>
                <li>url: {acc.string_url()}</li>
                <li>pg: {acc.pagina()}</li>
                <li>data: {acc.calculeaza_data()}</li>
            </ul>
        """
    except IndexError:
        response = f"<p>EROARE: nu există accesarea cu id-ul {id}</p>"

    return HttpResponse(
        f"""
            <html><body>
                <title>Pagină accesare</title>
                <h1>Pagină accesare</h1>
                {response}
            </body></html>
        """
    )


id_cereri_numere = 1
suma_numere = 0
def aduna_numere(request, nr):
    global id_cereri_numere, suma_numere

    i = len(nr) - 1
    while i >= 0 and "0" <= nr[i] <= "9":
        i -= 1
    id_cereri_numere += 1
    if i == len(nr) - 1:
        response = "eroare"
    else:
        suma_numere += int(nr[i+1:])
        response = f"numar cereri: {id_cereri_numere} suma numere: {suma_numere}"

    return HttpResponse(
        f"""
            <html><body>
                <title>aduna_numere</title>
                <h1>aduna_numere</h1>
                <p>{response}</p>
            </body></html>
        """
    )

def afiseaza_liste(request):
    lista = [(key, request.GET.getlist(key)) for key in request.GET.keys()]

    response = []
    
    for elem in lista:
        response.append(f"<p>{elem[0]}:</p><ul>")
        for val in elem[1]:
            response.append(f"<li>{val}</li>")
        response.append("</ul>")

    return HttpResponse(
        f"""
            <html><body>
                <title>afiseaza_liste</title>
                <h1>afiseaza_liste</h1>
                <div>{"".join(response)}</div>
            </body></html>
        """
    )

nume = 0
def numara_nume(request):
    global nume
    nume += 1

    return HttpResponse(
        f"""
            <html><body>
                <title>numara_nume</title>
                <h1>numara_nume</h1>
                <div>{nume}</div>
            </body></html>
        """
    )

def cauta_subsir(request, s):

    return HttpResponse(
        f"""
            <html><body>
                <title>cauta_subsir</title>
                <h1>cauta_subsir</h1>
                <div>{len(s)}</div>
            </body></html>
        """
    )

def afisare_categorii(request):

    nrPagina = request.GET.get("pagina", 1)

    categorii = Categorie.objects.all()
    paginator = Paginator(categorii, 3) # 10
    mesajEroare = None

    try:
        obPagina = paginator.page(nrPagina)
    except EmptyPage:
        obPagina = None
        mesajEroare = "Nu mai sunt categorii"
    except PageNotAnInteger:
        obPagina = None
        mesajEroare = "PageNotAnInteger"

    return render(request, 'aplicatie_magazin/categorii.html',
        {
            "pagina": obPagina,
            "eroare": mesajEroare,
        }
    )

def operatii(request):
    d = {
        "lista": [
            {
                "a":10,
                "b":20,
                "operatie":"suma"
            },
            {
                "a":40,
                "b":20,
                "operatie":"diferenta"
            },
            {
                "a":25,
                "b":30,
                "operatie":"suma"
            },
            {
                "a":40,
                "b":30,
                "operatie":"diferenta"
            },
            {
                "a":100,
                "b":50,
                "operatie":"diferenta"
            }
        ]
    }

    return render(request, 'aplicatie_magazin/operatii.html',
        {
            "d": d,
        }
    )

def afisare(request):
    # Exemplu de mesaje
    messages.debug(request, "Acesta este un mesaj de depanare. :( ")
    messages.info(request, "Acesta este un mesaj informativ. :) ")
    messages.success(request, "Actiunea a avut succes! :D ")
    messages.warning(request, "Acesta este un avertisment. :| ")
    messages.error(request, "A aparut o eroare! >:((  ")
   
    return render(request, 'aplicatie_magazin/un_template.html')

def redirectionare(request):
    messages.success(request, "Ai fost redirectionat!")
    return redirect('index') #home
