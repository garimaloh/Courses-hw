"Classes necessary to play generalized Tic-tac-toe game."
import matplotlib.pyplot as plt
import numpy as np

class board():
    """ Implements shared methods between the game and the players classes. Specifically, methods available_moves, print_board, and win."""
    
    def __init__(self, board, k):
        self.board = board
        self.m, self.n = board.shape
        self.k = k
    
    def available_moves(self):
        am = [] # to accumulate available moves as tuples
        for i in range(self.m):
            for j in range(self.n):
                if self.board[i,j] == '_': am.append((i,j))
        return am

    def print_board(self):
        print(' ')
        for i in range(self.m):
            print (' ', end='')
            for j in range(self.n):
                print(self.board[i,j], end=' ')
            print(' ')
        print(' ')

    def _win(self, a):
        """ Checks if k consecutive sites are True. """
        # the task is easy if we convert everything to string type 
        # return self.__win(a) would use the method without string type
        wst = '1'*self.k
        st = ''
        for el in a:
            st += '1' if el else '0'
        return True if (wst in st) else False 
       
    def __win(self, a):
        """ Without using string type. """
        for i in range(len(a)-self.k+1):
            flag = True
            for j in range(self.k):
                if not a[i+j]:
                    flag = False
                    break
            if flag: return True

    def win(self, mark):
        pos = (self.board == mark)
        for i in range(self.m): # rows
            if self._win(pos[i,:]): return True
        for j in range(self.n): # columns
            if self._win(pos[:,j]): return True
        for o in range(-self.m+self.k, self.n-self.k+1): # diagonals
            if self._win(pos.diagonal(offset=o)): return True
        for o in range(-self.m+self.k, self.n-self.k+1): # diagonals
            if self._win(pos[:,::-1].diagonal(offset=o)): return True
        return False

class game(board): # inherits methods from board
    """Takes two player objects and plays one round. Returns 'draw' or a pointer to the winner. Players required to have methods set_mark and next_move."""
    def __init__(self, m, n, k, player_one, player_two,first_turn='random'): # constructor is overloaded
        self.board = np.full((m,n), '_') # this is how the board will be represented
        self.m = m
        self.n = n
        self.k = k
        # A somewhat long initialization of players and their marks 
        if first_turn=='random':
            if np.random.randint(0,2,1): # chose random player to move first; that player plays 'x' 
                player_one.set_mark('x')
                self.mark_one = 'x'
                player_two.set_mark('o')
                self.mark_two = 'o'
                self.player_one = player_one # store the pointer to the players
                self.player_two = player_two
                self.active_player = self.player_one
            else:
                player_one.set_mark('o') # reverse order
                self.mark_one = 'o'
                player_two.set_mark('x')
                self.mark_two = 'x'
                self.player_one = player_one 
                self.player_two = player_two
                self.active_player = self.player_two
                
        elif first_turn=='first_player':
            player_one.set_mark('x')
            self.mark_one = 'x'
            player_two.set_mark('o')
            self.mark_two = 'o'
            self.player_one = player_one # store the pointer to the players
            self.player_two = player_two
            self.active_player = self.player_one
            
        elif first_turn=='second_player':
            player_one.set_mark('o') # reverse order
            self.mark_one = 'o'
            player_two.set_mark('x')
            self.mark_two = 'x'
            self.player_one = player_one 
            self.player_two = player_two
            self.active_player = self.player_two             
        self.active_mark = 'x' # by our convention that is the active mark
    
    # actual game 
    def game(self):
        for i in range(self.board.size): # maximum number of moves, but can finish earlier
            move = self.active_player.next_move(self.board.copy(), self.k) # cannot modify the common board
            if move in self.available_moves():
                self.board[move] = self.active_mark
                if self.win(self.active_mark):
                    return self.active_player # end game
                else:
                    self.flip_players()
            else:
                self.flip_players()
                return self.active_player # end game because of wrong move
        return 'draw'
    # after writing this function I know that I need three other functions available_moves, flip_players, and winn

    def flip_players(self):
        if self.active_player == self.player_one:
            self.active_player = self.player_two
            self.active_mark = self.mark_two
        else:
            self.active_player = self.player_one
            self.active_mark = self.mark_one   

class rp(board): # inherits methods from board
    """Not a functional player on its own. Provides functionality to other classes."""
    
    def set_mark(self, mark): # this method is overloaded to set the opponent's mark as well
        self.mark = mark
        if self.mark == 'x':
            self.opp_mark = 'o' # opponent's mark
        else:
            self.opp_mark = 'x'

    def set_up(self, board, k):
        self.board = board
        self.m, self.n = board.shape
        self.k = k
        self.am = self.available_moves()

    def winning_moves(self):
        self.wm = [] # winning moves
        self.owm = [] # opponent's winning moves
        for move in self.am:
            self.board[move] = self.mark
            if self.win(self.mark): self.wm.append(move)
            self.board[move] = self.opp_mark
            if self.win(self.opp_mark): self.owm.append(move)
            self.board[move] = '_'

