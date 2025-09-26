"""
Роуты для ML функциональности
"""

import io
from typing import Any, Dict

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import get_current_active_user
from app.db import get_db
from app.models.user import User

router = APIRouter()


@router.get("/")
async def ml_info(
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """Information about available ML algorithms"""
    return {
        "available_algorithms": [
            {
                "name": "K-Means",
                "description": "K-Means clustering algorithm implemented from scratch",
                "cli_command": "python -m ml_core.kmeans --data data.csv --clusters 3",
                "status": "available",
            },
            {
                "name": "Decision Tree",
                "description": "Decision tree classifier with information gain",
                "cli_command": "python -m ml_core.decision_tree --data data.csv --target class",
                "status": "available",
            },
            {
                "name": "Random Forest",
                "description": "Random forest ensemble with bootstrap sampling",
                "cli_command": "python -m ml_core.random_forest --data data.csv --target class",
                "status": "available",
            },
        ],
        "message": "All ML algorithms are implemented and ready to use via CLI",
        "version": "1.0.2",
        "features": [
            "Custom implementations from scratch using NumPy",
            "CLI interfaces for all algorithms",
            "Performance testing and validation",
            "Sample data included for testing",
        ],
    }


@router.post("/upload-data")
async def upload_data(
    file: UploadFile = File(...), current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Загрузка данных для ML обработки"""

    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поддерживаются только CSV файлы",
        )

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        return {
            "filename": file.filename,
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "preview": df.head().to_dict("records"),
            "message": "Данные успешно загружены и проанализированы",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при обработке файла: {str(e)}",
        )
