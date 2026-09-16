
from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str:
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

        campaign_id = f"g-{uuid4()}"

        return campaign_id

    def pause_campaign(self, campaign_id: str) -> None:
        pass

class FacebookAdsClient(ChannelClient):
    def __init__(self):
        super().__init__("facebook")

    def create_campaign(self, campaign: Campaign) -> str:

        budget = GlobalBudget()

        budget.allocate(campaign.daily_budget)

        campaign_id = f"f-{uuid4()}"

        return campaign_id

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
            raise ValueError("Unsupported channel")
