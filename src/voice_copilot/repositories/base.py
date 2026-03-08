"""
Base repository pattern for database operations.
"""

from typing import Generic, TypeVar, Type, List, Optional, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from ..logging_config import get_logger
from ..exceptions import DatabaseException

logger = get_logger(__name__)

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def create(self, **kwargs) -> ModelType:
        """
        Create a new record.
        
        Args:
            **kwargs: Model field values
            
        Returns:
            Created model instance
        """
        try:
            instance = self.model(**kwargs)
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            logger.info(
                "repository_create",
                model=self.model.__name__,
                id=getattr(instance, "id", None)
            )
            return instance
        except Exception as e:
            self.db.rollback()
            logger.error(
                "repository_create_error",
                model=self.model.__name__,
                error=str(e)
            )
            raise DatabaseException(f"Failed to create {self.model.__name__}: {str(e)}")
    
    def get_by_id(self, id_value: Any) -> Optional[ModelType]:
        """
        Get record by primary key.
        
        Args:
            id_value: Primary key value
            
        Returns:
            Model instance or None
        """
        try:
            # Get primary key column name
            pk_column = list(self.model.__table__.primary_key.columns)[0]
            stmt = select(self.model).where(pk_column == id_value)
            result = self.db.execute(stmt).scalar_one_or_none()
            return result
        except Exception as e:
            logger.error(
                "repository_get_error",
                model=self.model.__name__,
                id=id_value,
                error=str(e)
            )
            raise DatabaseException(f"Failed to get {self.model.__name__}: {str(e)}")
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        try:
            stmt = select(self.model).offset(skip).limit(limit)
            result = self.db.execute(stmt).scalars().all()
            return list(result)
        except Exception as e:
            logger.error(
                "repository_get_all_error",
                model=self.model.__name__,
                error=str(e)
            )
            raise DatabaseException(f"Failed to get all {self.model.__name__}: {str(e)}")
    
    def update(self, id_value: Any, **kwargs) -> Optional[ModelType]:
        """
        Update a record.
        
        Args:
            id_value: Primary key value
            **kwargs: Fields to update
            
        Returns:
            Updated model instance or None
        """
        try:
            instance = self.get_by_id(id_value)
            if not instance:
                return None
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            self.db.commit()
            self.db.refresh(instance)
            logger.info(
                "repository_update",
                model=self.model.__name__,
                id=id_value
            )
            return instance
        except Exception as e:
            self.db.rollback()
            logger.error(
                "repository_update_error",
                model=self.model.__name__,
                id=id_value,
                error=str(e)
            )
            raise DatabaseException(f"Failed to update {self.model.__name__}: {str(e)}")
    
    def delete(self, id_value: Any) -> bool:
        """
        Delete a record.
        
        Args:
            id_value: Primary key value
            
        Returns:
            True if deleted, False if not found
        """
        try:
            instance = self.get_by_id(id_value)
            if not instance:
                return False
            
            self.db.delete(instance)
            self.db.commit()
            logger.info(
                "repository_delete",
                model=self.model.__name__,
                id=id_value
            )
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(
                "repository_delete_error",
                model=self.model.__name__,
                id=id_value,
                error=str(e)
            )
            raise DatabaseException(f"Failed to delete {self.model.__name__}: {str(e)}")
    
    def filter(self, **kwargs) -> List[ModelType]:
        """
        Filter records by field values.
        
        Args:
            **kwargs: Field filters
            
        Returns:
            List of matching model instances
        """
        try:
            stmt = select(self.model)
            for key, value in kwargs.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)
            
            result = self.db.execute(stmt).scalars().all()
            return list(result)
        except Exception as e:
            logger.error(
                "repository_filter_error",
                model=self.model.__name__,
                filters=kwargs,
                error=str(e)
            )
            raise DatabaseException(f"Failed to filter {self.model.__name__}: {str(e)}")
    
    def count(self, **kwargs) -> int:
        """
        Count records matching filters.
        
        Args:
            **kwargs: Field filters
            
        Returns:
            Count of matching records
        """
        try:
            stmt = select(self.model)
            for key, value in kwargs.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)
            
            result = self.db.execute(stmt).scalars().all()
            return len(result)
        except Exception as e:
            logger.error(
                "repository_count_error",
                model=self.model.__name__,
                error=str(e)
            )
            raise DatabaseException(f"Failed to count {self.model.__name__}: {str(e)}")
