
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str:
        # TODO: Create a campaign on this channel and return an external id.
        pass

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        pass


class GoogleAdsClient(ChannelClient):
  # TODO: Implement the Google Ads specific logic here.
  def __init__(self):
     super().__init__("google")
  def create_campaign(self,campaign: Campaign) -> str:
     budget=GlobalBudget()
     budget.allocate(campaign.daily_budget)
     return f"g-{uuid4()}"
  def pause_campaign(self, campaign_id: str) -> None:
          pass

class FacebookAdsClient(ChannelClient):
  # TODO: Implement the Facebook Ads specific logic here.
  def __init__(self):
     super().__init__("facebook")
  def create_campaign(self,campaign: Campaign) -> str:
     budget=GlobalBudget()
     budget.allocate(campaign.daily_budget)
     return f"f-{uuid4()}"
  def pause_campaign(self, campaign_id: str) -> None:
          pass

class ChannelClientFactory:
    @staticmethod
    def create(channel: str) -> ChannelClient:
      # TODO: Return the appropriate client based on the channel.
      if channel=="google":
        return GoogleAdsClient()
      elif channel=="facebook":
        return FacebookAdsClient()
      else:
         raise ValueError(f"Unsupported channel: {channel}")
