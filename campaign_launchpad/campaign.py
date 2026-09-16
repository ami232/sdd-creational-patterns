
from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any, List


@dataclass(frozen=True)
class Campaign:
    name: str
    channel: str
    daily_budget: float
    start_date: date
    end_date: Optional[date]
    target_audience: Dict[str, Any]
    creatives: List[Dict[str, str]]
    tracking: Dict[str, str]


class CampaignBuilder:
    def __init__(self):
        self.name = None
        self.channel = None
        self.daily_budget = None
        self.start_date = None
        self.end_date = None
        self.target_audience = {}
        self.creatives = []
        self.tracking = {}

    def with_name(self, name: str):
        self.name = name
        return self

    def with_channel(self, channel: str):
        self.channel = channel
        return self

    def with_budget(self, daily_budget: float):
        self.daily_budget = daily_budget
        return self

    def with_dates(self, start_date, end_date=None):
        self.start_date = start_date
        self.end_date = end_date
        return self

    def with_audience(self, **kwargs):
        self.target_audience = kwargs
        return self

    def add_creative(self, headline: str, image_url: str):
        self.creatives.append({"headline": headline, "image_url": image_url})
        return self

    def with_tracking(self, **kwargs):
        self.tracking = kwargs
        return self

    def build(self) -> Campaign:
        if not self.name or not self.name.strip():
            raise ValueError("Campaign name is required")
        if not self.channel or not self.channel.strip():
            raise ValueError("Campaign channel is required")
        if self.daily_budget is None or not self.daily_budget > 0:
            raise ValueError("Budget must be provided and positive")
        if self.start_date is None:
            raise ValueError("Start date is required")
        if self.end_date is not None and self.start_date > self.end_date:
            raise ValueError("Start date must be before or equal to end date")
        if not self.creatives:
            raise ValueError("At least one creative is required")
        for creative in self.creatives:
            if not creative["headline"].strip() or not creative["image_url"].strip():
                raise ValueError("Each creative requires a headline and image URL")

        return Campaign(
            name=self.name,
            channel=self.channel,
            daily_budget=self.daily_budget,
            start_date=self.start_date,
            end_date=self.end_date,
            target_audience=deepcopy(self.target_audience),
            creatives=deepcopy(self.creatives),
            tracking=deepcopy(self.tracking),
        )
