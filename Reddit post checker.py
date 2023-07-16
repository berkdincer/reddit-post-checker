import time
import pickle
import praw

reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent='',
    password='',
    username=''
)

subredditAdlari = []
dataicerikleri = []
kullanicilar = []
tekliListe = []
girisKontrolcu = 0
cikisyapildi = 0
tekliTarama = 0

def dataYukle():
    global subredditAdlari 
    global dataicerikleri  
    global kullanicilar
    kullanicilar = pickle.load(open("kullanicilar.pickle", "rb"))
    subredditAdlari = pickle.load(open("subredditAdlari.pickle", "rb"))
    dataicerikleri = pickle.load(open("postlar.pickle", "rb"))
dataYukle()

def Tarama():
    global tekliListe
    global tekliTarama
    global cikisyapildi
    global suankiZaman
    global subredditAdlari
    global dataicerikleri
    global subredditq
    global Sayi
    print("Tarama işleminiz başlıyor.")
    time.sleep(3)
    while cikisyapildi == 0:
        if tekliTarama == 0:
            gecenZaman = time.time()
            if gecenZaman - suankiZaman >= 180:
                soru = input("Zamanlayıcı üç dakikadır çalışıyor.\nİşleminize devam etmek ister misiniz ?\n").lower()
                if soru == "evet":
                    print("Kod çalışmaya devam ediyor.")
                    suankiZaman = time.time()
                else:
                    print("Başlangıç sayfasına geri dönülüyor.")
                    break
            for subreddit_ad in subredditAdlari:
                subreddit = reddit.subreddit(subreddit_ad)
                for postlar in subreddit.new(limit= Sayi):
                    yeni_post = {"Post Başlığı": postlar.title, "Post İçeriği": postlar.selftext, "Post Skoru": postlar.score, "Postu Yayınlayan": postlar.author.name}
                    if yeni_post not in dataicerikleri:
                        print("YENİ BİR POST/GELİŞME VAR!")
                        print(yeni_post)
                        dataicerikleri.append(yeni_post)
                        pickle.dump(dataicerikleri, open("postlar.pickle", "wb"))

        else:
            gecenZaman = time.time()
            if gecenZaman - suankiZaman >= 180:
                soru = input("Zamanlayıcı üç dakikadır çalışıyor.\nİşleminize devam etmek ister misiniz ?\n").lower()
                if soru == "evet":
                    print("Kod çalışmaya devam ediyor.")
                    suankiZaman = time.time()
                else:
                    print("Başlangıç sayfasına geri dönülüyor.")
                    break
            for subreddit_ad in tekliListe:
                subreddit = reddit.subreddit(subreddit_ad)
                for postlar in subreddit.new(limit= Sayi):
                    yeni_post = {"Post Başlığı": postlar.title, "Post İçeriği": postlar.selftext, "Post Skoru": postlar.score, "Postu Yayınlayan": postlar.author.name}
                    if yeni_post not in dataicerikleri:
                        print(yeni_post)
                        dataicerikleri.append(yeni_post)
                        pickle.dump(dataicerikleri, open("postlar.pickle", "wb"))
        
def CokluTarama():
    global tekliTarama
    global subredditq
    global tekliListe
    global suankiZaman
    if tekliTarama == 1:
        for i in tekliListe:
            subreddit = reddit.subreddit(i)
            post = 1
            print("Şu an görüntülenen subreddit:", i, "\n")
            print("Görüntülenen post sayısı:", Sayi, "\n")
            for i in subreddit.new(limit=Sayi):
                print(post, " - ", "Post başlığı: ", i.title)
                print("Postun içeriği: ", i.selftext)
                print("Post Skoru: ", i.score)
                print("Postu yayınlayan: ", i.author.name, "\n")
                dataicerikleri.append({"Post Başlığı": i.title, "Post İçeriği": i.selftext, "Post Skoru": i.score, "Postu Yayınlayan": i.author.name})
                pickle.dump(dataicerikleri, open("postlar.pickle", "wb"))
                post += 1
                suankiZaman = time.time()
    else:
        for i in subredditAdlari:
            subreddit = reddit.subreddit(i)
            post = 1
            print("Şu an görüntülenen subreddit:", i, "\n")
            print("Görüntülenen post sayısı:", Sayi, "\n")
            for i in subreddit.new(limit=Sayi):
                print(post, " - ", "Post başlığı: ", i.title)
                print("Postun içeriği: ", i.selftext)
                print("Post Skoru: ", i.score)
                print("Postu yayınlayan: ", i.author.name, "\n")
                dataicerikleri.append({"Post Başlığı": i.title, "Post İçeriği": i.selftext, "Post Skoru": i.score, "Postu Yayınlayan": i.author.name})
                pickle.dump(dataicerikleri, open("postlar.pickle", "wb"))
                post += 1
                suankiZaman = time.time()
    post = 1
    time.sleep(2)
    Tarama()

