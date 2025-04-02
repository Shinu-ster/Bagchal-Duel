import numpy as np

# class Move: 
#     def __init__(self):


class Move:
    def __init__(self,board):
       self.board = board
        


    def is_valid_move(self,from_pos,to_pos,player_turn):
        

        from_x , from_y = from_pos
        to_x, to_y = to_pos

        print("move is valid from ",from_x,from_y , "to ",to_x,to_y,"Player turn ",player_turn)
        piece_at_destination = self.board.get_piece_at(to_x,to_y)
        if player_turn == False: # Turn of Tiger
            if piece_at_destination is not None and piece_at_destination == 1 or piece_at_destination == 2:
                print("Invalid tiger move piece exists in the node")
                return False
            else:
                return True
        else: # Turn of Goat
            if piece_at_destination is not None and piece_at_destination == 2 or piece_at_destination == 1:
                print("Invalid Goat move piece exists in the node")
                return False
            else:
                return True
                

        # if piece_at_destination is not None and piece_at_destination != 0:
        #     print("Invalid Move node occupied")
        #     return False
        # else:
        #     print("Node empty piece can move")
        #     return True

