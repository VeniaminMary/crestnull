import random
import os
from datetime import datetime

class krestikinoliki:
    def __init__(self):
        self.doska = []
        self.razmer = 0
        self.tekuschiy_igrok = ''
        self.igra_zavershena = False
        self.pobeditel = None
        self.stats_directory = "game_statistics"
        self._create_stats_directory()
        self.wins_o = 0
        self.wins_x = 0
        self.games_count = 0
        self.draws_count = 0
        
    def _create_stats_directory(self):
        if not os.path.exists(self.stats_directory):
            os.makedirs(self.stats_directory)
    
    def initialize_game_board(self, size):
        return [['.' for _ in range(size)] for _ in range(size)]
    
    def show_game_board(self, board):
        size = len(board)
        print("  " + " ".join(str(i + 1) for i in range(size)))
        for i in range(size):
            print(f"{i + 1} " + " ".join(board[i]))
    
    def make_player_move(self, board, row, col, current_player):
        if board[row][col] == '.':
            board[row][col] = current_player
            return True
        return False
    
    def check_winner(self, board, current_player):
        size = len(board)
        
        for i in range(size):
            if all(board[i][j] == current_player for j in range(size)):
                return True
        
        for j in range(size):
            if all(board[i][j] == current_player for i in range(size)):
                return True
        
        if all(board[i][i] == current_player for i in range(size)):
            return True
        
        if all(board[i][size-1-i] == current_player for i in range(size)):
            return True
        
        return False
    
    def check_draw(self, board):
        for row in board:
            if '.' in row:
                return False
        return True
    
    def ask_for_replay(self):
        while True:
            try:
                print('\nХотите сыграть еще раз?')
                print('1. Да')
                print('2. Нет')
                choice = int(input('Ваш выбор: '))
                if choice == 1:
                    return True
                elif choice == 2:
                    return False
                else:
                    print("Пожалуйста, введите 1 или 2")
            except ValueError:
                print("Пожалуйста, введите число")
    
    def select_random_starting_player(self):
        return random.choice(['X', 'O'])
    
    def update_score(self, current_player):
        if current_player == 'X':
            self.wins_x += 1
        else:
            self.wins_o += 1
    
    def save_game_statistics(self, is_draw=False, winner=None):
        self.games_count += 1
        if is_draw:
            self.draws_count += 1

        stats_file = os.path.join(self.stats_directory, "game_stats.txt")
        with open(stats_file, 'w', encoding='utf-8') as file:
            file.write('Статистика игр:\n')
            file.write(f'Побед O: {self.wins_o}\n')
            file.write(f'Побед X: {self.wins_x}\n')
            file.write(f'Сыграно игр: {self.games_count}\n')
            file.write(f'Ничьих: {self.draws_count}\n')
        
        detail_file = os.path.join(self.stats_directory, "detailed_stats.txt")
        with open(detail_file, 'a', encoding='utf-8') as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if is_draw:
                result = "Ничья"
            else:
                result = f"Победитель: {winner}"
            file.write(f"[{timestamp}] Игра #{self.games_count} - {result}\n")
    
    def get_valid_board_size(self):
        while True:
            try:
                size = int(input("Введите размер игрового поля (3-9): "))
                if 3 <= size <= 9:
                    return size
                else:
                    print("Неверный размер, пожалуйста введите число от 3 до 9")
            except ValueError:
                print("Пожалуйста, введите число")
    
    def get_valid_player_move(self, board, current_player):
        size = len(board)
        while True:
            try:
                print(f"\nХод игрока {current_player}. Введите строку и столбец (например: 1 2): ", end="")
                row, col = map(int, input().split())
                
                if not (1 <= row <= size and 1 <= col <= size):
                    print(f"Пожалуйста, введите числа от 1 до {size}")
                    continue
                
                if self.make_player_move(board, row-1, col-1, current_player):
                    return True
                else:
                    print("Эта клетка уже занята! Попробуйте другую.")
                    
            except ValueError:
                print("Пожалуйста, введите два числа через пробел")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
    
    def play_single_game(self):
        size = self.get_valid_board_size()
        board = self.initialize_game_board(size)
        current_player = self.select_random_starting_player()
        
        print(f'\nПервым ходит: {current_player}')
        self.show_game_board(board)
        
        while True:
            if self.get_valid_player_move(board, current_player):
                print()
                self.show_game_board(board)
                
                if self.check_winner(board, current_player):
                    print(f"\n{current_player} победил!")
                    self.update_score(current_player)
                    self.save_game_statistics(is_draw=False, winner=current_player)
                    return
                
                elif self.check_draw(board):
                    print("\nНичья!")
                    self.save_game_statistics(is_draw=True)
                    return
                
                current_player = 'O' if current_player == 'X' else 'X'
    
    def ochistit_ekran(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pokazat_statistiku(self):
        self.ochistit_ekran()
        print("Статистика")
        stats_file = os.path.join(self.stats_directory, "game_stats.txt")
        if os.path.exists(stats_file):
            print("\nОсновная статистика:")
            with open(stats_file, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print("Основная статистика пока недоступна.")
        

        detail_file = os.path.join(self.stats_directory, "detailed_stats.txt")
        if os.path.exists(detail_file):
            print("\nИстория последних игр:")
            with open(detail_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    for line in lines[-10:]: 
                        print(line.strip())
                else:
                    print("История игр пока пуста.")
        else:
            print("История игр пока недоступна.")
        
        input("\nНажмите Enter для продолжения...")
    
    def sprosit_igrat_esche(self):
        while True:
            print("\nВыберите действие:")
            print("1 - Новая игра")
            print("2 - Показать статистику")
            print("3 - Выйти из игры")
            
            vybor = input("Ваш выбор (1-3): ").strip()
            
            if vybor == '1':
                return True
            elif vybor == '2':
                self.pokazat_statistiku()
                self.ochistit_ekran()
                continue
            elif vybor == '3':
                return False
            else:
                print("Пожалуйста, введите 1, 2 или 3.")
    
    def igrat_v_igru(self):
        self.ochistit_ekran()
        print("     Крестики-Нолики    ")
        self.play_single_game()
    
    def start_game_session(self):
        print("Добро пожаловать в игру Крестики-Нолики!")
        print(f"Статистика сохраняется в папке: {self.stats_directory}")
        
        while True:
            self.igrat_v_igru()
            
            if not self.sprosit_igrat_esche():
                print("\nСпасибо за игру! До свидания!")
                break
            
            print("\nНачинаем новую игру!")
            self.ochistit_ekran()

def main():
    game = krestikinoliki()
    game.start_game_session()

if __name__ == "__main__":
    main()