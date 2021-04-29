from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
from flask import Flask, render_template, request, redirect, url_for


# ベストプレイヤーのモデルの読み込み
model = load_model('./model/best.h5')



class BrowsPlay:
    def __init__(self):
        self.state = State()
        self.next_action = pv_mcts_action(model, 0.0)

    # 人間のターン
    def turn_of_human(self, action):
        # ゲーム終了時
        if self.state.is_done():
            self.state = State()
            redirect(url_for("done"))
            

        # 先手でない時
        if not self.state.is_first_player():
            return


        # 合法手でない時
        if not (action in self.state.legal_actions()):
            return

        # 次の状態の取得
        self.state = self.state.next(action)

        

    # AIのターン
    def turn_of_ai(self):
        # ゲーム終了時
        if self.state.is_done():
            self.state = State()
            redirect(url_for("done"))
            
        
        # 行動の取得
        action = self.next_action(self.state)

        # 次の状態の取得
        self.state = self.state.next(action)
        


bp = BrowsPlay()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        if self.state.is_done():
            self.state = State()
            redirect(url_for("done"))
        return render_template("index.html", your_turn = bp.state.is_first_player(), statements = bp.state.get_state())
    
    if request.method == "POST":
        if self.state.is_done():
            self.state = State()
            redirect(url_for("done"))
        
        if request.form["col"]:
            action = int(request.form["col"])
            bp.turn_of_human(action)
            bp.turn_of_ai()
            print(bp.state)

        return render_template("index.html", your_turn = bp.state.is_first_player(), statements = bp.state.get_state())

#試合終了時
@app.route("/done", methods=["GET", "POST"])
def done():
    your_turn = bp.state.is_first_player()
    results = [bp.state.is_lose(), bp.state.is_draw()]
    if bp.state.is_draw():
        result = "引き分け"
    elif (your_turn and bp.state.is_lose()) or not your_turn and all(not i for i in results):
        result = "あなたの負け"
    else:
        result = "あなたの勝ち"
    return render_template("done.html", result=result, statements = bp.state.get_state())
    


if __name__ == "__main__":
    app.run(debug=True)