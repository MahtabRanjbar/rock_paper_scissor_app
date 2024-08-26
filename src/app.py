import streamlit as st
from tournament import TournamentManager
from PIL import Image
import base64
import io

def load_images():
    images = {
        'rock': Image.open('images/fist.png'),
        'paper': Image.open('images/hand-paper.png'),
        'scissors': Image.open('images/scissors.png'),
    }
    return images

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def display_choices(player_choice, computer_choice, images):
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-around; align-items: center;">
            <div style="text-align: center;">
                <img src="data:image/png;base64,{image_to_base64(images[player_choice])}" style="width: 100px; height: 100px;"/>
                <p>You chose: {player_choice.capitalize()}</p>
            </div>
            <div style="text-align: center;">
                <img src="data:image/png;base64,{image_to_base64(images[computer_choice])}" style="width: 100px; height: 100px;"/>
                <p>Computer chose: {computer_choice.capitalize()}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def update_scores(winner):
    st.session_state.games_played += 1
    if winner == 'Player':
        st.session_state.wins += 1
    elif winner == 'Computer':
        st.session_state.losses += 1

def display_metrics():
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Games", st.session_state.games_played)
    col2.metric("Wins", st.session_state.wins)
    col3.metric("Losses", st.session_state.losses)

def main():
    st.set_page_config(page_title="Rock, Paper, Scissors", layout="wide")
    
    logo = Image.open('images/logo.png')
    img_str = image_to_base64(logo)

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
            <img src="data:image/png;base64,{img_str}" style="height: 50px; margin-right: 10px;"/>
            <h1 style="margin: 0; font-size: 24px; color: #0e1117;">Rock, Paper, Scissors</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    tournament_manager = TournamentManager()
    images = load_images()

    if 'games_played' not in st.session_state:
        st.session_state.games_played = 0
        st.session_state.wins = 0
        st.session_state.losses = 0
        st.session_state.computer_choice = None
        st.session_state.winner = None

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Make Your Choice")
        choice_col1, choice_col2, choice_col3 = st.columns(3)
        
        with choice_col1:
            rock_button = st.button("🪨 Rock")
        with choice_col2:
            paper_button = st.button("📄 Paper")
        with choice_col3:
            scissors_button = st.button("✂️ Scissors")

        player_choice = None
        if rock_button:
            player_choice = 'rock'
        elif paper_button:
            player_choice = 'paper'
        elif scissors_button:
            player_choice = 'scissors'

        if player_choice:
            computer_choice = tournament_manager.get_computer_choice()
            winner = tournament_manager.decide_winner(player_choice, computer_choice)

            st.session_state.computer_choice = computer_choice
            st.session_state.winner = winner
            update_scores(winner)

            display_choices(player_choice, computer_choice, images)

            if winner == 'Player':
                st.success("🎉 You win!")
            elif winner == 'Computer':
                st.error("💔 Computer wins!")
            else:
                st.info("🤝 It's a tie!")

    with col2:
        st.markdown("### Game Stats")
        display_metrics()

        # Add a reset button
        if st.button("Reset Game"):
            st.session_state.games_played = 0
            st.session_state.wins = 0
            st.session_state.losses = 0
            st.session_state.computer_choice = None
            st.session_state.winner = None
            st.rerun()

if __name__ == '__main__':
    main()