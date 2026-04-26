# NexusRSA: End-to-End Encrypted Messaging System (E2EE) 🛡️💬

NexusRSA, uçtan uca şifreleme (E2EE) prensibiyle çalışan, gizliliğin matematiksel olarak garanti altına alındığı modern bir mesajlaşma uygulamasıdır. Bu proje, **Zero-Knowledge (Sıfır Bilgi)** mimarisini kullanarak sunucunun bile mesaj içeriğini okuyamadığı bir yapı sunar.

## 🚀 Öne Çıkan Özellikler

- **Asimetrik Şifreleme:** Mesajlar 2048-bit RSA-OAEP algoritması ile şifrelenir.
- **Zero-Knowledge Architecture:** Özel anahtarlar (Private Keys) asla sunucuya gönderilmez; yalnızca kullanıcının yerel cihazında (`localStorage`) saklanır.
- **Şeffaf Kripto Motoru:** Uygulama içindeki gerçek zamanlı terminal sayesinde şifreleme, deşifreleme ve anahtar import süreçleri adım adım izlenebilir.
- **Single Page Application (SPA):** Sayfa yenilenmeden akıcı bir kullanıcı deneyimi sunan modern web mimarisi.
- **Güvenli Kimlik Doğrulama:** Şifreler sunucuda güvenli hash algoritmalarıyla saklanır.

## 🛠️ Teknoloji Yığını

- **Backend:** Python (Flask)
- **Frontend:** Vanilla JavaScript (Web Crypto API - `window.crypto.subtle`)
- **Veritabanı:** SQLite3
- **Stil:** CSS3 (Custom Responsive Design)

## 🔐 Güvenlik Modeli (Nasıl Çalışır?)

1. **Anahtar Üretimi:** Kayıt sırasında tarayıcıda bir RSA anahtar çifti üretilir. Public Key sunucuya gönderilir, Private Key cihazda mühürlü kalır.
2. **Şifreleme:** Mesaj gönderilmeden önce alıcının Public Key'i sunucudan çekilir ve mesaj tarayıcı seviyesinde şifrelenir.
3. **İletim:** Sunucuya giden veri sadece anlamsız bir Base64 bloğudur (Ciphertext).
4. **Deşifre:** Alıcı, mesajı sadece kendi Private Key'ini kullanarak çözebilir.

## 💻 Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için:

1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install flask flask-cors
   ```

2. Sunucuyu başlatın:
   ```bash
   python app.py
   ```

3. Tarayıcınızda şu adrese gidin:
   ```
   http://127.0.0.1:5000
   ```


## 📜 Lisans
Bu proje eğitim amaçlı geliştirilmiştir ve açık kaynak kodludur.
