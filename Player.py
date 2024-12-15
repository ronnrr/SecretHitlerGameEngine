from abc import ABC, abstractmethod


class Player(ABC):
    @abstractmethod
    def discard_card(self):
        pass

    @abstractmethod
    def suggest_chancellor(self):
        pass

    @abstractmethod
    def exercise_power(self, rule_count, players):
        if rule_count == 2:
            self.choose_player_to_investigate(players)
        elif rule_count == 3:
            self.choose_next_president(players)
        elif rule_count >= 4:
            self.choose_player_to_kill(players)

    @abstractmethod
    def choose_player_to_investigate(self, players):
        pass

    @abstractmethod
    def choose_next_president(self, players):
        pass

    @abstractmethod
    def choose_player_to_kill(self, players):
        pass