def kodCalisma():
    global subredditAdlari
    global dataicerikleri
    global Sayi
    global tekliListe
    global tekliTarama
    global suankiZaman
    while True:
        print("1- Post aranacak/kayıtlı subreddit listesini görüntüle ")
        print("2- Mevcut post verilerini görüntüle")
        print("3- Subreddit ekle") 
        print("4- Mevcut verileri sıfırla")
        print("5- Mevcut subredditlerde tarama yap")
        print("6- Çıkış")
        soru1 = int(input("İşlemlerden hangisini yapmak istersiniz?\n"))
        if soru1 == 1:
            print("Mevcut subredditler: {}".format(subredditAdlari))
        elif soru1 == 2:
            print("Mevcut postlar görüntüleniyor.")
            time.sleep(1)
            for i in dataicerikleri:
                print("Post Başlığı: {}".format(i["Post Başlığı"]))
                print("Post İçeriği: {}".format(i["Post İçeriği"]))
                print("Postu Yayınlayan: {}".format(i["Postu Yayınlayan"]))
                print("Post Skoru: {}\n".format(i["Post Skoru"]))
        elif soru1 == 3:
            global subredditq
            while True:
                subredditq = input("Kullanmak istediğiniz subredditin ismini girin (q subreddit eklemeden çıkabilirsiniz):\n")
                if subredditq == "q":
                    print("Subreddit ekleme menüsünden çıkış yapılıyor.")
                    break
                else:
                    if subredditq not in subredditAdlari:
                        subredditAdlari.append(subredditq)
                        pickle.dump(subredditAdlari, open("subredditAdlari.pickle", "wb"))
                    else:
                        print("Bu subreddit adı zaten listede var.")
        elif soru1 == 4:
            subredditAdlari.clear()
            dataicerikleri.clear()
            pickle.dump(dataicerikleri, open("postlar.pickle", "wb"))
            pickle.dump(subredditAdlari, open("subredditAdlari.pickle", "wb"))
            print("Subreddit dataları ve post dataları sıfırlandı.")
            print("Mevcut data listesi Postlar:{}\nSubreddit Adları{}".format(dataicerikleri, subredditAdlari))
            time.sleep(2)
            KullaniciSifirlamaSorusu = input("Kullanıcı listesini de sıfırlamak ister misiniz ?\n").lower()
            if KullaniciSifirlamaSorusu == "evet":
                kullanicilar.clear()
                pickle.dump(kullanicilar, open("kullanicilar.pickle", "wb"))
                print("Kullanıcı verileri sıfırlandı.")
                print("Mevcut data listesi Kullanıcılar {}".format(dataicerikleri, subredditAdlari))
                time.sleep(1)
            else:
                kodCalisma()
        elif soru1 == 5:
            while True:
                print("Subreddit listesi {}".format(subredditAdlari))
                TekliKontrol = input("Subreddit listesinde işlem yapmak istediklerinizi seçiniz\n(Hepsini seçmek için /all yazmalısınız.)\nÇıkış yapmak için q tuşuna basınız\n")
                if TekliKontrol not in tekliListe:
                    if TekliKontrol == "/all":
                        Sayi = int(input("Taramak istediğiniz post sayısını giriniz."))
                        print("{} Listesindeki subredditlerde olan son {} post görüntülenecek.".format(subredditAdlari,Sayi))
                        time.sleep(1)
                        suankiZaman = time.time()
                        tekliTarama = 0
                        CokluTarama()
                        break        
                    elif TekliKontrol == "q":
                        Sayi = int(input("Taramak istediğiniz post sayısını giriniz."))
                        print("{} Listesindeki subredditlerde olan son {} post görüntülenecek.".format(tekliListe,Sayi))
                        suankiZaman = time.time()
                        tekliTarama = 1
                        CokluTarama()
                        break
                else:
                    print("Bu subreddit zaten eklendi.")
                if TekliKontrol not in subredditAdlari:
                    print("Bu subreddit listenizde bulunmuyor")
                else:
                    tekliListe.append(TekliKontrol)
                    print("{} Başarıyla eklendi.".format(TekliKontrol))
                    print("Güncel liste {}".format(tekliListe))
        elif soru1 == 6:
            global cikisyapildi
            cikisyapildi = 1
            for i in range(3):
                i +=1
                if i==1:
                    print("Çıkış yapılıyor.")
                    time.sleep(1)
                if i==2:
                    print("Çıkış yapılıyor..")
                    time.sleep(1)
                if i==3:
                    print("Çıkış yapılıyor...")
                    time.sleep(1)
            break

while girisKontrolcu == 0:
    girissorusu = input("1- Giriş yapma \n2- Hesap oluşturma\n")
    if girissorusu == "1":
        kullanici = input("Kullanıcı adı giriniz:\n")
        parola = input("Parola giriniz:\n")
        for i in kullanicilar:
            if kullanici == i["kullanici"] and parola == i["parola"]:
                girisKontrolcu = 1
                print("Başarıyla giriş yapıldı")
        if girisKontrolcu == 0:
            print("Kullanıcı adı ya da parola hatalı.")

    if girissorusu == "2":
        kayitolkullanici = input("Kullanıcı adı giriniz:\n")
        kayitolparola = input("Parola giriniz:\n")
        kullanici_var = False
        for i in kullanicilar:
            if i["kullanici"] == kayitolkullanici:
                kullanici_var = True
                break
        if kullanici_var:
            print("Bu kullanıcı adı ile hesap açılmış")
        else:
            kullanicilar.append({"kullanici": kayitolkullanici, "parola": kayitolparola})
            print("Üyeliğiniz başarıyla oluşturuldu.\nKullanıcı adı: {}\nParola: {}".format(kayitolkullanici, kayitolparola))
            pickle.dump(kullanicilar, open("kullanicilar.pickle", "wb"))
            girisKontrolcu = 1
kodCalisma()