class rp_0(rp): # inherits methods from rp
    """Chooses a random move out of available ones."""
    def next_move(self, board, k):
        am=self.available_moves()
        self.set_up(board, k)
        return am[int(np.random.randint(0,len(am),1))]

class rp_1(rp): 
    """Checks if there is a winning move."""
    
    def next_move(self, board, k):
        self.set_up(board,k)
        self.winning_moves()
        if self.wm: # strategy implementation
            return self.wm[int(np.random.randint(0,len(self.wm),1))]
        else:
            return self.am[int(np.random.randint(0,len(self.am),1))]

class rp_2(rp):
    """Checks if there is a winning move for itself and the opponent."""
        
    def next_move(self, board, k):
        self.set_up(board,k)
        self.winning_moves()
        if self.wm: # strategy implementation
            return self.wm[int(np.random.randint(0,len(self.wm),1))]
        elif self.owm:
            return self.owm[int(np.random.randint(0,len(self.owm),1))]
        else:
            return self.am[int(np.random.randint(0,len(self.am),1))] 


def non_interactive_session(N,m,n,k,gamebetween,first_turn):
    
    if gamebetween=="AI1 vs. AI0":
        win1=0
        win2=0
        for i in range(N):        
            player_one=rp_1(np.full((m,n),'_'), k)
            player_two=rp_0(np.full((m,n),'_'), k)
            gm = game(m, n, k, player_one, player_two,first_turn)
            outcome=gm.game()
            if outcome==player_one:
                win1+=1
            elif outcome==player_two:
                win2+=1
        p1,p2=win1/N,win2/N
        return p1,p2

    elif gamebetween=="AI2 vs. AI0":
        win1=0
        win2=0
        for i in range(N):        
            player_one=rp_2(np.full((m,n),'_'), k)
            player_two=rp_0(np.full((m,n),'_'), k)
            gm = game(m, n, k, player_one, player_two,first_turn)
            outcome=gm.game()
            if outcome==player_one:
                win1+=1
            elif outcome==player_two:
                win2+=1
        p1,p2=win1/N,win2/N
        return p1,p2    

    elif gamebetween=="AI2 vs. AI1":
        win1=0
        win2=0
        for i in range(N):        
            player_one=rp_2(np.full((m,n),'_'), k)
            player_two=rp_1(np.full((m,n),'_'), k)
            gm = game(m, n, k, player_one, player_two,first_turn)
            outcome=gm.game()
            if outcome==player_one:
                win1+=1
            elif outcome==player_two:
                win2+=1
        p1,p2=win1/N,win2/N
        return p1,p2    
    
    elif gamebetween=="AI0 vs. AI0":
        win1=0
        win2=0
        for i in range(N):        
            player_one=rp_0(np.full((m,n),'_'), k)
            player_two=rp_0(np.full((m,n),'_'), k)
            gm = game(m, n, k, player_one, player_two,first_turn)
            outcome=gm.game()
            if outcome==player_one:
                win1+=1
            elif outcome==player_two:
                win2+=1
        p1,p2=win1/N,win2/N
        return p1,p2  
    
    elif gamebetween=="AI2 vs. AI2":
        win1=0
        win2=0
        for i in range(N):        
            player_one=rp_2(np.full((m,n),'_'), k)
            player_two=rp_2(np.full((m,n),'_'), k)
            gm = game(m, n, k, player_one, player_two,first_turn)
            outcome=gm.game()
            if outcome==player_one:
                win1+=1
            elif outcome==player_two:
                win2+=1
        p1,p2=win1/N,win2/N
        return p1,p2  
    

