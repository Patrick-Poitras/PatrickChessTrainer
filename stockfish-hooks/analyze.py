import chess
import chess.pgn
import chess.engine
import io
import time
import concurrent.futures

pgn_path = f"lichess_{uname}_2026-01-31.pgn"
stockfish_path = "stockfish/stockfish-ubuntu-x86-64-avx2"

# debugging for games that don't return
debug_when_clogged = True
clogging_threshold = 900 # games start printing debug info after 15 mins

def read_all_games(path):
    pgn = open(path)
    games = []
    game = chess.pgn.read_game(pgn)

    # limit for debugging. -1 disables the limit
    limit = -1
    while game is not None:
        games.append(str(game))
        game = chess.pgn.read_game(pgn)
        if limit == len(games):
            break
    return games

games = read_all_games(pgn_path)

def process_game(game_str, debug=False):
    starttime = time.time()
    eng = chess.engine.SimpleEngine.popen_uci(stockfish_path)
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
        info = eng.analyse(node.board(), chess.engine.Limit(depth=20, time=15))
        score_pov = info["score"]
        if not score_pov.is_mate():
            if info.get("time", 9999) < 0.1:
                info = eng.analyse(node.board(), chess.engine.Limit(time=1, depth=50))
            
        score_me = (score_pov.white() if color == "white" else score_pov.black())
        node.set_eval(score_pov, info["depth"])
        if time.time() - starttime > clogging_threshold:
            debug = debug_when_clogged
        if debug:
            move_str = str((node.ply()+1)//2)+("." if node.ply() % 2 == 1 else "...") 
            print(move_str, node.san(), score_me, info["depth"], info.get("time", None))
    print("Done processing of", game.headers["Date"] ,game.headers["UTCTime"], "Time:", time.time()-starttime)
    eng.close()
    return str(game)

#print(process_game(str(games[28]), debug=True))

done_games = []
def run():
    outfile = open("processed-games", "w")
    print("Starting runs")
    starttime = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=24) as executor:
        for value in executor.map(process_game, games):
            done_games.append(value)
            speed = len(done_games)/(time.time()-starttime)
            print(value, file=outfile, end="\n\n")
            print(f"Done indexing! {len(done_games)}/{len(games)}", "Time remaining:", (len(games)-len(done_games))/speed)
        print("All complete!")
    outfile.close()

if __name__ == "__main__":
    run()
print("Exited!")
