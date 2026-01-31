import chess
import chess.pgn
import chess.engine

pgn = open(f"lichess_{uname}_2026-01-31.pgn")

game = chess.pgn.read_game(pgn)

board = game.board()
eng = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-ubuntu-x86-64-avx2")
eng.configure({"Threads": 1})

def process_game(game):
    color = None
    if game.headers["Black"] == uname:
        color = "black"
    elif game.headers["White"] == uname:
        color = "white"
    else:
        assert(False)
    print(game.headers["Black"])
    for node in game.mainline():
        info = eng.analyse(node.board(), chess.engine.Limit(depth=20))
        score_pov = info["score"]
        if info["time"] < 0.1:
            info = eng.analyse(node.board(), chess.engine.Limit(time=1))
        score_me = (score_pov.white() if color == "white" else score_pov.black())
        a_300 = 0
        if score_me >= chess.engine.Cp(300):
            print("Above 300!")
            a_300 = 0
        print(str((node.ply()+1)//2)+("." if node.ply() % 2 == 1 else "..."), node.san(), score_me, info["depth"], info["time"])

process_game(game)
