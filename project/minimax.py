import chess
from stockfish import Stockfish
from util import to_list

INFINITY = 5000
ENV_PATH = 'stockfish_14.1_win_x64_avx2.exe'


cache = {}


def minimax(game: chess.Board, depth, max_depth):
    state = f'{game.fen()}{depth % 2}'

    if state in cache:
        return cache[state]

    if depth == max_depth:
        fen_position = game.fen()

        agent = Stockfish(ENV_PATH, parameters={'Threads': 1})
        agent.set_position()
        agent.set_depth(1)
        agent.set_fen_position(fen_position)

        _eval = agent.get_evaluation()

        cache[state] = _eval
        return _eval

    best_val = -INFINITY
    best_eval = None

    moves = to_list(game.legal_moves)
    for move in moves:
        game.push(chess.Move.from_uci(move))
        _eval = minimax(game, depth + 1, max_depth)
        game.pop()

        if _eval['type'] == 'mate':
            if depth % 2 == 0:
                _eval['value'] = 10000
            if depth % 2 == 1:
                _eval['value'] = -10000

        value = _eval['value']

        if value > best_val:
            best_val = value
            best_eval = _eval
            best_eval['move'] = move

    cache[state] = best_eval
    return best_eval
