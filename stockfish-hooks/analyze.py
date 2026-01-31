import chess
import chess.pgn
import chess.engine
import io
import time

pgn = open(f"lichess_{uname}_2026-01-31.pgn")

games = []
game = chess.pgn.read_game(pgn)
while game is not None:
    games.append(str(game))
    game = chess.pgn.read_game(pgn)


def process_game(game_str, debug=False):
    starttime = time.time()
    eng = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-ubuntu-x86-64-avx2")
    game = chess.pgn.read_game(io.StringIO(game_str))
    print("Starting processing of", game.headers["Date"] ,game.headers["UTCTime"])
    #mainly analysis
    color = None
    if game.headers["Black"] == uname:
        color = "black"
    elif game.headers["White"] == uname:
        color = "white"
    else:
        assert(False)

    for node in game.mainline():
        info = eng.analyse(node.board(), chess.engine.Limit(depth=20))
        score_pov = info["score"]
        if not score_pov.is_mate():
            if info["time"] < 0.1 and info["depth"] < 50:
                info = eng.analyse(node.board(), chess.engine.Limit(time=1))
            
        score_me = (score_pov.white() if color == "white" else score_pov.black())
        node.set_eval(score_pov,info["depth"])
        if debug:
            print(str((node.ply()+1)//2)+("." if node.ply() % 2 == 1 else "..."), node.san(), score_me, info["depth"], info.get("time",None))
    print("Done processing of", game.headers["Date"] ,game.headers["UTCTime"], "Time:", time.time()-starttime)
    eng.close()
    return str(game)

#print(process_game(str(games[2], debug=True)))

import concurrent.futures
done_games = []
def run():
    outfile = open("processed-games", "w")
    print("Starting runs")
    with concurrent.futures.ProcessPoolExecutor(max_workers=24) as executor:
        for value in executor.map(process_game, games):
            done_games.append(value)
            print(f"Done! {len(done_games)}/{len(games)}")
            print(value, file=outfile, end="\n\n")
        print("Done!")
    outfile.close()

if __name__ == "__main__":
    run()
print("Exited!")
