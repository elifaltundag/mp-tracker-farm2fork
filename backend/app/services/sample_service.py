"""
Sample service - İş mantığı katmanı.
"""
from typing import Optional, List, Dict, Any
from app.repositories.sample_repository import SampleRepository
from app.models.sample import SampleCreate, SampleUpdate, SampleResponse, SampleListResponse
from app.config import MESSAGES
from fastapi import HTTPException


class SampleService:
    """Örnek verileri için servis katmanı."""

    def __init__(self, repository: SampleRepository):
        self.repository = repository

    async def create_sample(self, sample: SampleCreate) -> SampleResponse:
        """Yeni örnek oluştur."""
        # Örnek numarası kontrolü
        existing = await self.repository.find_by_ornek_no(sample.ornek_no)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Örnek numarası '{sample.ornek_no}' zaten mevcut"
            )

        # Model'i dict'e çevir
        sample_data = sample.model_dump(exclude_none=False)

        # Tarihi string'e çevir
        if sample_data.get("ornekleme_tarihi"):
            sample_data["ornekleme_tarihi"] = sample.ornekleme_tarihi.isoformat()

        # Repository'ye kaydet
        created = await self.repository.create(sample_data)

        return SampleResponse(**created)

    async def get_sample(self, sample_id: str) -> SampleResponse:
        """Örnek detayını getir."""
        sample = await self.repository.find_by_id(sample_id)

        if not sample:
            raise HTTPException(
                status_code=404,
                detail=MESSAGES["sample_not_found"]
            )

        return SampleResponse(**sample)

    async def list_samples(
        self,
        page: int = 1,
        page_size: int = 20,
        ornek_turu: Optional[str] = None,
        jeoloji: Optional[str] = None
    ) -> SampleListResponse:
        """Örnek listesini getir."""
        # Sayfalama hesapla
        skip = (page - 1) * page_size

        # Filtreleri hazırla
        filters = {}
        if ornek_turu:
            filters["ornek_turu"] = ornek_turu
        if jeoloji:
            filters["konum.jeoloji"] = jeoloji

        # Verileri getir
        samples, total = await self.repository.find_all(
            skip=skip,
            limit=page_size,
            filters=filters
        )

        # Response oluştur
        sample_responses = [SampleResponse(**s) for s in samples]
        total_pages = (total + page_size - 1) // page_size

        return SampleListResponse(
            data=sample_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    async def update_sample(self, sample_id: str, update: SampleUpdate) -> SampleResponse:
        """Örnek güncelle."""
        # Önce mevcut olup olmadığını kontrol et
        existing = await self.repository.find_by_id(sample_id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=MESSAGES["sample_not_found"]
            )

        # Update data hazırla
        update_data = update.model_dump(exclude_none=True)

        # Tarihi string'e çevir
        if "ornekleme_tarihi" in update_data and update_data["ornekleme_tarihi"]:
            update_data["ornekleme_tarihi"] = update.ornekleme_tarihi.isoformat()

        # Güncelle
        updated = await self.repository.update(sample_id, update_data)

        return SampleResponse(**updated)

    async def delete_sample(self, sample_id: str) -> dict:
        """Örnek sil."""
        # Önce mevcut olup olmadığını kontrol et
        existing = await self.repository.find_by_id(sample_id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=MESSAGES["sample_not_found"]
            )

        # Sil
        success = await self.repository.delete(sample_id)

        if not success:
            raise HTTPException(
                status_code=500,
                detail=MESSAGES["database_error"]
            )

        return {"message": MESSAGES["sample_deleted"], "id": sample_id}
