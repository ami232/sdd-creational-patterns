
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
      
      self._name: str = None
      self._channel: str = None
      self._daily_budget: float = None
      self._start_date: date = None
      self._end_date: Optional[date] = None
      self._target_audience: Dict[str, Any] = {}
      self._creatives: List[Dict[str, str]] = []
      self._tracking: Dict[str, str] = {}

    def with_name(self, name: str):
      self._name = name

      return self

    def with_channel(self, channel: str):
      self._channel = channel
      return self

    def with_budget(self, daily_budget: float):
      self._daily_budget = daily_budget
      return self
    
    def with_dates(self, start_date, end_date=None):
      self._start_date = start_date
      self._end_date = end_date
      return self
    
    def with_audience(self, **kwargs):
      self._target_audience.update(kwargs)
      return self

    def add_creative(self, headline: str, image_url: str):
      self._creatives.append({"headline": headline, "image_url": image_url})
      return self

    def with_tracking(self, **kwargs):
      self._tracking.update(kwargs)
      return self

    def build(self) -> Campaign:
      if not self._name:
        raise ValueError("Campaign name is required")
      if not self._channel:
        raise ValueError("Channel is required")
      if self._daily_budget is None or self._daily_budget <= 0:
        raise ValueError("Budget must be positive")
      if self._start_date is None:
        raise ValueError("Start date is required")
      if self._end_date is not None and self._start_date > self._end_date:
        raise ValueError("Start date must be before or equal to end date")
      if not self._creatives:
        raise ValueError("At least one creative is required")

      return Campaign(
          name=self._name,
          channel=self._channel,
          daily_budget=self._daily_budget,
          start_date=self._start_date,
          end_date=self._end_date,
          target_audience=self._target_audience,
          creatives=self._creatives,
          tracking=self._tracking,
      )
