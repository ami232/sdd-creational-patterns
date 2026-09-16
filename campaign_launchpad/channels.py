
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    def __init__(self, name: str):
        self.name = name

    def _register_campaign(self, campaign: Campaign, prefix: str) -> str:
        GlobalBudget().allocate(campaign.daily_budget)
        return f"{prefix}{uuid4()}"

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str:
        # TODO: Create a campaign on this channel and return an external id.
        pass

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        pass


class GoogleAdsClient(ChannelClient):
    def create_campaign(self, campaign: Campaign) -> str:
        return self._register_campaign(campaign, "g-")

    def pause_campaign(self, campaign_id: str) -> None:
        pass


class FacebookAdsClient(ChannelClient):
    def create_campaign(self, campaign: Campaign) -> str:
        return self._register_campaign(campaign, "f-")

    def pause_campaign(self, campaign_id: str) -> None:
        pass


class ChannelClientFactory:
    @staticmethod
    def create(channel: str) -> ChannelClient:
        if channel == "google":
            return GoogleAdsClient("google")
        if channel == "facebook":
            return FacebookAdsClient("facebook")
        raise ValueError(f"Unknown channel: {channel}")
