import streamlit as st
import pandas as pd




# DB Management
import os

def get_usertable():
	if not os.path.exists("usertable.csv"):
		df = pd.DataFrame({"users":[], "passwords":[], "id":[], "line_repetition": [], "randomness": [], "max_line": [], "min_line": []})
		df.to_csv("usertable.csv",index=False)
	else:
		df = pd.read_csv("usertable.csv")
	return df

def get_gallery():
	if not os.path.exists("gallery.csv"):
		df = pd.DataFrame({"users":[], "Requests":[], "Creations":[]})
		df.to_csv("gallery.csv",index=False)
	else:
		df = pd.read_csv("gallery.csv")
	return df


class user_database:
	def __init__(self):
		self.user_table = get_usertable()
		self.user_id = None
		self.user_data = None

	def add_song_to_gallery(self, user, request, creation):
		gallery = get_gallery()
		gallery = gallery.append({"users": user, "Requests": request, "Creations": creation}, ignore_index=True)
		gallery.to_csv("gallery.csv", index=False)
		return gallery

	def sign_up_users(self, username, password):
		if username == "":
			return "empty username"
		elif password == "":
			return "empty password"
		elif username not in self.user_table["users"].values:
			self.user_table = self.user_table.append({"users": username, "passwords": password, "id": len(self.user_table), "line_repetition": 0.5, "randomness": 0.5, "max_line": 6, "min_line": 3}, ignore_index=True)
			self.user_id = len(self.user_table["users"])-1
			self.user_table.to_csv("usertable.csv", index=False)
			return "success"
		else:
			return "username taken"

	def login_users(self, username, password):
		if username in self.user_table["users"].values:
			if password == str(self.user_table[self.user_table["users"] == username]["passwords"].values[0]):
				self.get_userid(username)
				return "success"
			else:
				return "Wrong Password"
		else:
			return "User not found"

	def get_userid(self, username):
		self.user_id = self.user_table[self.user_table["users"] == username]["id"].values[0]

	def get_userdata(self,id):
		if not os.path.exists("users/{}.csv".format(id)):
			self.user_data = pd.DataFrame({"request": [], "response": []})
			self.user_data.to_csv("users/{}.csv".format(id), index=False)
		else:
			self.user_data = pd.read_csv("users/{}.csv".format(id))

	def update_userdata(self, request, response):
		self.user_data = self.user_data.append({"request": request, "response": response}, ignore_index=True)
		self.user_data.to_csv("users/{}.csv".format(self.user_id), index=False)
		return self.user_data

	def get_user_settings(self, id):
		return list(self.user_table[self.user_table["id"] == int(id)][["line_repetition", "randomness", "max_line", "min_line"]].values[0])

	def update_user_settings(self, id, line_repetition, randomness, max_line, min_line):
		self.user_table.loc[self.user_table["id"] == int(id), "line_repetition"] = line_repetition
		self.user_table.loc[self.user_table["id"] == int(id), "randomness"] = randomness
		self.user_table.loc[self.user_table["id"] == int(id), "max_line"] = max_line
		self.user_table.loc[self.user_table["id"] == int(id), "min_line"] = min_line
		self.user_table.to_csv("usertable.csv", index=False)
		return self.user_table

	def get_username(self, id):
		return self.user_table[self.user_table["id"] == int(id)]["users"].values[0]






def main():
	"""Simple Login App"""
	database= user_database()

	st.title("Simple Login App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password", type='password')
		if st.sidebar.button("Login"):
			result = database.login_users(username,password)
			if result == "success":
				database.get_userdata(database.user_id)
				st.success("Logged In as {}".format(username))
				task = st.selectbox("Task", ["Add Post", "Analytics", "Profiles"])
				if task == "Add Post":
					st.subheader("Add Your Post")

				elif task == "Analytics":
					st.subheader("Analytics")

			elif result == "Wrong Password":
				st.warning("Incorrect Password")
			else:
				st.warning("User not found")


	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
		print(new_user, new_password)

		if st.button("Signup"):
			response = database.sign_up_users(new_user,new_password)
			if response == "success":
				database.get_userdata(database.user_id)
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")
			elif response == "username taken":
				st.warning("Username already taken")
			elif response == "empty username":
				st.warning("Username cannot be empty")
			else:
				st.warning("Password cannot be empty")






if __name__ == '__main__':
	main()