if __name__ == '__main__':
    
    print("-"*20)
    print("This is for first question")
    
    p1,p2=non_interactive_session(10**5,3,3,3,"AI1 vs. AI0",'random')
    print("The two probabilities for AI1 vs. AI0 game for (3,3,3) board are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))
    p1,p2=non_interactive_session(10**5,3,3,3,"AI2 vs. AI0",'random')
    print("The two probabilities for AI2 vs. AI0 game for (3,3,3) board are p1=P(AI2)={} and p2=P(AI0)={}".format(p1,p2))
    p1,p2=non_interactive_session(10**5,3,3,3,"AI2 vs. AI1",'random')
    print("The two probabilities for AI2 vs. AI1 game for (3,3,3) board are p1=P(AI2)={} and p2=P(AI1)={}".format(p1,p2))
    
    
    p1,p2=non_interactive_session(10**5,4,4,4,"AI1 vs. AI0",'random')
    print("The two probabilities for AI1 vs. AI0 game for (4,4,4) board are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))
    p1,p2=non_interactive_session(10**5,4,4,4,"AI2 vs. AI0",'random')
    print("The two probabilities for AI2 vs. AI0 game for (4,4,4) board are p1=P(AI2)={} and p2=P(AI0)={}".format(p1,p2))
    p1,p2=non_interactive_session(10**5,4,4,4,"AI2 vs. AI1",'random')
    print("The two probabilities for AI2 vs. AI1 game for (4,4,4) board are p1=P(AI2)={} and p2=P(AI1)={}".format(p1,p2))
    
    p1,p2=non_interactive_session(10**5,4,3,3,"AI1 vs. AI0",'random')
    print("The two probabilities for AI1 vs. AI0 game and (4,3,3) board are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2)) 
    p1,p2=non_interactive_session(10**5,4,3,3,"AI2 vs. AI0",'random')
    print("The two probabilities for AI2 vs. AI0 game and (4,3,3) board are p1=P(AI2)={} and p2=P(AI0)={}".format(p1,p2))
    p1,p2=non_interactive_session(10**5,4,3,3,"AI2 vs. AI1",'random')
    print("The two probabilities for AI2 vs. AI1 game and (4,3,3) board are p1=P(AI2)={} and p2=P(AI0)={}".format(p1,p2))
    
    print("-"*20)
    print("This is for second question")
    
    p1,p2=non_interactive_session(10**5,3,3,3,"AI0 vs. AI0",first_turn='first_player')
    print("The two probabilities for AI0 vs. AI0 game for (3,3,3) board and p1 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))
#    p1,p2=non_interactive_session(10**5,3,3,3,"AI0 vs. AI0",first_turn='second_player')
#    print("The two probabilities for AI0 vs. AI0 game for (3,3,3) board and p2 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))

    p1,p2=non_interactive_session(10**5,3,3,3,"AI2 vs. AI2",first_turn='first_player')
    print("The two probabilities for AI2 vs. AI2 game for (3,3,3) board and p1 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))
#    p1,p2=non_interactive_session(10**5,3,3,3,"AI2 vs. AI2",first_turn='second_player')
#    print("The two probabilities for AI2 vs. AI2 game for (3,3,3) board and p2 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))

    p1,p2=non_interactive_session(10**5,4,4,4,"AI0 vs. AI0",first_turn='first_player')
    print("The two probabilities for AI0 vs. AI0 game for (4,4,4) board and p1 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))
#    p1,p2=non_interactive_session(10**5,4,4,4,"AI0 vs. AI0",first_turn='second_player')
#    print("The two probabilities for AI0 vs. AI0 game for (4,4,4) board and p2 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))

    p1,p2=non_interactive_session(10**5,4,4,4,"AI2 vs. AI2",first_turn='first_player')
    print("The two probabilities for AI2 vs. AI2 game for (4,4,4) board and p1 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))
#    p1,p2=non_interactive_session(10**5,4,4,4,"AI2 vs. AI2",first_turn='second_player')
#    print("The two probabilities for AI2 vs. AI2 game for (4,4,4) board and p2 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))
    
    p1,p2=non_interactive_session(10**5,4,3,3,"AI0 vs. AI0",first_turn='first_player')
    print("The two probabilities for AI0 vs. AI0 game for (4,3,3) board and p1 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))
#    p1,p2=non_interactive_session(10**5,4,3,3,"AI0 vs. AI0",first_turn='second_player')
#    print("The two probabilities for AI0 vs. AI0 game for (4,3,3) board and p2 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))

    p1,p2=non_interactive_session(10**5,4,3,3,"AI2 vs. AI2",first_turn='first_player')
    print("The two probabilities for AI2 vs. AI2 game for (4,3,3) board and p1 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))
#    p1,p2=non_interactive_session(10**5,4,3,3,"AI2 vs. AI2",first_turn='second_player')
#    print("The two probabilities for AI2 vs. AI2 game for (4,3,3) board and p2 first are p1=P(AI1)={} and p2=P(AI0)={}".format(p1,p2))

    scenario1p1=[]
    scenario1p2=[]
    scenario2p1=[]
    scenario2p2=[]
    
    for i in range(100):
        p1,p2=non_interactive_session(10**5,3,3,3,"AI2 vs. AI1",'random')
        scenario1p1=scenario1p1+[p1]
        scenario1p2=scenario1p2+[p2]
        
        p1,p2=non_interactive_session(10**5,3,3,3,"AI2 vs. AI0",'random')
        scenario2p1=scenario2p1+[p1]
        scenario2p2=scenario2p2+[p2]
        
    plt.hist(scenario1p1)
    plt.show()
    

    plt.hist(scenario1p2)
    plt.show()
    
    
    plt.hist(scenario2p1)
    plt.show()
    
    
    plt.hist(scenario2p2)
    plt.show()
    
