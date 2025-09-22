"""
Роуты для ML функциональности
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import io
from typing import Dict, Any

from app.db import get_db
from app.auth.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/")
async def ml_info(
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Информация о доступных ML алгоритмах"""
    return {
        "available_algorithms": [
            {
                "name": "K-Means",
                "description": "Алгоритм кластеризации K-средних",
                "endpoint": "/api/v1/ml/kmeans",
                "status": "coming_soon"
            },
            {
                "name": "Decision Tree",
                "description": "Дерево решений для классификации",
                "endpoint": "/api/v1/ml/decision-tree",
                "status": "coming_soon"
            },
            {
                "name": "Random Forest",
                "description": "Случайный лес для классификации и регрессии",
                "endpoint": "/api/v1/ml/random-forest",
                "status": "coming_soon"
            }
        ],
        "message": "ML модули будут реализованы в следующих версиях",
        "version": "0.1.0"
    }


@router.post("/upload-data")
async def upload_data(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Загрузка данных для ML обработки"""
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поддерживаются только CSV файлы"
        )
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        return {
            "filename": file.filename,
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "preview": df.head().to_dict('records'),
            "message": "Данные успешно загружены и проанализированы"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при обработке файла: {str(e)}"
        )
