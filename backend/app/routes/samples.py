"""
Sample routes - REST API endpoints.
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.models.sample import SampleCreate, SampleUpdate, SampleResponse, SampleListResponse
from app.services.sample_service import SampleService
from app.repositories.sample_repository import SampleRepository
from app.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase


router = APIRouter()


def get_sample_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> SampleService:
    """Sample service dependency."""
    repository = SampleRepository(db)
    return SampleService(repository)


@router.post(
    "/samples",
    response_model=SampleResponse,
    status_code=201,
    summary="Yeni örnek oluştur",
    description="Yeni bir mikroplastik örneği kaydeder."
)
async def create_sample(
    sample: SampleCreate,
    service: SampleService = Depends(get_sample_service)
):
    """Yeni örnek oluştur."""
    return await service.create_sample(sample)


@router.get(
    "/samples",
    response_model=SampleListResponse,
    summary="Örnekleri listele",
    description="Tüm örnekleri sayfalama ve filtreleme ile listeler."
)
async def list_samples(
    page: int = Query(1, ge=1, description="Sayfa numarası"),
    page_size: int = Query(20, ge=1, le=100, description="Sayfa başına kayıt sayısı"),
    ornek_turu: Optional[str] = Query(None, description="Örnek türüne göre filtrele"),
    jeoloji: Optional[str] = Query(None, description="Jeoloji türüne göre filtrele"),
    service: SampleService = Depends(get_sample_service)
):
    """Örnekleri listele."""
    return await service.list_samples(
        page=page,
        page_size=page_size,
        ornek_turu=ornek_turu,
        jeoloji=jeoloji
    )


@router.get(
    "/samples/{sample_id}",
    response_model=SampleResponse,
    summary="Örnek detayı",
    description="Belirtilen ID'ye sahip örneğin detayını getirir."
)
async def get_sample(
    sample_id: str,
    service: SampleService = Depends(get_sample_service)
):
    """Örnek detayını getir."""
    return await service.get_sample(sample_id)


@router.put(
    "/samples/{sample_id}",
    response_model=SampleResponse,
    summary="Örnek güncelle",
    description="Mevcut bir örneği günceller."
)
async def update_sample(
    sample_id: str,
    update: SampleUpdate,
    service: SampleService = Depends(get_sample_service)
):
    """Örnek güncelle."""
    return await service.update_sample(sample_id, update)


@router.delete(
    "/samples/{sample_id}",
    summary="Örnek sil",
    description="Belirtilen ID'ye sahip örneği siler."
)
async def delete_sample(
    sample_id: str,
    service: SampleService = Depends(get_sample_service)
):
    """Örnek sil."""
    return await service.delete_sample(sample_id)
