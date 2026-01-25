"""
MongoDB bağlantı yönetimi.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from app.config import settings


class Database:
    """MongoDB bağlantı yöneticisi."""

    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect(cls):
        """Veritabanına bağlan."""
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        cls.db = cls.client[settings.DATABASE_NAME]

        # İndeksleri oluştur
        await cls.create_indexes()

        print(f"✅ MongoDB'ye bağlanıldı: {settings.DATABASE_NAME}")

    @classmethod
    async def disconnect(cls):
        """Veritabanı bağlantısını kapat."""
        if cls.client:
            cls.client.close()
            print("❌ MongoDB bağlantısı kapatıldı")

    @classmethod
    async def create_indexes(cls):
        """Koleksiyon indekslerini oluştur."""
        if cls.db is None:
            return

        samples_collection = cls.db.samples

        # Coğrafi indeks (2dsphere)
        await samples_collection.create_index([("konum.koordinatlar", "2dsphere")])

        # Sık kullanılan filtreler için indeksler
        await samples_collection.create_index("ornek_turu")
        await samples_collection.create_index("ornekleme_tarihi")
        await samples_collection.create_index("ornek.tur")
        await samples_collection.create_index("konum.jeoloji")

        print("📊 Veritabanı indeksleri oluşturuldu")

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Veritabanı instance'ını döndür."""
        if cls.db is None:
            raise Exception("Veritabanı bağlantısı yapılmadı")
        return cls.db


# Dependency injection için
async def get_database() -> AsyncIOMotorDatabase:
    """FastAPI dependency."""
    return Database.get_db()
