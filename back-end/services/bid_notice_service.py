from repositories.bid_notice_repository import BidNoticeRepository


class BidNoticeService:
    def __init__(self, repository=None):
        self.repository = repository or BidNoticeRepository()

    def list_notices(self, filters=None):
        return self.repository.list(filters)

    def get_notice(self, notice_id):
        return self.repository.get(notice_id)
