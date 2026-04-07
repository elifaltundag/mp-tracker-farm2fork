"""
Uygulama yapılandırması ve sabit değerler.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Uygulama ayarları."""

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "microplastic_db"

    # API
    API_VERSION: str = "v1"
    API_TITLE: str = "Mikroplastik Takip Sistemi API"
    API_DESCRIPTION: str = "Mikroplastik Veri Yönetim Sistemi"

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Settings instance
settings = Settings()


# Türkçe mesajlar (i18n hazırlığı)
MESSAGES = {
    "sample_created": "Örnek başarıyla oluşturuldu",
    "sample_updated": "Örnek başarıyla güncellendi",
    "sample_deleted": "Örnek başarıyla silindi",
    "sample_not_found": "Örnek bulunamadı",
    "invalid_id": "Geçersiz ID formatı",
    "database_error": "Veritabanı hatası",
    "validation_error": "Veri doğrulama hatası",
}


# Enum değerleri
ORNEK_TURLERI = ["Standart Örnek", "Referans Örnek"]
SULAMA_TURLERI = ["Salma Sulama", "Damlama Sulama", "Yağmurlama Sulama", "Arık Sulama"]
SULAMA_KAYNAKLARI = ["Nehir", "Yeraltı Suyu", "Baraj Sulaması"]
JEOLOJI_TURLERI = [
    "Alüvyon",
    "Alüvyon yelpazesi",
    "Andezit",
    "Kireçtaşı",
    "Konglomera",
    "Mermer",
    "Metamorfik",
    "Ofiyolit",
    "Şist"
]
ALINAN_ORNEK_TURLERI = ["Toprak", "Su", "Gübre", "Bitki"]
PLASTIK_KIRLILIK_SEVIYELERI = ["Yok", "Düşük", "Yüksek"]
URUN_YETISME_TURLERI = ["Açıkta", "Sera"]
