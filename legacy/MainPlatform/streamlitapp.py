import streamlit as st
import subprocess
import sys

def main():
    st.title("Simple Game Selector with Reinforcement Learning")

    game_choice = st.selectbox("Choose a game mode:", ["Select a mode", "Play Flappy Bird", "Play Snake", "Play Bouncy Ball", "RL Flappy Bird", "RL Snake", "RL Bouncy Ball"])

    if game_choice == "Play Flappy Bird":
        if st.button("Play Flappy Bird"):
            run_game("flappy_bird.py")
    elif game_choice == "Play Snake":
        if st.button("Play Snake"):
            run_game("snake.py")
    elif game_choice == "Play Bouncy Ball":
        if st.button("Play Bouncy Ball"):
            run_game("bouncy_ball.py")
    elif game_choice == "RL Flappy Bird":
        if st.button("Run RL for Flappy Bird"):
            run_rl("flappy_bird_rl.py")
    elif game_choice == "RL Snake":
        if st.button("Run RL for Snake"):
            run_rl("snake_rl.py")
    elif game_choice == "RL Bouncy Ball":
        if st.button("Run RL for Bouncy Ball"):
            run_rl("bouncy_ball_rl.py")

def run_game(game_script):
    subprocess.run([sys.executable, game_script])

def run_rl(rl_script):
    subprocess.run([sys.executable, rl_script])

if __name__ == "__main__":
    main()
