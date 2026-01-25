"""
Sample repository - MongoDB CRUD işlemleri.
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional, List, Dict, Any
from datetime import datetime


class SampleRepository:
    """Örnek verileri için repository."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.samples

    async def create(self, sample_data: dict) -> dict:
        """Yeni örnek oluştur."""
        # Metadata ekle
        sample_data["olusturma_tarihi"] = datetime.utcnow()
        sample_data["guncelleme_tarihi"] = datetime.utcnow()

        result = await self.collection.insert_one(sample_data)
        created_sample = await self.collection.find_one({"_id": result.inserted_id})
        return self._format_sample(created_sample)

    async def find_by_id(self, sample_id: str) -> Optional[dict]:
        """ID'ye göre örnek bul."""
        if not ObjectId.is_valid(sample_id):
            return None

        sample = await self.collection.find_one({"_id": ObjectId(sample_id)})
        return self._format_sample(sample) if sample else None

    async def find_all(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> tuple[List[dict], int]:
        """Tüm örnekleri listele (sayfalama ve filtreleme ile)."""
        query = filters or {}

        # Toplam kayıt sayısı
        total = await self.collection.count_documents(query)

        # Sayfalı sonuçlar
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("ornekleme_tarihi", -1)
        samples = await cursor.to_list(length=limit)

        formatted_samples = [self._format_sample(s) for s in samples]
        return formatted_samples, total

    async def update(self, sample_id: str, update_data: dict) -> Optional[dict]:
        """Örnek güncelle."""
        if not ObjectId.is_valid(sample_id):
            return None

        # Güncelleme zamanını ekle
        update_data["guncelleme_tarihi"] = datetime.utcnow()

        # None olan değerleri kaldır (partial update)
        update_data = {k: v for k, v in update_data.items() if v is not None}

        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(sample_id)},
            {"$set": update_data},
            return_document=True
        )

        return self._format_sample(result) if result else None

    async def delete(self, sample_id: str) -> bool:
        """Örnek sil."""
        if not ObjectId.is_valid(sample_id):
            return False

        result = await self.collection.delete_one({"_id": ObjectId(sample_id)})
        return result.deleted_count > 0

    async def find_by_ornek_no(self, ornek_no: str) -> Optional[dict]:
        """Örnek numarasına göre bul."""
        sample = await self.collection.find_one({"ornek_no": ornek_no})
        return self._format_sample(sample) if sample else None

    def _format_sample(self, sample: Optional[dict]) -> Optional[dict]:
        """MongoDB dökümanını API formatına çevir."""
        if not sample:
            return None

        sample["id"] = str(sample.pop("_id"))
        return sample
