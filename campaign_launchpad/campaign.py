
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
      # TODO
      self.campaign = Campaign()

    def with_name(self, name: str):
      # TODO
      self.campaign.name = name
      return self

    def with_channel(self, channel: str):
      # TODO
      self.campaign.channel = channel
      return self

    def with_budget(self, daily_budget: float):
      # TODO
      self.campaign.daily_budget = daily_budget
      return self

    def with_dates(self, start_date, end_date=None):
      # TODO
      self.campaign.start_date = start_date
      self.campaign.end_date = end_date
      return self

    def with_audience(self, **kwargs):
      # TODO
      self.target_audience.update(kwargs)
      return self


    def add_creative(self, headline: str, image_url: str):
      # TODO
      self.creatives.append({"headline": headline, "image_url" : image_url})
      return self

    def with_tracking(self, **kwargs):
      # TODO
      self.tracking.update(kwargs)
      return self

    def build(self) -> Campaign:
      # TODO: Validations and return Campaign instance
      if not self.name:
          raise ValueError("No name")
      if not self.channel:
          raise ValueError("No channel")
      if not self.daily_budget or daily_budget < 0:
          raise ValueError("Invalid Budget")
      if not self.start_date:
          raise ValueError("No start date")
      if self.start_date > self.end_date:
          raise ValueError("Invalid start/end dates")
      if not self.creatives:
          raise ValueError("At least one creative is required")
