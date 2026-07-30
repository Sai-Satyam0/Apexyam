
import chess
import chess.svg
import chess.engine
import streamlit as st

# =========================
# STOCKFISH PATH
# =========================

STOCKFISH_PATH = "/usr/games/stockfish"


# =========================
# INIT GAME
# =========================

def init_game():

    board = chess.Board()

    state = {
        "board": board,
        "move_history": [],
        "game_over": False,
        "result": None
    }

    return state


# =========================
# PLAYER MOVE
# =========================

def player_move(state, move):

    try:

        board = state["board"]

        # =========================
        # ONLY WHITE CAN PLAY
        # =========================

        if board.turn != chess.WHITE:

            st.error(
                "Wait for AI move!"
            )

            return state

        move = move.strip().lower()

        chess_move = chess.Move.from_uci(
            move
        )

        if chess_move not in board.legal_moves:

            st.error(
                "Illegal move!"
            )

            return state

        # =========================
        # PLAYER MOVE
        # =========================

        board.push(chess_move)

        state["move_history"].append(
            f"Player: {move}"
        )

        if board.is_game_over():

            state["game_over"] = True

            state["result"] = board.result()

        return state

    except Exception as e:

        st.error(
            f"Move Error: {e}"
        )

        return state



# =========================
# AI MOVE
# =========================

def ai_move(state, difficulty):

    try:

        board = state["board"]

        # =========================
        # ONLY BLACK AI MOVES
        # =========================

        if board.turn != chess.BLACK:

            return state

        depth_map = {
            "Easy": 1,
            "Medium": 5,
            "Hard": 10
        }

        depth = depth_map.get(
            difficulty,
            5
        )

        engine = chess.engine.SimpleEngine.popen_uci(
            STOCKFISH_PATH
        )

        result = engine.play(
            board,
            chess.engine.Limit(depth=depth)
        )

        ai_move = result.move

        board.push(ai_move)

        state["move_history"].append(
            f"AI ({difficulty}): {ai_move}"
        )

        engine.quit()

        if board.is_game_over():

            state["game_over"] = True

            state["result"] = board.result()

        return state

    except Exception as e:

        st.error(
            f"AI Error: {e}"
        )

        return state

# =========================
# BOARD SVG
# =========================

def get_board_svg(state):

    try:

        board = state["board"]

        svg = chess.svg.board(
            board=board,
            size=500,
            flipped=False
        )

        return svg

    except Exception as e:

        st.error(f"Board Error: {e}")

        return None
