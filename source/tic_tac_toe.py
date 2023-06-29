import pygame, sys
import numpy as np
import ctypes
pygame.init()

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 3
WIN_LINE_WIDTH = 5
BOARD_SIZE = 20
BOARD_SIZE = 20
SQUARE_SIZE = 30
CIRCLE_RADIUS = 10
CIRCLE_WIDTH = 3
CROSS_WIDTH = 3
SPACE = 23
# board = [[int(0)] * BOARD_SIZE] * BOARD_SIZE
winScore = 1000000000

RED = (255, 0, 0)
BackGround_COLOR = (0, 0, 0)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (255, 130, 71)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BackGround_COLOR)

# Hàm kẻ bảng bàn cờ
def draw_lines():
    for j in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, j * SQUARE_SIZE), (WIDTH, j * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Hàm vẽ XO
x_img = pygame.transform.smoothscale(pygame.image.load("x_icon.png").convert(),(28,28))
o_img = pygame.transform.smoothscale(pygame.image.load("o_icon.png").convert(),(28,28))

def draw_figures(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (
                    int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS,
                                   CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
# Đánh số 1, 2 trong matrix board
def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0

def returnMove(listMove):
    global moves
    for move in listMove:
        moves.remove((move[0], move[1]))

def available_moves(matrix):
    moves = list()
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if matrix[row][col] != 0:
                if row + 1 < BOARD_SIZE:
                    if col - 1 >= 0 and matrix[row+1][col-1] == 0 and (row+1, col-1) not in moves:
                        moves.append((row + 1, col - 1))
                    if col + 1 < BOARD_SIZE and matrix[row+1][col+1] == 0 and (row+1, col+1) not in moves:
                        moves.append((row + 1, col + 1))
                    if matrix[row+1][col] == 0 and (row+1, col) not in moves:
                        moves.append((row+1, col))
                if row - 1 >= 0:
                    if col - 1 >= 0 and matrix[row - 1][col - 1] == 0 and (row - 1, col - 1) not in moves:
                        moves.append((row - 1, col - 1))
                    if col + 1 < BOARD_SIZE and matrix[row - 1][col + 1] == 0 and (row - 1, col + 1) not in moves:
                        moves.append((row - 1, col + 1))
                    if matrix[row - 1][col] == 0 and (row - 1, col) not in moves:
                        moves.append((row - 1, col))
                if col - 1 >= 0 and matrix[row][col-1] == 0 and (row, col-1) not in moves:
                    moves.append((row, col-1))
                if col + 1 < BOARD_SIZE and matrix[row][col+1] == 0 and (row, col+1) not in moves:
                    moves.append((row, col+1))
    return moves

def printBoard(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            print(board[row][col], end=" ")
        print()

# Hàm dùng giải thuật minimax - alpha-beta
def minimax(matrix, depth, maximizingPlayer):
    return alphabeta(matrix, depth, -10000000000, 10000000000, maximizingPlayer)


def alphabeta(matrix, depth, alpha, beta, maximazingPlayer):
    moves = available_moves(matrix)
    if depth == 0 or len(moves) == 0:
        return [value(matrix), None, None]
    bestMove = [None, None, None]
    if maximazingPlayer:
        bestMove[0] = -10000000000
        for move in moves:
            matrix[move[0]][move[1]] = 1
            tmp = alphabeta(matrix, depth-1, alpha, beta, False)
            matrix[move[0]][move[1]] = 0
            if tmp[0] > alpha:
                alpha = tmp[0]
                bestMove = tmp
                bestMove[1] = move[0]
                bestMove[2] = move[1]
            if tmp[0] >= beta:
                return tmp
    else:
        bestMove[0] = 10000000000
        bestMove[1] = moves[0][0]
        bestMove[2] = moves[0][1]
        for move in moves:
            matrix[move[0]][move[1]] = 2
            tmp = alphabeta(matrix, depth - 1, alpha, beta, True)
            matrix[move[0]][move[1]] = 0
            if tmp[0] < beta:
                beta = tmp[0]
                bestMove = tmp
                bestMove[1] = move[0]
                bestMove[2] = move[1]
            if tmp[0] <= alpha:
                return tmp

    return bestMove

def restart():
    screen.fill(BackGround_COLOR)
    draw_lines()
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            board[row][col] = int(0)

# Hàm đánh giá trạng thái bàn cờ
def evaluateBoard(matrix, player):
    return evaluateDiagonal(matrix, player) + evaluateHorizontal(matrix, player) + evaluateVertical(matrix, player)

#Hàm đánh giá hàng ngang
def evaluateHorizontal(matrix, player):
    consecutive = 0
    blocks = 2
    score = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if matrix[row][col] == (2 if player else 1):
                consecutive += 1
            elif matrix[row][col] == 0:
                if consecutive > 0:
                    blocks -= 1
                    score += getValue(consecutive, blocks, True if player else False)
                    consecutive = 0
                    blocks = 1
                else:
                    blocks = 1
            elif consecutive > 0:
                score += getValue(consecutive, blocks, True if player else False)
                blocks = 2
                consecutive = 0
            else:
                blocks = 2
        if consecutive > 0:
            score += getValue(consecutive, blocks, True if player else False)
        blocks = 2
        consecutive = 0
    return score

# Hàm đánh giá hàng dọc
def evaluateVertical(matrix, player):
    consecutive = 0
    blocks = 2
    score = 0
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE):
            if matrix[row][col] == (2 if player else 1):
                consecutive += 1
            elif matrix[row][col] == 0:
                if consecutive > 0:
                    blocks -= 1
                    score += getValue(consecutive, blocks, True if player else False)
                    consecutive = 0
                    blocks = 1
                else:
                    blocks = 1
            elif consecutive > 0:
                score += getValue(consecutive, blocks, True if player else False)
                blocks = 2
                consecutive = 0
            else:
                blocks = 2
        if consecutive > 0:
            score += getValue(consecutive, blocks, True if player else False)
        blocks = 2
        consecutive = 0
    return score

# Hàm đánh giá đường chéo
def evaluateDiagonal(matrix, player):
    consecutive = 0
    blocks = 2
    score = 0

    # Đánh giá đường chéo chính
    for i in range(1 - BOARD_SIZE, BOARD_SIZE):
        jStart = max(i, 0)
        jEnd = min(i + BOARD_SIZE - 1, BOARD_SIZE - 1)
        for j in range(jStart, jEnd + 1):
            k = j - i
            if matrix[j][k] == (2 if player else 1):
                consecutive += 1
            elif matrix[j][k] == 0:
                if consecutive > 0:
                    blocks -= 1
                    score += getValue(consecutive, blocks, True if player else False)
                    consecutive = 0
                    blocks = 1
                else:
                    blocks = 1
            elif consecutive > 0:
                score += getValue(consecutive, blocks, True if player else False)
                blocks = 2
                consecutive = 0
            else:
                blocks = 2
        if consecutive > 0:
            score += getValue(consecutive, blocks, True if player else False)
        blocks = 2
        consecutive = 0

    # Đánh giá đường chéo phụ
    for i in range(2 * (BOARD_SIZE - 1) + 1):
        jStart = max(0, i - BOARD_SIZE + 1)
        jEnd = min(BOARD_SIZE - 1, i)
        for j in range(jStart, jEnd + 1):
            k = i - j
            if matrix[j][k] == (2 if player else 1):
                consecutive += 1
            elif matrix[j][k] == 0:
                if consecutive > 0:
                    blocks -= 1
                    score += getValue(consecutive, blocks, True if player else False)
                    consecutive = 0
                    blocks = 1
                else:
                    blocks = 1
            elif consecutive > 0:
                score += getValue(consecutive, blocks, True if player else False)
                blocks = 2
                consecutive = 0
            else:
                blocks = 2
        if consecutive > 0:
            score += getValue(consecutive, blocks, True if player else False)
        blocks = 2
        consecutive = 0
    return score

# Hàm tính điểm cho mỗi node
def getValue(count, blocks, player):
    if count >= 5:
        return -1000000000*2 if player else 1000000000*2
    if count < 5 and blocks == 2:
        return 0
    if count == 4:
        if blocks == 1:
            return -1000000 if player else 1000000
        else:
            return -1000000000 if player else 1000000000
    elif count == 3:
        if blocks == 1:
            return -10000 if player else 10000
        elif blocks == 0:
            return -100000 if player else 100000
    elif count == 2:
        if blocks == 1:
            return -100 if player else 100
        elif blocks == 0:
            return -1000 if player else 1000
    elif count == 1:
        if blocks == 1:
            return -1 if player else 1
        elif blocks == 0:
            return -10 if player else 10


def value(matrix):
    player = evaluateBoard(matrix, True)
    computer = evaluateBoard(matrix, False)
    if player <= -2000000000:
        return player
    if computer >= 2000000000:
        return computer
    if computer >= 1000000000 and player > -1000000000:
        return computer
    if player <= -100000:
        return player
    if computer >= 10000 and player > -100000:
        return computer
    return computer

# Hàm tìm nước đi thắng gần nhất(độ sâu là 1)
def searchWinMove(matrix):
    moves = available_moves(matrix)
    res = list()
    ok = 0
    for move in moves:
        matrix[move[0]][move[1]] = 1
        if evaluateBoard(matrix, False) >= 2000000000:
            res.append(move[0])
            res.append(move[1])
            ok = 1
        if ok == 1:
            break
        matrix[move[0]][move[1]] = 0
    if ok == 1:
        return res
    else:
        return None

#Hàm tìm nước thua gần nhất ( độ sâu là 1)
def searchLoseMove(matrix):
    moves = available_moves(matrix)
    res = list()
    ok = 0
    for move in moves:
        matrix[move[0]][move[1]] = 2
        if evaluateBoard(matrix, True) <= -2000000000:
            res.append(move[0])
            res.append(move[1])
            ok = 1
        matrix[move[0]][move[1]] = 0
        if ok == 1:
            break
    if ok == 1:
        return res
    else:
        return None

# Hàm checkWin
def checkWin(matrix, player):
    for row in range(BOARD_SIZE):
        consecutiveRow = 0
        consecutiveCol = 0
        for col in range(BOARD_SIZE):
            if matrix[row][col] == (2 if player else 1):
                consecutiveRow += 1
            elif consecutiveRow >= 5:
                return True
            if matrix[col][row] == (2 if player else 1):
                consecutiveCol += 1
            elif consecutiveCol >= 5:
                return True
        if consecutiveRow >= 5:
            return True
        if consecutiveCol >= 5:
            return True

        # Đánh giá đường chéo chính
        for i in range(1 - BOARD_SIZE, BOARD_SIZE):
            jStart = max(i, 0)
            jEnd = min(i + BOARD_SIZE - 1, BOARD_SIZE - 1)
            consecutive = 0
            for j in range(jStart, jEnd + 1):
                k = j - i
                if matrix[j][k] == (2 if player else 1):
                    consecutive += 1
                elif consecutive >= 5:
                    return True
            if consecutive >= 5:
                return True


        # Đánh giá đường chéo phụ
        for i in range(2 * (BOARD_SIZE - 1) + 1):
            jStart = max(0, i - BOARD_SIZE + 1)
            jEnd = min(BOARD_SIZE - 1, i)
            consecutive = 0
            for j in range(jStart, jEnd + 1):
                k = i - j
                if matrix[j][k] == (2 if player else 1):
                    consecutive += 1
                elif consecutive >= 5:
                    return True
            if consecutive >= 5:
                return True

    return False

player = 2
game_over = False

if __name__ == '__main__':
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    draw_lines()
    WS_EX_TOPMOST = 0x40000
    windowTitle = "Message"
    message = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)

                    board[clicked_row][clicked_col] = player
                    if checkWin(board, True):
                        print("Bạn win")
                        message = "       Bạn thắng.       "
                        game_over = True
                    else:
                        player = player % 2 + 1
                        winMove =searchWinMove(board)
                        loseMove = searchLoseMove(board)
                        if winMove != None:
                            mark_square(winMove[0], winMove[1], player)
                            board[winMove[0]][winMove[1]] = 1
                            print("AI win")
                            message = "       Máy thắng.       "
                            game_over = True
                        elif loseMove != None:
                            mark_square(loseMove[0], loseMove[1], player)
                            board[loseMove[0]][loseMove[1]] = 1
                        else:
                            bestMove = minimax(board, 3, True)
                            print("best move", bestMove)
                            if bestMove[1] != None and available_square(bestMove[1], bestMove[2]):
                                mark_square(bestMove[1], bestMove[2], player)
                                board[bestMove[1]][bestMove[2]] = 1
                            else:
                                message = "       Hòa.       "
                                game_over = True
                        draw_figures(board)
                        # printBoard(board)
                        player = player % 2 + 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    player = 1
                    game_over = False
            pygame.display.update()
            if game_over == True:
                ctypes.windll.user32.MessageBoxExW(None, message, windowTitle, WS_EX_TOPMOST)
                break
        if game_over == True:
            break