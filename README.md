# RhymZ Song Generator
#### A python 3.8.3 project
RhymZ is an interactive, streamlit-built interface for generating songs with GPT-3.
RhymZ allows a signed in user to:
1. Add parameters and create songs in the `Songs Workshop` page
2. Save their songs to their `History` page
3. Publish their songs to the `Gallery` page- a public spotlight for all aspiring songwriters to see and get inspiration from other users
4. Change hyperparameters of the GPT-3 in the `Preferences` page for extra control and customizability
### To use the code do the following:
1. Clone the repository with git to your working directory or download a zip file which will cointain a folder. If you chose the second option make sure the path of your working directory ends with `/<name_of_zipped_folder>`
2. In the directory you're using our code write the `pip install -r requirements.txt` in the terminal

3. Have a working account of openai and in the `request.py` file, on `line 4`, insert your api key as a string:
`PRIVATE_API_KEY = "<your_api_key>"`
4. In the directory you're using our code write the `streamlit run home_page.py` in the terminal. You will get local and network URL's and will be directed to RhymZ


