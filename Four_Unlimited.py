from pdb import Restart
import numpy as np
import random
import pygame
import sys
import math

row_size = 6
col_size = 7

P_1 = 0
AI = 1

EMPTY = 0
p1_piece = 1
ai_piece = 2

window_size = 4

def create_board():
	board = np.zeros((row_size,col_size))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[row_size-1][col] == 0

def get_next_open_row(board, col):
	for r in range(row_size):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(col_size-3):
		for r in range(row_size):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(col_size):
		for r in range(row_size-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(col_size-3):
		for r in range(row_size-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(col_size-3):
		for r in range(3, row_size):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
	score = 0
	opp_piece = p1_piece
	if piece == p1_piece:
		opp_piece = ai_piece

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, col_size//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(row_size):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(col_size-3):
			window = row_array[c:c+window_size]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(col_size):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(row_size-3):
			window = col_array[r:r+window_size]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(row_size-3):
		for c in range(col_size-3):
			window = [board[r+i][c+i] for i in range(window_size)]
			score += evaluate_window(window, piece)

	for r in range(row_size-3):
		for c in range(col_size-3):
			window = [board[r+3-i][c+i] for i in range(window_size)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, p1_piece) or winning_move(board, ai_piece) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, ai_piece):
				return (None, 100000000000000)
			elif winning_move(board, p1_piece):
				return (None, -100000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, ai_piece))
	if maximizingPlayer:
		value = -math.inf
		
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, ai_piece)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, p1_piece)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(col_size):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

az_c = (130,193,248)
g_c = (255,255,255)
r_c = (255,77,92,255)
am_c = (244,221,85)
def draw_board(board):
	for c in range(col_size):
		for r in range(row_size):
			pygame.draw.rect(screen, az_c, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, g_c, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(col_size):
		for r in range(row_size):		
			if board[r][c] == p1_piece:
				pygame.draw.circle(screen, r_c, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == ai_piece: 
				pygame.draw.circle(screen, am_c, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 115

width = col_size * SQUARESIZE
height = (row_size+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("arialblack", 90)

turn = random.randint(P_1, AI)

while not game_over:

	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, g_c, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == P_1:
				pygame.draw.circle(screen, r_c, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, g_c, (0,0, width, SQUARESIZE))
			
		
			# Ask for Player 1 Input
			if turn == P_1:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, p1_piece)

					if winning_move(board, p1_piece):
						label = myfont.render("HUMAN is victor!", 2, r_c)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)

					
	# # Ask for Player 2 Input
	if turn == AI and not game_over:				

		
		col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, ai_piece)

			if winning_move(board, ai_piece):
				label = myfont.render("AI is victor!!!", 1, am_c)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)
		