import random
import pandas as pd
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def choose_action(self):
        return input(f"{self.name}, choose action (C for cooperate, D for defect): ").upper()

class BotPlayer(Player):
    bot_number = 1

    def __init__(self, strategy, score_counter):
        super().__init__(f"Bot{BotPlayer.bot_number}")
        BotPlayer.bot_number += 1
        self.opponent_last_actions = []
        self.strategy = strategy
        self.score_counter = score_counter
        self.move_counter = 0  # Initialize move counter

    def choose_action(self):
        if self.strategy == 'Tit2ForTat':
            return self.tit2_for_tat()
        elif self.strategy == 'Copycat':
            return self.copycat()
        elif self.strategy == 'Cheater':
            return self.cheater()
        elif self.strategy == 'DefectEverySecond':
            return self.defect_every_second()
        elif self.strategy == 'Random':
            return self.random_action();

    def tit2_for_tat(self):
        if not self.opponent_last_actions:
            return random.choice(['C', 'D'])
        elif self.opponent_last_actions[-1]=='D':
            return 'D'
        elif len(self.opponent_last_actions)<2:
            return 'C'
        elif self.opponent_last_actions[-2]=='D':
            return 'D'
        else:
            return 'C';

    def copycat(self):
        if not self.opponent_last_actions:
            return random.choice(['C', 'D'])
        if self.opponent_last_actions[-1]=='':
            return 'C'
        else:
            return self.opponent_last_actions[-1]

    def cheater(self):
        return 'D'

    def defect_every_second(self):
        self.move_counter += 1
        return 'D' if self.move_counter % 2 == 0 else 'C'

    def random_action(self):
        return random.choice(['C', 'D'])

def main():
    player1 = Player("User")
    overall_score = Player("Overall")
  
    all_players = [
        BotPlayer('Tit2ForTat', overall_score),
        BotPlayer('Copycat', overall_score),
        BotPlayer('Cheater', overall_score),
        BotPlayer('DefectEverySecond', overall_score),
        BotPlayer('Random', overall_score),
    ]

    
    opponents = random.sample(all_players, 3)
    print("You are in a tournament against 5 players out of which you have to play 10 rounds against 3 random players.\nYour goal is to get cumulative 40 points.\nThe rules are as follows\n")
    scoring={
            'C':{' C ':'+1/+1',' D ':'0/+5'},
            'D':{' C ':'+3/0',' D ':'-1/-1'}
            }
    df=pd.DataFrame(scoring);
    print(df)
    print("\nThe rows represent opponent input and column represent player input.\nThe points are in the format player/opponent\n")
    print("You are playing against:")
    for opponent in opponents:
        print(f"{opponent.name}")
    opponents = random.sample(opponents,3)
    for selected_opponent in opponents:
        print(f"\nPlaying 10 rounds against an anonymous opponent")
        for round_num in range(1, 11):
            print(f"\nRound {round_num}")
            action1 = player1.choose_action()
            action2 = selected_opponent.choose_action()

            if action1 == 'C' and action2 == 'C':
                player1.score += 1
                selected_opponent.score_counter.score += 1
            elif action1=='' and action2=='C' and selected_opponent.strategy=="Random":
                player1.score += 3
            elif action1 == 'C' and action2 == 'D':
                player1.score += 0
                selected_opponent.score_counter.score += 5
            elif action1 == 'D' and action2 == 'C':
                player1.score += 3
                selected_opponent.score_counter.score += 0
            elif action1 == 'D' and action2 == 'D':
                player1.score -= 1
                selected_opponent.score_counter.score -= 1

            player1.opponent_last_action = action2
            selected_opponent.opponent_last_actions.append(action1)

            print(f"Scores: {player1.name}: {player1.score}, Opponent: Bot ({selected_opponent.score_counter.score})")

    print("\nFinal Scores:")
    print(f"{player1.name}: {player1.score}")
    print(f"{overall_score.name}: {overall_score.score}")

    if player1.score >= 40:
        print("Congratulations! You win against the three selected opponents!\nFlag:nite{a_v3ry_nashty_play3r}")

if __name__ == "__main__":
    main()
