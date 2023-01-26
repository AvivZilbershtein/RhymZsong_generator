import base64
from login import user_database, get_gallery
from streamlit_option_menu import option_menu
import streamlit as st
from PIL import Image
from request import Request
import pandas as pd

img = Image.open('Untitled.png')
st.set_page_config(page_title="Home"
                   , page_icon=img
                   , layout="centered")


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


set_png_as_page_bg('./Untitled.png')
with st.sidebar:
    st.image(img, width=200)


def main():
    database = user_database()


    with st.sidebar:
        choice = option_menu(menu_title=None,  # required
            options=["Log in", "Sign Up", "Home", "Songs Workshop", "Gallery", "History", "Preferences"],  # required
            menu_icon="cast",  # optional
            default_index=0,  # optional
            styles={"container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "15px"},
                    "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee", },
                    "nav-link-selected": {"background-color": "darkcyan"}, },
        )

    if choice == "Log in":

        st.title("Login")
        st.subheader("Sign in to save your creation!")
        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            result = database.login_users(username, password)
            if result == "success":
                database.get_userdata(database.user_id)
                st.experimental_set_query_params(my_saved_result=database.user_id)
                st.success("Logged In as {}".format(username))
            elif result == "Wrong Password":
                st.warning("Incorrect Password")
            else:
                st.warning("User not found")


    elif choice == "Sign Up":
        st.title("Welcome to the Sign Up page!")
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            response = database.sign_up_users(new_user, new_password)
            if response == "success":
                print("$$$$$$$$$$$$$$$$")
                print(database.user_id)
                database.get_userdata(database.user_id)
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")
            elif response == "username taken":
                st.warning("Username already taken")
            elif response == "empty username":
                st.warning("Username cannot be empty")
            else:
                st.warning("Password cannot be empty")

    elif choice == "Home":
        #st.subheader("Home")
        st.title("Create You Own Songs With RhymZ!")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            move_to_songs_workshop = st.button("Rhyme Now")
            if move_to_songs_workshop:
                st.markdown("Go to the Songs Workshop page")
        with col2:
            move_to_gallery = st.button("Unispired?")
            if move_to_gallery:
                st.markdown("Go to the Gallery page")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            "##### Are you looking for a way to create your own unique songs?\nLook no further! Whether you're a professional musician or just\nstarting out, our song generator will help you create the perfect song.")
        st.markdown("###### So what are you waiting for? Get creative and start making songs today with RhymZ!")

    elif choice == "Songs Workshop":

        st.title("Welcome to the Workshop!")
        st.markdown(
            "##### Here you can quickly and easily create unique lyrics for your next hit.\nAll you need to do is enter some keywords and the application will generate a variety of catchy phrases and lines that fit your style.")

        r = Request()
        song_type = st.radio(label="What type of song?", options=["Limerick", "Poem", "Song"], key="song_type")
        subject = st.text_input(label="What is it about?", key="subject")
        length = st.slider(label="Number of Lines", min_value=1, max_value=20, value=10, key="length")
        genre = st.radio(label="Genre", options=["Rock", "Pop", "Jazz", "Classical", "Country"], key="genre")
        context = st.text_input(label="Context", key="context")

        if "Create Song" not in st.session_state:
            st.session_state["Create Song"] = False

        if "Save Song" not in st.session_state:
            st.session_state["Save Song"] = False

        if "Publish To Gallery" not in st.session_state:
            st.session_state["Publish To Gallery"] = False


        if st.button("Create Song"):
            st.session_state["Create Song"] = not st.session_state["Create Song"]


        if st.session_state["Create Song"]:
            if None not in (subject, length, context) and genre != "" and song_type != "":
                try:

                    app_state = st.experimental_get_query_params()
                    if "my_saved_result" in app_state:
                        user_id = app_state["my_saved_result"][0]
                        database.user_id = user_id
                        line_repetition, randomness, max_line, min_line = database.get_user_settings(database.user_id)
                        r.change_preferences(line_repetition, randomness, max_line, min_line)

                    respond, request = r.get_response(creation_type=song_type, size=length, genre=genre, subject=subject, context=context)
                    st.markdown(f"###### Here is your generated song :smiley:")

                    split_response = respond.split("\n")
                    for line in split_response:
                        st.write(line)

                    #st.session_state["Create Song"] = not st.session_state["Create Song"]

                    if st.button("Save Song"):
                        st.session_state["Save Song"] = not st.session_state["Save Song"]

                    if st.button("Publish To Gallery"):
                        st.session_state["Publish To Gallery"] = not st.session_state["Publish To Gallery"]

                    if st.session_state["Save Song"]:
                        app_state = st.experimental_get_query_params()
                        if "my_saved_result" in app_state:
                            user_id = app_state["my_saved_result"][0]
                            database.user_id = user_id
                            database.get_userdata(user_id)
                            database.update_userdata(request, respond)
                            st.success("Song saved successfully")
                        else:
                            st.warning("Please login to save your song")
                    if st.session_state["Publish To Gallery"]:
                        app_state = st.experimental_get_query_params()
                        if "my_saved_result" in app_state:
                            user_id = app_state["my_saved_result"][0]
                            database.user_id = user_id
                            name=database.get_username(database.user_id)
                            database.add_song_to_gallery(name, request, respond)
                            st.success("Song published successfully")
                        else:
                            st.warning("Please login to publish your song")
                    if st.session_state["Save Song"]:
                        st.session_state["Save Song"] = not st.session_state["Save Song"]
                    if st.session_state["Publish To Gallery"]:
                        st.session_state["Publish To Gallery"] = not st.session_state["Publish To Gallery"]
                except NameError:
                    st.markdown("###### Unfortunately your parameters weren't loaded properly. Try again")

            elif None in (subject, length, context) or genre == "" or song_type == "":
                if subject is not None:
                    st.warning("Please enter a subject")
                if length is not None:
                    st.warning("Please enter a length")
                if context is not None:
                    st.warning("Please enter a context")
                if genre == "":
                    st.warning("Please enter a genre")
                if song_type != "":
                    st.warning("Please enter a song type")
                st.warning("###### Set all your parameters before pressing the `Create Song` button")
        else:
            st.warning("Fill in all the parameters")

    elif choice == "Gallery":
        st.title("Welcome to the Gallery!")
        st.markdown("<p>Here you can find all the latest and greatest songs from our talented users. From upbeat pop to soulful ballads, "
                    "there's something for everyone.<br><b>So come on in and explore the world of music created by our users!</b></p>",
                    unsafe_allow_html=True)
        gallery = get_gallery()
        if len(gallery) == 0:
            st.markdown("<br><h3><center>No songs yet<center></h3>", unsafe_allow_html=True)
        else:
            gallery["Creations"] = gallery["Creations"].apply(lambda x: str(x).replace("\n", "<br>"))
            print(gallery["Creations"])
            for idx, requests in enumerate(gallery["Requests"]):
                words = requests.split(" ")
                for i, word in enumerate(words):
                    if i % 9 == 0 and i != 0:
                        words[i] = word + "<br>"
                new_respone = " ".join(words)
                gallery["Requests"][idx] = new_respone
            table_code = """
                                <table style="width:100%">
                                    <tr>
                                        <th style="text-align: center">Creator</th>
                                        <th style="text-align: center"> Requests</th>
                                        <th style="text-align: center">Generated Creations</th>
                                      </tr>
                                      """
            for i in range(len(gallery)):
                table_code += f"""
                                <tr>
                                    <td style="text-align: center">{gallery["users"][i]}</td>
                                    <td>{gallery["Requests"][i]}</td>
                                    <td>{gallery["Creations"][i]}</td>
                                </tr>
                                """
            table_code += "</table>"
            st.markdown(table_code, unsafe_allow_html=True)

    elif choice == "History":
        st.title("Welcome to your History page!")
        st.markdown("##### Here you can find all the songs you have created using RhymZ")
        app_state = st.experimental_get_query_params()
        if "my_saved_result" in app_state:
            user_id = app_state["my_saved_result"][0]
            database.user_id = user_id
            database.get_userdata(user_id)
            if len(database.user_data) != 0:
                historyDF = database.user_data
                historyDF["response"] = historyDF["response"].apply(lambda x: x.replace("\n", "<br>"))
                for idx, respone in enumerate(historyDF["request"]):
                    words = respone.split(" ")
                    for i, word in enumerate(words):
                        if i%9==0 and i!=0:
                            words[i] = word + "<br>"
                    new_respone = " ".join(words)
                    historyDF["request"][idx] = new_respone

                table_code ="""
                                <table style="width:100%">
                                    <tr>
                                        <th style="text-align: center"> Requests</th>
                                        <th style="text-align: center">Generated Creations</th>
                                      </tr>"""
                for i in range(len(historyDF)):
                    table_code += f"""
                      <tr>
                        <td>{historyDF["request"][i]}</td>
                        <td>{historyDF["response"][i]}</td>
                      </tr>
                    """
                table_code += "</table>"
                st.markdown(table_code, unsafe_allow_html=True)

            else:
                st.markdown("<br><h3><center>You haven't created any songs yet<center></h3>",unsafe_allow_html=True)
        else:
            st.warning("Please login to view your History")

    elif choice == "Preferences":

        st.title("Welcome to the Preferences page!")
        st.markdown("##### Here you can modify the generator according to your needs")
        line_repetition_val, randomness_val, max_line_val, min_line_val= 50, 50, 6, 1
        app_state = st.experimental_get_query_params()
        if "my_saved_result" in app_state:
            user_id = app_state["my_saved_result"][0]
            database.user_id = user_id
            database.get_userdata(user_id)
            line_repetition_val, randomness_val, max_line_val, min_line_val = database.get_user_settings(database.user_id)
            line_repetition_val = int(float(line_repetition_val)*100)
            randomness_val = int(float(randomness_val)*100)
            max_line_val = int(max_line_val)
            min_line_val = int(min_line_val)

        line_repetition = st.slider(label="Line repetition- how much freedom would you give the model to repeat previous lines or words (%)", min_value=0, max_value=100, value=line_repetition_val, key="line_repetition")
        randomness = st.slider(label="Randomness- how much freedom would you give the model to generate random words (%)", min_value=0, max_value=100, value=randomness_val, key="randomness")
        line_repetition = line_repetition / 100
        randomness = randomness / 100
        max_length = st.number_input(label="Maximum line length", min_value=1, value=max_line_val, key="max_length")
        min_length = st.number_input(label="Minimum line length", max_value=max_length, min_value=1, value=min_line_val, key="min_length")
        apply = st.button(label="Apply")
        if apply:
            if None not in (line_repetition, randomness, max_length, min_length):
                try:
                    r = Request()
                    app_state = st.experimental_get_query_params()
                    if "my_saved_result" in app_state:
                        user_id = app_state["my_saved_result"][0]
                        database.user_id = user_id
                        database.update_user_settings(user_id, line_repetition, randomness, max_length, min_length)
                        r.change_preferences(line_repetition=line_repetition, randomness=randomness, max_line=max_length, min_line=min_length)
                        st.markdown("###### Finished updating your preferences :smiley:")
                    else:
                        st.warning("Please login to update your preferences")
                except NameError:
                    st.markdown("###### Unfortunately your preferences weren't loaded properly. Try again")
            elif None in (line_repetition, randomness, max_length, min_length):
                st.markdown("###### Set all your preferences before pressing the Apply button")


if __name__ == '__main__':
    main()