def all_roles(x, hold_num):
    rolls = set([()])
    for i in range(hold_num):
        this_move = set()
        for hold_next in rolls:
            for next in x:
                hold = list(hold_next)
                hold.append(next)
                this_move.add(tuple(hold))
        rolls = this_move
    return rolls

def score(hand):
    max_score = 0
    if len(hand) > 0:
        for num in hand:
            score = 0
            for i in range(len(hand)):
                if num == hand[i]:
                    score += num
            if score > max_score:
                max_score = score
        return max_score
    else:
        return 0

def score_next(hold_dice, hold_num):

    scores = []
    rolls = all_roles(range(1, 7), hold_num)
    for roll in rolls:
        scores.append(score(roll + hold_dice))
    return sum(scores) / float(len(scores))


def holds(current_state):
    if len(current_state) > 0:
        current = list(current_state)
        out = current.pop()
        last_holds = holds (tuple(current))
        all_holds = set([()])
        for hold in last_holds:
            x = list(hold)
            x.append(out)
            all_holds.add(tuple(x))
        all_holds.update(last_holds)
        return all_holds
    else:
        return set([()])

def main(current_state):
    possible_holds = holds(current_state)

    next_move = ()
    max_value = 0
    for next in possible_holds:
        score = score_next(next, 3 - len(next))
        if score > max_value:
            max_value = score
            next_move = next
    return next_move


def evaluate():
    current_state = (6, 1, 1)
    next_move = main(current_state)
    print "Next move should be to hold", next_move

evaluate()