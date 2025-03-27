# FLSim

A tool for simulation and analysis of top FL client selection algorithms.

Aklımda şöyle bi sistem var:
2 boyutlu linear regression'ı simüle etcez. Her client'ın farklı datasetleri olcak, yani hepsi farklı updateler göndercek, sonra client selection algorithm'lere göre daha \
"kaliteli" olanlar öne çıkcak (umarım).
Her round'da current weightler (ax+b nin a ve b'si) clientlara gönderilcek, clientlar update'leri hesaplayıp geri göndercek. Central server da update'leri client selection \
algoritmalarına göndercek, onların verdiği bilgiye göre bi sonraki roundda farklı clientlar seçilcek. Central server bi de gelen updateleri aggregate etcek (ortalamalarını \
felan alabilir en basitinden). Sonraki roundda da işte aggregate edilmiş weightleri (yeni a ve b'yi) göndercek.
2 boyutlu linear regression seçmemiz şu yüzden bence baya hoş olur:
    basit
    görsel olarak rahat gösteririz

TO DO:
fl_simulator dosyasının altına server.py açılıp yazılmalı
fl_simulator dosyasının altına client.py açılıp yazılmalı
experiments diye bi klasör açılmalı. İçine fl_simulator'daki dosyalar kullanılarak bi experiment runlayıp sonuçları kaydetcek bişey tasarlanmalı
    bence ilk adımda bu experimentlar CLI'dan ilerlesin. Zaten CLI'dan yaptık mı bizim iş bitiyo aslında, UI kısmı da nice to have olur bence. Sonuçta makalede simulasyon \
    vidyosu falan koymicaz.
Data generator ve syntetic data klasörleri silinebilir. Şu anda csv üretiyo, onun yerine direk clientların içinde datayı üretirsek csv importlamakla felan uğraşmayız daha \
rahat olur bence.
OPTIONAL: visualization diye bi klasör açılmalı. Ona da visualization şeysini yapcaz işte.

TO RUN EXPRERIMENT 1

Go to the FLSim directory

Run "python -m experiments.experiment_1"