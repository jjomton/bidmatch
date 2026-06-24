from repositories.match_rule_repository import MatchRuleRepository
from services.match_service import run_match_for_rule

class MatchRuleService:
    def __init__(self, repository=None):
        self.repository = repository or MatchRuleRepository()

    def list_rules(self, user_id):
        rules = self.repository.list(user_id)
        for r in rules:
            if r.get('created_at'):
                r['created_at'] = r['created_at'].isoformat()
            if r.get('updated_at'):
                r['updated_at'] = r['updated_at'].isoformat()
        return rules

    def create_rule(self, user_id, payload):
        rule = self.repository.create(user_id, payload)
        # 생성 후 즉시 매칭 로직 구동
        matched_count = run_match_for_rule(rule['id'])
        rule['matched_count'] = matched_count
        
        if rule.get('created_at'):
            rule['created_at'] = rule['created_at'].isoformat()
        if rule.get('updated_at'):
            rule['updated_at'] = rule['updated_at'].isoformat()
        return rule

    def update_rule(self, rule_id, payload):
        return self.repository.update(rule_id, payload)

    def delete_rule(self, rule_id, user_id):
        return self.repository.delete(rule_id, user_id)
