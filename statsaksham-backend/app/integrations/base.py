from datetime import datetime, timezone
from typing import Any, Dict, List
from app.repositories.in_memory import db


class IGOTAdapter:
    async def get_courses(self, competency: str | None = None) -> List[Dict[str, Any]]:
        courses = [c for c in db.courses if c["provider"] == "iGOT Karmayogi"]
        if competency:
            courses = [c for c in courses if competency.lower() in c["competency"].lower()]
        return courses

    async def sync(self) -> Dict[str, Any]:
        return {
            "provider": "iGOT Karmayogi",
            "mode": "MOCK",
            "status": "Connected",
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "records_synced": len(db.courses),
        }


class NSSTAAdapter:
    async def get_programmes(self) -> List[Dict[str, Any]]:
        return [c for c in db.courses if c["provider"] == "NSSTA"]

    async def sync(self) -> Dict[str, Any]:
        return {
            "provider": "NSSTA",
            "mode": "MOCK",
            "status": "Connected",
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "records_synced": 2,
        }


class TPACAdapter:
    async def sync(self) -> Dict[str, Any]:
        return {
            "provider": "TPAC",
            "mode": "MOCK",
            "status": "Connected",
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "records_synced": 6,
        }


igot_adapter = IGOTAdapter()
nssta_adapter = NSSTAAdapter()
tpac_adapter = TPACAdapter()
