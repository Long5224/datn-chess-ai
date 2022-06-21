import random
import TranspositionTable

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

piecePositionScores = {"N": knightScores, "Q": queenScores, "B": bishopScores, "R": rookScores, "bp": blackPawnScores,
                       "wp": whitePawnScores}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

NO_HASH = 100000

HASH_EXACT = 0
HASH_ALPHA = 1
HASH_BETA = 2


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


'''
Find the best move based on material alone
'''


def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = -CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                if gs.checkMate:
                    score = -turnMultiplier * CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


'''
Helper method to make first recursive call
'''


def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegaMaxAlphaBetaTT(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    aspiration(gs, validMoves, DEPTH, -3, 100, 1 if gs.whiteToMove else -1)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:  # pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def findMoveNegaMaxAlphaBetaQuiescene(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return quiescene(gs, validMoves, alpha, beta, turnMultiplier)

    # move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBetaQuiescene(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:  # pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def findMoveNegaMaxAlphaBetaTT(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    alphaOrig = alpha

    # Transposition Table Lookup
    hashEntry = TranspositionTable.transTable.table.get(gs.hashValue)
    if hashEntry and hashEntry.depth >= depth:
        if hashEntry.scoreType == TranspositionTable.transTable.EXACT_SCORE:
            TranspositionTable.transTable.hits = TranspositionTable.transTable.hits + 1
            return hashEntry.score
        if hashEntry.scoreType == TranspositionTable.transTable.LOWER_BOUND_SCORE:
            alpha = max(alpha, hashEntry.score)
        elif hashEntry.flag == HASH_BETA:
            beta = min(hashEntry.score, beta)
        if alpha >= beta:
            return hashEntry.score

    newEntry = False
    if not hashEntry:
        hashEntry = TranspositionTable.transTableEntry()
        hashEntry.zobristHash = gs.hashValue
        newEntry = True
    hashEntry.depth = depth
    hashEntry.move = None

    if depth == 0:
        if TranspositionTable.transTable.size == TranspositionTable.transTable.maxSize and newEntry:
            TranspositionTable.transTable.table.popitem()
            TranspositionTable.transTable.size = TranspositionTable.transTable.size - 1
        TranspositionTable.transTable.table[gs.hashValue] = hashEntry
        TranspositionTable.transTable.size = TranspositionTable.transTable.size + 1
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBetaTT(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                hashEntry.bestMove = move
        gs.undoMove()
        if maxScore > alpha:  # pruning happens
            alpha = maxScore
        if alpha >= beta:
            break

    # Transposition Table Store
    hashEntry.score = maxScore
    if maxScore <= alphaOrig:
        hashEntry.scoreType = TranspositionTable.transTable.UPPER_BOUND_SCORE
    elif maxScore >= beta:
        hashEntry.scoreType = TranspositionTable.transTable.LOWER_BOUND_SCORE
    else:
        hashEntry.scoreType = TranspositionTable.transTable.EXACT_SCORE
    hashEntry.depth = depth
    if TranspositionTable.transTable.size == TranspositionTable.transTable.maxSize and newEntry:
        TranspositionTable.transTable.table.popitem()
        TranspositionTable.transTable.size = TranspositionTable.transTable.size - 1
    TranspositionTable.transTable.table[gs.hashValue] = hashEntry
    return maxScore


"""
Aspiration
"""


def aspiration(gs, validMoves, depth, prevValue, window, turnMultiplier):
    value = findMoveNegaMaxAlphaBetaTT(gs, validMoves, depth, prevValue-window, prevValue+window, turnMultiplier)
    if value >= prevValue+window:   #fail high
        value = findMoveNegaMaxAlphaBetaTT(gs, validMoves, depth, value, +CHECKMATE, turnMultiplier)
    elif value <= prevValue-window: #fail low
        value = findMoveNegaMaxAlphaBetaTT(gs, validMoves, depth, -CHECKMATE, value, turnMultiplier)
    return value


"""
PVS
"""

def PVS(gs, validMoves, depth, alpha, beta, turnMultiplier):
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    nextMoves = gs.getValidMoves()
    value = -PVS(gs, nextMoves, depth - 1, -beta, -alpha)
    for move in validMoves:
        if value >= beta:
            return value
        if value > alpha:
            alpha = value
        nextMoves = gs.getValidMoves(move)
        temp = -PVS(gs, nextMoves, depth - 1, -alpha - 1, -alpha)
        if temp > value: #fail high
            # check if temp value within bounds
            if alpha < temp and temp < beta and depth > 2:
                value = -PVS(-beta, -temp, depth-1)
            else:
                value = temp



'''
A positive score is good for white, a negative score is good for black
'''


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.staleMate:
        return STALEMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                # score it positionally
                piecePositionScore = 0
                if square[1] != "K":  # no position table for king
                    if square[1] == "p":  # for pawn
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:  # for other pieces
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * .1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore * .1
    return score


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score


"""
Quiescene search
"""


def quiescene(gs, validMoves, alpha, beta, turnMultiplier):
    evaluation = turnMultiplier * scoreBoard(gs)

    if evaluation >= beta:
        return beta  # pruning

    # found a better move
    if evaluation > alpha:
        alpha = evaluation

    score = 0

    # loop over moves within a moveList
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -quiescene(gs, nextMoves, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        if score >= beta:
            return beta  # pruning

        # found a better move
        if score > alpha:
            alpha = score
    return alpha
