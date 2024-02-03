ÖZET<br>
X-ray cihazlarında nesne tespiti zaman alıcı ve hataya müsait bir süreçtir.
Bu çalışmada bunu iyileştirmek amacıyla yapay zekâ kullanımı incelenmektedir.
Çalışmanın amacı, YOLOv5 kullanılarak eğitilen bir model yardımıyla X-ray cihazlarına tehlikeli
maddeleri tespit etme yeteneği kazandırmaktır. Bu teknolojilerin kullanımı sayesinde havaalanları,
kamu binaları gibi kritik noktalarda zaman kaybı azaltılabilir ve güvenlik kontrolleri daha etkin
hale getirilebilir. Çalışmada operatörlerin daha iyi müdahale yapabilmesine destek olacak bir
uygulama geliştirilmesi amaçlanmaktadır. Bu uygulamada YOLOv5s modeli, Flask ve OpenCV kullanılmıştır.

GİRİŞ<br>
X-ray cihazları, günümüzde güvenlik amacıyla havaalanları, kamu binaları, sınır kontrol noktaları gibi
yerlerde yaygın bir şekilde kullanılmaktadır fakat bazı dezavantajları da bulunmaktadır. Bu cihazlarda
yapay zeka kullanımı sayesinde operatörlere destek olunabilir ve güvenlik artırılabilir.

YÖNTEM<br>
Model eğitilirken YOLOv5s kullanılmıştır. Bunun ana sebebi uygulamanın gerçek zamanlı çalışmasının
amaçlanmasıdır. Eğitim için ana veri seti olarak PIDray ve ondaki ortak sınıflara yardımcı olması için
CLCXray veri seti kullanılmıştır. Model OpenCV ve Flask aracılığıyla bir web uygulamasında kullanılmıştır.

BULGULAR<br>
Eğitilen model ile baton, hammer, scissors, bullet ve knife sınıflarında daha düşük bir mAP değeri elde
edilmiştir. Kolay, Zor ve Gizli test sınıflarında ortalama mAP değeri için 0.691 bulunmuştur. Bu sonuçlar
PIDray çalışmasında farklı omurgalarla yapılan testlerin sonuçlarından daha başarılıdır.

EKLER<br>
Veri Setleri<br>
PIDray: https://github.com/bywang2018/security-dataset
CLCXray: https://github.com/GreysonPhoenix/CLCXray

Model eğitilirken bu iki veri setinden faydalanılmıştır. Bazı şeyler telif veya hak ihlali gibi
sıkıntıların yaşanmaması için eklenmemiştir. requirements.txt dosyasını kurunuz.
