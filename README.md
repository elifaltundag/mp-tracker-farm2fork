# 🔬 Mikroplastik Takip Sistemi

TÜBİTAK 1001 "Çiftlikten Çatala - Küçük Menderes Havzası Tarım Toprakları ve Bitkisel Ürünlerde Mikroplastik Kirliliğinin Araştırılması" projesi kapsamında geliştirilmiş veri yönetim sistemi MVP yazılımı.

## 📋 Proje Hakkında

Bu sistem, tarım topraklarında ve bitkisel ürünlerdeki mikroplastik kirliliği verilerinin sistematik olarak kaydedilmesi, yönetilmesi ve analiz edilmesi için geliştirilmiştir.

**Proje No:** 123Y303

**Özellikler:**
- 🌐 Web tabanlı veri giriş arayüzü
- 🔌 REST API ile veri erişimi
- 🗄️ MongoDB ile veri saklama
- 📊 Swagger/OpenAPI dokümantasyonu
- 🐳 Docker ile kolay kurulum

---

## Hızlı Başlangıç [Yerel Kurulum]

### Gereksinimler

- Docker Desktop
- Docker Compose

### Kurulum ve Çalıştırma

```bash
# Projeyi klonlayın
git clone <repository-url>
cd mp-tracker-farm2fork

# Tüm servisleri başlatın
docker-compose up -d
```

### Erişim

Sistemin başlaması 30 saniye kadar sürebilir. Ardından:

- **Web Arayüzü:** Tarayıcınızda `localhost:3000` adresini açın
- **API Dokümantasyonu:** Tarayıcınızda `localhost:8000/docs` adresini açın
- **MongoDB:** MongoDB Compass ile `mongodb://localhost:27017` bağlantısı

### Durdurma

```bash
docker-compose down
```

---

## 📊 Veri Modeli

Sistem aşağıdaki veri kategorilerini yönetir:

- **Örnekleme Bilgileri:** Örnek numarası, tarih, tür
- **Konum:** Yerleşim yeri, GPS koordinatları, jeoloji
- **Tarım:** Sulama, ürün yetiştirme, plastik kullanımı
- **Fizikokimyasal:** pH, EC, organik madde
- **Mikroplastik Analiz:** Tür, sayı, renk, morfoloji, boyut

---

## 📚 API Kullanımı

### Örnek İstekler

**Yeni örnek oluştur:**
```bash
curl -X POST http://localhost:8000/api/v1/samples \
  -H "Content-Type: application/json" \
  -d '{
    "ornek_no": "1",
    "ornekleme_tarihi": "2024-04-28",
    "ornek_turu": "Standart Örnek",
    "konum": {
      "yerlesim_yeri": "Hasköy",
      "koordinatlar": {
        "enlem": 38.127516,
        "boylam": 27.509202
      }
    }
  }'
```

**Örnekleri listele:**
```bash
curl http://localhost:8000/api/v1/samples
```

Detaylı API dokümantasyonu için Swagger UI kullanın.

---

## 🛠️ Geliştirme

### Proje Yapısı

```
├── backend/          # FastAPI uygulaması
│   ├── app/
│   │   ├── models/   # Pydantic modelleri
│   │   ├── routes/   # API endpoints
│   │   ├── services/ # İş mantığı
│   │   └── repositories/ # Veri erişimi
│   └── tests/        # Test dosyaları
├── frontend/         # Web arayüzü
│   ├── css/
│   ├── js/
│   └── index.html
└── docker-compose.yml
```

### Kod Kalitesi

```bash
# Backend formatla
docker exec -it microplastic_api black app/

# Testleri çalıştır
docker exec -it microplastic_api pytest tests/
```

---

## 🔧 Sorun Giderme

**Docker container'ları kontrol et:**
```bash
docker-compose ps
```

**Logları görüntüle:**
```bash
docker-compose logs -f api
docker-compose logs -f mongodb
docker-compose logs -f frontend
```

**Veritabanını sıfırla:**
```bash
docker-compose down -v
docker-compose up -d
```

---

## 📈 Proje Durumu

### ✅ Tamamlanan Aşamalar
- ✅ Sistem mimarisi ve teknoloji seçimi
- ✅ Backend altyapısı (FastAPI + MongoDB)
- ✅ Temel veri modelleri ve API
- ✅ Web arayüzü (veri giriş/listeleme/düzenleme/silme)
- ✅ Docker yapılandırması
- ✅ Temel dokümantasyon

### 🔄 Devam Eden Aşamalar
- 🔄 Ek veri alanları (tarım, fizikokimyasal, MP analiz)
- 🔄 Excel içe/dışa aktarma

### ⏳ Planlanan Aşamalar
- ⏳ Test yazımı
- ⏳ Detaylı kullanım kılavuzu
- ⏳ Kullanıcı yönetimi ve yetkilendirme
- ⏳ Harita görselleştirme
- ⏳ Veri analizi ve raporlama