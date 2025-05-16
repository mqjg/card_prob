import pydealer
import itertools
from pydealer.const import POKER_RANKS

def count_suits(stack):
    suits = {}
    for card in stack.cards:
        suit = card.suit
        if suit in suits.keys():
            suits[suit] += 1
        else:
            suits[suit] = 1

    return suits


def count_values(stack):
    values = {}
    for card in stack.cards:
        value = card.value
        if value in values.keys():
            values[value] += 1
        else:
            values[value] = 1

    return values


def classify_hand(stack):
    suits = count_suits(stack)
    values = count_values(stack)

    flush = False
    if 5 in suits.values():
        flush = True

    royal = False
    sequential = False
    if set(values.keys()) == {'Ace', 'King', 'Queen', 'Jack', '10'}:
        royal = True
        sequential = True
    elif set(values.keys()) == {'Ace', '2', '3', '4', '5'}:
        sequential = True


    sequential = False
    min_value = min(values.keys())
    if sorted(values.keys()) == list(range(min_value, min_value + 5)):
        sequential = True

    royal = False

    if flush and 5 in values.values():
        return 'Flush Five'
    elif flush and 3 in values.values() and 2 in values.values():
        return 'Flush House'
    elif 5 in values.values():
        return 'Five of a Kind'
    elif flush and sequential and royal:
        return 'Royal Flush'
    elif flush and sequential:
        return 'Straight Flush'
    elif 4 in values.values():
        return 'Four of a Kind'
    elif 3 in values.values() and 2 in values.values():
        return 'Full House'
    elif flush:
        return 'Flush'
    elif sequential:
        return 'Straight'
    elif 3 in values.values():
        return 'Three of a Kind'
    elif list(values.values()).count(2) == 2:
        return 'Two Pair'
    elif list(values.values()).count(2) == 1:
        return 'Pair'
    else:
        return 'High Card'


def permute_hands(hand, deck, max_hand_size=8, play_size=5):
    permute_size = max_hand_size - hand.size

    # get all permutations of cards that could be drawn
    possible_draws = itertools.combinations(deck.cards, r=permute_size)

    # create all possible hands
    possible_hands = []
    for draw in possible_draws:
        tmp_hand = pydealer.Stack()

        tmp_hand.add(hand.cards)

        tmp_hand.add(draw)
        possible_hands.append(tmp_hand)

    # get list of all possible cards we could play
    possible_plays = []
    for p_hand in possible_hands:
        plays = itertools.combinations(p_hand.cards, r=play_size)


        possible_plays += [pydealer.Stack(cards=play, sort=True) for play in list(plays)]

    # should this have duplicates?
    return possible_plays


if __name__ == "__main__":
    MAX_HAND_SIZE = 8
    HAND_SIZE = 6

    # Construct a Deck instance, with 52 cards.
    deck = pydealer.Deck()
    # Shuffle the deck, in place.
    deck.shuffle()

    deck.deal(35)

    # Construct a Stack instance, for use as a hand in this case.
    hand = pydealer.Stack()
    # Add the cards to the top of the hand (Stack).
    hand += deck.deal(HAND_SIZE)

    print(hand)
