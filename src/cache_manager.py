import json
import os
from datetime import datetime, timedelta
from typing import Dict
from log import logger

CACHE_FILE = "commit_timestamps.json"
COMMITS_DEFAULT_SINCE_DAYS = 3
CACHE_VERSION = 1


class CacheManager:
    def __init__(self, cache_file: str = CACHE_FILE):
        self.cache_file = cache_file
        self.timestamps: Dict[str, str] = {}

    def load(self) -> None:
        """Load commit timestamps from cache file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    data = json.load(f)
                    # Check cache version
                    if data.get("__version__") != CACHE_VERSION:
                        logger.warning(
                            "Cache version mismatch, starting with empty cache"
                        )
                        self.timestamps = {}
                    else:
                        self.timestamps = data.get("timestamps", {})
                logger.info(f"Loaded {len(self.timestamps)} timestamps from cache")
            except json.JSONDecodeError:
                logger.warning("Failed to load cache file, starting with empty cache")
                self.timestamps = {}
        else:
            logger.info("No cache file found, starting with empty cache")
            self.timestamps = {}

    def save(self) -> None:
        """Save commit timestamps to cache file"""
        # Clean up old timestamps
        cutoff_date = (
            datetime.now() - timedelta(days=COMMITS_DEFAULT_SINCE_DAYS)
        ).isoformat()
        self.timestamps = {
            repo: timestamp
            for repo, timestamp in self.timestamps.items()
            if timestamp >= cutoff_date
        }

        # Save to file with version
        data = {"__version__": CACHE_VERSION, "timestamps": self.timestamps}
        with open(self.cache_file, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved {len(self.timestamps)} timestamps to cache")

    def get_timestamp(self, repo: str) -> datetime | None:
        """Get the last commit timestamp for a repository"""
        timestamp = self.timestamps.get(repo)
        if timestamp:
            return datetime.fromisoformat(timestamp)
        return None

    def set_timestamp(self, repo: str, timestamp: datetime) -> None:
        """Set the last commit timestamp for a repository"""
        self.timestamps[repo] = timestamp.isoformat()
