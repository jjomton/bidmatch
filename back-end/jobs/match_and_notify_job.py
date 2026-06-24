from services.matching_service import MatchingService


def run():
    matcher = MatchingService()
    return matcher.match()
