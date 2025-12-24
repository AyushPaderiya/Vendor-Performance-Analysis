"""
Configuration loader utility for Vendor Performance Analysis.
Provides centralized access to all configuration parameters.
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager that loads and provides access to config.yaml settings."""
    
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls) -> 'Config':
        """Singleton pattern to ensure only one config instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self) -> None:
        """Load configuration from config.yaml file."""
        # Find project root by looking for config directory
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        config_path = project_root / 'config' / 'config.yaml'
        
        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}\n"
                "Please ensure config/config.yaml exists in the project root."
            )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
    
    def reload(self) -> None:
        """Reload configuration from file (useful after changes)."""
        self._load_config()
    
    @property
    def database(self) -> Dict[str, Any]:
        """Get database configuration."""
        return self._config.get('database', {})
    
    @property
    def database_path(self) -> str:
        """Get database file path."""
        return self.database.get('path', 'inventory.db')
    
    @property
    def data(self) -> Dict[str, Any]:
        """Get data source configuration."""
        return self._config.get('data', {})
    
    @property
    def raw_data_dir(self) -> str:
        """Get raw data directory path."""
        return self.data.get('raw_data_dir', 'data')
    
    @property
    def etl(self) -> Dict[str, Any]:
        """Get ETL configuration."""
        return self._config.get('etl', {})
    
    @property
    def load_mode(self) -> str:
        """Get ETL load mode (replace or append)."""
        return self.etl.get('load_mode', 'replace')
    
    @property
    def batch_size(self) -> int:
        """Get batch size for processing."""
        return self.etl.get('batch_size', 100000)
    
    @property
    def data_quality(self) -> Dict[str, Any]:
        """Get data quality configuration."""
        return self._config.get('data_quality', {})
    
    @property
    def missing_values(self) -> Dict[str, Any]:
        """Get missing value handling configuration."""
        return self._config.get('missing_values', {})
    
    @property
    def logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self._config.get('logging', {})
    
    @property
    def output(self) -> Dict[str, Any]:
        """Get output configuration."""
        return self._config.get('output', {})
    
    @property
    def metrics(self) -> Dict[str, Any]:
        """Get metrics calculation configuration."""
        return self._config.get('metrics', {})
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get any configuration value by dot-notation key.
        
        Example: config.get('database.path', 'default.db')
        """
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value


def get_config() -> Config:
    """Get the global configuration instance."""
    return Config()


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_database_url() -> str:
    """Get the SQLAlchemy database URL."""
    config = get_config()
    db_path = get_project_root() / config.database_path
    return f"sqlite:///{db_path}"
