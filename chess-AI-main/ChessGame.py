"""
This is our main driver file. It will be responsible for handling user input and displaying the current
GameState object
"""
import pygame as p
import ChessEngine
import SmartMoveFinder
from ChessMenu import MainMenu

BOARD_WIDTH = BOARD_HEIGHT = 512  # 400 is another option
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8  # dimension of a chess board are 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15  # for animation later on
IMAGES = {}

"""
The main driver for out code. This will handling user input and updating the graphics

"""


class ChessGame:
    def __init__(self):
        p.init()
        self.DISPLAY_W, self.DISPLAY_H = 762, 512
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.display = p.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = p.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        # self.font_name = '8-BIT WONDER.TTF'
        self.font_name = p.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
        self.clock = p.time.Clock()
        self.screen.fill(p.Color('white'))
        self.moveLogFont = p.font.SysFont('Arial', 14, False, False)
        self.gs = ChessEngine.GameState()
        self.validMoves = self.gs.getValidMoves()
        self.moveMade = False  # flag varibale for when a move is made
        self.animate = False  # flag variable for when we should animate a move
        self.loadImages()  # only do this once, before the while loop
        self.running = True
        self.sqSelected = ()  # no square is selected, keep track of last click of user
        self.playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
        self.gameOver = False
        self.playerOne = True  # if a human is playing white, then this will be True. If AI is playing , then false
        self.playerTwo = False  # Same as above but for black
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu

    """
    Initialize a global dictionary of images. This will be called exactly once in the main
    """

    def loadImages(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # Note: we can access an image by saying 'IMAGES['wp']'

    def game_loop(self):
        while self.running:
            humanTurn = (self.gs.whiteToMove and self.playerOne) or (not self.gs.whiteToMove and self.playerTwo)
            for e in p.event.get():
                if e.type == p.QUIT:
                    self.running = False
                # mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not self.gameOver and humanTurn:
                        location = p.mouse.get_pos()  # (x, y) location of mouse
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        if self.sqSelected == (row, col) or col >= 8:  # the user clicked the same square twice
                            self.sqSelected = ()  # deselect
                            playerClicks = []  # clear player clicks
                        else:
                            self.sqSelected = (row, col)
                            self.playerClicks.append(self.sqSelected)  # append for both 1st and 2st clicks
                        if len(self.playerClicks) == 2:  # after 2nd click
                            move = ChessEngine.Move(self.playerClicks[0], self.playerClicks[1], self.gs.board, self.gs.hashValue)
                            print(move.getChessNotation())
                            for i in range(len(self.validMoves)):
                                if move == self.validMoves[i]:
                                    self.gs.makeMove(self.validMoves[i])
                                    self.moveMade = True
                                    self.animate = True
                                    self.sqSelected = ()  # reset user clicks
                                    self.playerClicks = []
                                if not self.moveMade:
                                    self.playerClicks = [self.sqSelected]
                # key handler
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:  # undo when 'z' is pressed
                        self.gs.undoMove()
                        self.moveMade = True
                        self.animate = False
                        self.gameOver = False
                    if e.key == p.K_r:  # reset the board when 'r' is pressed
                        self.gs = ChessEngine.GameState()
                        self.validMoves = self.gs.getValidMoves()
                        self.sqSelected = []
                        self.playerClicks = []
                        self.moveMade = False
                        self.animate = False
                        self.gameOver = False

            # AI move finder
            if not self.gameOver and not humanTurn:
                AIMove = SmartMoveFinder.findBestMoveMinMax(self.gs, self.validMoves)
                if AIMove is None:
                    AIMove = SmartMoveFinder.findRandomMove(self.validMoves)
                self.gs.makeMove(AIMove)
                self.moveMade = True
                self.animate = True

            if self.moveMade:
                if self.animate:
                    self.animateMove(self.gs.moveLog[-1], self.screen, self.gs.board, self.clock)
                self.validMoves = self.gs.getValidMoves()
                self.moveMade = False
                self.animate = False

            self.drawGameState(self.screen, self.gs, self.validMoves, self.sqSelected, self.moveLogFont)

            if self.gs.checkMate:
                self.gameOver = True
                text = 'Stalemate' if self.gs.staleMate else 'Black wins by checkmate' if self.gs.whiteToMove else 'White wins by checkmate'
                self.drawEndGameText(self.screen, text)

            self.clock.tick(MAX_FPS)
            p.display.flip()
            self.reset_keys()


    '''
    Hightlight square selected and moves for piece selected
    '''

    def highlightSquares(self, screen, gs, validMoves, sqSelected):
        if sqSelected != ():
            r, c = sqSelected
            if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # sqSelected is a piece that can be moved
                # highlight selected square
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)  # transperancy value -> 0 transparent; 255 opaque
                s.fill(p.Color('blue'))
                screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
                # hightlight moves form that square
                s.fill(p.Color('yellow'))
                for move in validMoves:
                    if move.startRow == r and move.startCol == c:
                        screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

    '''
     Responsible for all the graphics within a current game state
     '''

    def drawGameState(self, screen, gs, validMoves, sqSelected, moveLogFont):
        self.drawBoard(screen)  # draw squares on the board
        self.highlightSquares(screen, gs, validMoves, sqSelected)
        self.drawPieces(screen, gs.board)  # draw pieces on top of those squares
        self.drawMoveLog(screen, gs, moveLogFont)

    """
    Draw the squares on the board.
    """

    def drawBoard(self, screen):
        global colors
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = colors[(r + c) % 2]
                p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    """
    Draw the pieces on the board using the current GameState.board
    """

    def drawPieces(self, screen, board):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = board[r][c]
                if piece != "--":  # not empty squares
                    screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    '''
    Draws the move log
    '''

    def drawMoveLog(self, screen, gs, font):
        moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
        p.draw.rect(screen, p.Color("black"), moveLogRect)
        moveLog = gs.moveLog
        moveTexts = []
        for i in range(0, len(moveLog), 2):
            moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + " "
            if i + 1 < len(moveLog):  # make sure black made a move
                moveString += str(moveLog[i + 1]) + "  "
            moveTexts.append(moveString)

        movePerRow = 3
        padding = 5
        lineSpacing = 2
        textY = padding
        for i in range(0, len(moveTexts), movePerRow):
            text = ""
            for j in range(movePerRow):
                if i + j < len(moveTexts):
                    text += moveTexts[i + j]
            textObject = font.render(text, True, p.Color('white'))
            textLocation = moveLogRect.move(padding, textY)
            screen.blit(textObject, textLocation)
            textY += textObject.get_height() + lineSpacing

    '''
    Animating a move
    '''

    def animateMove(self, move, screen, board, clock):
        global colors
        dR = move.endRow - move.startRow
        dC = move.endCol - move.startCol
        framesPreSquare = 10  # frames to move on square
        frameCount = (abs(dR) + abs(dC)) * framesPreSquare
        for frame in range(frameCount + 1):
            r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
            self.drawBoard(screen)
            self.drawPieces(screen, board)
            # erase the piece moved from its ending square
            color = colors[(move.endRow + move.endCol) % 2]
            endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, endSquare)
            # draw captured piece onto rectangle
            if move.pieceCaptured != '--':
                if move.isEnpassantMove:
                    enPassantRow = (move.endRow + 1) if move.pieceCaptured[0] == 'b' else move.endRow - 1
                    endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)

                screen.blit(IMAGES[move.pieceCaptured], endSquare)
            # draw moving piece
            screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            p.display.flip()
            clock.tick(70)

    def drawEndGameText(self, screen, text):
        font = p.font.SysFont('Helvitca', 32, True, False)
        textObject = font.render(text, 0, p.Color('Gray'))
        textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
            BOARD_WIDTH / 2 - textObject.get_width() / 2,
            BOARD_HEIGHT / 2 - textObject.get_height() / 2)
        screen.blit(textObject, textLocation)
        textObject = font.render(text, 0, p.Color('Black'))
        screen.blit(textObject, textLocation.move(2, 2))

    def check_events(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    self.START_KEY = True
                if event.key == p.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == p.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == p.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = p.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


if __name__ == '__main__':
    g = ChessGame()

    g.curr_menu.display_menu()
    g.game_loop()
