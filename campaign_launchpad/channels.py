
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
    def __init__(self):
        super().__init__("google")

    def create_campaign(self, campaign: Campaign) -> str:
        budget = GlobalBudget()
        budget.allocate(campaign.daily_budget)
        new_id = "g-" + str(uuid4())
        return new_id

    def pause_campaign(self, campaign_id: str) -> None:
        pass


class FacebookAdsClient(ChannelClient):
    def __init__(self):
        super().__init__("facebook")

    def create_campaign(self, campaign: Campaign) -> str:
        budget = GlobalBudget()
        budget.allocate(campaign.daily_budget)
        new_id = "f-" + str(uuid4())
        return new_id

    def pause_campaign(self, campaign_id: str) -> None:
        pass


class ChannelClientFactory:
    @staticmethod
    def create(channel: str) -> ChannelClient:
        if channel == "google":
            return GoogleAdsClient()
        elif channel == "facebook":
            return FacebookAdsClient()
        else:
            raise ValueError(f"Unknown channel: {channel}")