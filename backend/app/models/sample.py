"""
Örnek (Sample) veri modelleri.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class Koordinatlar(BaseModel):
    """GPS koordinatları."""
    enlem: float = Field(..., ge=-90, le=90, description="Enlem (latitude)")
    boylam: float = Field(..., ge=-180, le=180, description="Boylam (longitude)")

    class Config:
        json_schema_extra = {
            "example": {
                "enlem": 38.127516,
                "boylam": 27.509202
            }
        }


class Konum(BaseModel):
    """Örnekleme konum bilgileri."""
    yerlesim_yeri: str = Field(..., description="En yakın yerleşim yeri")
    ozel_aciklama: Optional[str] = Field(None, description="Saha notları")
    koordinatlar: Optional[Koordinatlar] = None
    yukseklik_m: Optional[float] = Field(None, description="Deniz seviyesinden yükseklik (metre)")
    egim_yuzde: Optional[float] = Field(None, description="Saha eğimi (%)")
    jeoloji: Optional[str] = Field(None, description="Jeolojik yapı")


class Tarim(BaseModel):
    """Tarımsal bilgiler."""
    sulama_turu: Optional[str] = Field(None, description="Sulama türü")
    sulama_kaynagi: Optional[str] = Field(None, description="Sulama kaynağı")
    sulama_sikligi_gun: Optional[int] = Field(None, description="Sulama sıklığı (gün)")
    urun_yetisme_turu: Optional[str] = Field(None, description="Ürün yetiştirme türü")
    plastik_malc: Optional[bool] = Field(None, description="Plastik malç kullanımı")
    plastik_kirlilik_gozlemi: Optional[str] = Field(None, description="Plastik kirlilik gözlemi")
    olasi_mp_kaynaklari: Optional[List[str]] = Field(None, description="Olası MP kaynakları")
    mp_kaynagina_mesafe_m: Optional[float] = Field(None, description="En yakın MP kaynağına mesafe (m)")


class Ornek(BaseModel):
    """Alınan örnek bilgileri."""
    tur: Optional[str] = Field(None, description="Örnek türü (Toprak, Su, Gübre, Bitki)")
    ozellik: Optional[str] = Field(None, description="Derinlik veya bitki türü")


class Fizikokimyasal(BaseModel):
    """Fizikokimyasal analiz sonuçları."""
    ph: Optional[float] = Field(None, description="pH değeri")
    ec: Optional[float] = Field(None, description="Elektriksel iletkenlik (µS/cm)")
    organik_madde: Optional[float] = Field(None, description="Organik madde (% Kuru Madde)")
    seluloz: Optional[float] = Field(None, description="Selüloz (% OM)")
    hemiseluloz: Optional[float] = Field(None, description="Hemiselüloz (% OM)")
    lignin: Optional[float] = Field(None, description="Lignin (% OM)")
    ekstraktif: Optional[float] = Field(None, description="Ekstraktif (% OM)")


class MPSayi(BaseModel):
    """Mikroplastik sayısı (adet/kg)."""
    toplam: Optional[int] = None
    pet: Optional[int] = None
    pp: Optional[int] = None
    pe: Optional[int] = None
    ps: Optional[int] = None
    pvc: Optional[int] = None
    arac_lastigi: Optional[int] = None
    pa: Optional[int] = None
    pc: Optional[int] = None
    pom: Optional[int] = None
    diger: Optional[int] = None


class MPRenk(BaseModel):
    """Mikroplastik renk dağılımı (adet/kg)."""
    renksiz_seffaf: Optional[int] = None
    beyaz: Optional[int] = None
    kirmizi: Optional[int] = None
    mavi: Optional[int] = None
    yesil: Optional[int] = None
    sari: Optional[int] = None
    diger: Optional[int] = None


class MPMorfoloji(BaseModel):
    """Mikroplastik morfoloji (adet/kg)."""
    fragman: Optional[int] = None
    film: Optional[int] = None
    lif: Optional[int] = None
    granul_pellet: Optional[int] = None
    kopuk: Optional[int] = None
    boncuk: Optional[int] = None
    yonga_pul: Optional[int] = None


class MPBoyut(BaseModel):
    """Mikroplastik boyut bilgileri."""
    cap_kategori: Optional[str] = Field(
        None,
        description="Çap kategorisi (<25, 25-100, 100-250, 250-500, 500-1000, 1000-2000, 2000-5000 µm)"
    )
    cap_min: Optional[float] = Field(None, description="Minimum çap (µm)")
    cap_max: Optional[float] = Field(None, description="Maksimum çap (µm)")


class MPAnaliz(BaseModel):
    """Mikroplastik analiz sonuçları."""
    yontem: Optional[str] = Field(None, description="Analiz yöntemi")
    sayi: Optional[MPSayi] = None
    renk: Optional[MPRenk] = None
    morfoloji: Optional[MPMorfoloji] = None
    boyut: Optional[MPBoyut] = None


# Request/Response Modelleri

class SampleCreate(BaseModel):
    """Yeni örnek oluşturma modeli."""
    ornek_no: str = Field(..., description="Benzersiz örnek numarası")
    ornekleme_tarihi: date = Field(..., description="Örnekleme tarihi")
    ornek_turu: str = Field(..., description="Örnek türü (Standart Örnek / Referans Örnek)")
    konum: Konum
    tarim: Optional[Tarim] = None
    ornek: Optional[Ornek] = None
    fizikokimyasal: Optional[Fizikokimyasal] = None
    mp_analiz: Optional[MPAnaliz] = None

    class Config:
        json_schema_extra = {
            "example": {
                "ornek_no": "1",
                "ornekleme_tarihi": "2024-04-28",
                "ornek_turu": "Standart Örnek",
                "konum": {
                    "yerlesim_yeri": "Hasköy",
                    "koordinatlar": {
                        "enlem": 38.127516,
                        "boylam": 27.509202
                    },
                    "jeoloji": "Alüvyon"
                },
                "tarim": {
                    "sulama_turu": "Damlama Sulama",
                    "plastik_malc": True
                }
            }
        }


class SampleUpdate(BaseModel):
    """Örnek güncelleme modeli (tüm alanlar opsiyonel)."""
    ornek_no: Optional[str] = None
    ornekleme_tarihi: Optional[date] = None
    ornek_turu: Optional[str] = None
    konum: Optional[Konum] = None
    tarim: Optional[Tarim] = None
    ornek: Optional[Ornek] = None
    fizikokimyasal: Optional[Fizikokimyasal] = None
    mp_analiz: Optional[MPAnaliz] = None


class SampleResponse(SampleCreate):
    """Örnek yanıt modeli."""
    id: str = Field(..., description="MongoDB ObjectId (string)")
    olusturma_tarihi: Optional[datetime] = None
    guncelleme_tarihi: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "65a1b2c3d4e5f6789",
                "ornek_no": "1",
                "ornekleme_tarihi": "2024-04-28",
                "ornek_turu": "Standart Örnek",
                "konum": {
                    "yerlesim_yeri": "Hasköy",
                    "koordinatlar": {
                        "enlem": 38.127516,
                        "boylam": 27.509202
                    }
                },
                "olusturma_tarihi": "2024-01-25T10:00:00",
                "guncelleme_tarihi": "2024-01-25T10:00:00"
            }
        }


class SampleListResponse(BaseModel):
    """Örnek listesi yanıt modeli."""
    data: List[SampleResponse]
    total: int = Field(..., description="Toplam kayıt sayısı")
    page: int = Field(..., description="Mevcut sayfa numarası")
    page_size: int = Field(..., description="Sayfa başına kayıt sayısı")
    total_pages: int = Field(..., description="Toplam sayfa sayısı")
