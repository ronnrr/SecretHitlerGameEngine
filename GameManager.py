import random

from GameConstants import GameConstants
from Rule import Rule
from Victory import Victory


class GameManager(object):
    def __init__(self, players):
        self.players = players
        self.president_index = 0
        self.liberal_rules = []
        self.fascist_rules = []
        self.pile = [Rule.FASCIST, Rule.FASCIST, Rule.FASCIST, Rule.FASCIST,
                     Rule.FASCIST, Rule.FASCIST, Rule.FASCIST, Rule.FASCIST,
                     Rule.FASCIST, Rule.FASCIST, Rule.FASCIST, Rule.LIBERAL,
                     Rule.LIBERAL, Rule.LIBERAL, Rule.LIBERAL, Rule.LIBERAL,
                     Rule.LIBERAL]
        self.temporary_discard_pile = []
        random.shuffle(self.pile)

    def run_game_loop(self):
        game_has_not_ended = True
        while game_has_not_ended:
            chancellor, president = self.select_chancellor()
            if not chancellor:
                card = self.draw_random_card_from_pile()
                self.assign_card_to_correct_pile(card)
                victory = self.check_victory()
                if victory == Victory.NOONE:
                    continue
                return victory
            cards = [self.draw_random_card_from_pile(), self.draw_random_card_from_pile(),
                     self.draw_random_card_from_pile()]  # this needs to be refactored.
            cards, discarded_card = president.discard_card(cards)
            self.temporary_discard_pile.append(discarded_card)
            rule, discarded_card = chancellor.choose_rule()
            self.temporary_discard_pile.append(discarded_card)
            self.assign_card_to_correct_pile(rule)
            victory = self.check_victory()
            if victory != Victory.NOONE:
                return victory
            if rule == Rule.FASCIST:
                president.exercise_power(len(self.fascist_rules), self.players)
            self.president_index += 1

    def select_chancellor(self):
        for i in range(0, GameConstants.TURNS_UNTIL_RANDOM_DRAW):
            chancellor = self.players[self.president_index % len(self.players)].suggest_chancelor()
            self.president_index += 1
            if not chancellor:
                continue
            return chancellor, self.players[self.president_index % len(self.players)]
        return None, None

    def draw_random_card_from_pile(self):
        return self.pile.pop()

    def assign_card_to_correct_pile(self, card):
        if card == Rule.FASCIST:
            self.fascist_rules.append(card)
        else:
            self.liberal_rules.append(card)

    def check_victory(self):
        if len(self.liberal_rules) == GameConstants.LIBERAL_RULES_NEEDED_FOR_VICTORY:
            return Victory.LIBERAL
        elif len(self.fascist_rules) == GameConstants.FASCIST_RULES_NEEDED_FOR_VICTORY:
            return Victory.FASCIST
        return Victory.NOONE
