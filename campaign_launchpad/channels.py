
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
        raise NotImplementedError

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None:
        raise NotImplementedError


class GoogleAdsClient(ChannelClient):
    def __init__(self):
        super().__init__("google")

    def create_campaign(self, campaign: Campaign) -> str:
        budget = GlobalBudget()
        if campaign.daily_budget > budget.remaining():
            raise ValueError("Insufficient funds to create this campaign.")
        budget.allocate(campaign.daily_budget)
        return f"g-{uuid4().hex[:8]}"

    def pause_campaign(self, campaign_id: str) -> None:
        return None


class FacebookAdsClient(ChannelClient):
    def __init__(self):
        super().__init__("facebook")

    def create_campaign(self, campaign: Campaign) -> str:
        budget = GlobalBudget()
        if campaign.daily_budget > budget.remaining():
            raise ValueError("Insufficient funds to create this campaign.")
        budget.allocate(campaign.daily_budget)
        return f"f-{uuid4().hex[:8]}"

    def pause_campaign(self, campaign_id: str) -> None:
        return None


class ChannelClientFactory:
    @staticmethod
    def create(channel: str) -> ChannelClient:
        normalized_channel = str(channel).lower()
        if normalized_channel == "google":
            return GoogleAdsClient()
        if normalized_channel == "facebook":
            return FacebookAdsClient()
        raise ValueError(f"Unsupported channel: {channel}")
