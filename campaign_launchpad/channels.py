
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str:
        """Create a campaign on this channel and return an external id."""
        pass

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        pass


class GoogleAdsClient(ChannelClient):
    def create_campaign(self, campaign: Campaign) -> str:
        # Raises ValueError if the global budget cannot cover this campaign.
        GlobalBudget().allocate(campaign.daily_budget)
        return f"g-{uuid4()}"

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[{self.name}] paused campaign {campaign_id}")


class FacebookAdsClient(ChannelClient):
    def create_campaign(self, campaign: Campaign) -> str:
        GlobalBudget().allocate(campaign.daily_budget)
        return f"f-{uuid4()}"

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[{self.name}] paused campaign {campaign_id}")


class ChannelClientFactory:
    @staticmethod
    def create(channel: str) -> ChannelClient:
        if channel == "google":
            return GoogleAdsClient(name="Google Ads")
        elif channel == "facebook":
            return FacebookAdsClient(name="Facebook Ads")
        else:
            raise ValueError(f"Unsupported channel: {channel}")
