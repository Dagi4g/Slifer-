# Copyright 2025 Dagim 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3
from datetime import date

# Read me first dagim
#   "I have no time to worry."

# Right now i am not concerned about sql conjector attack but in future this will be fixed
data_base = "/data/data/com.termux/files/home/slifer/App/Backend/DataBase/slifer.db"
schema_file = "/data/data/com.termux/files/home/slifer/App/Backend/DataBase/schema.sql"

def initalize_database(data_base: str, schema_file: str):
    """ This method will read the schema file from database directory and executes the code. """

    with open(schema_file) as file:
        # Storing all the code in one sql file is simple for managing the data base.
        schema = file.read()
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.executescript(schema)
    # */ There will be 3 tables in a data base called slifer that store,subject, topic and subtopic. */
    conn.commit()
    print("The Data base created successfully")


    


# Eventhough i want to have some beautiful user interface ,creating the table for subject,topic and subtopic in the start will help me identify usefull approaches


""" Add subject first then ask for topics and subtopics smothlly"""

class Subject:
    """ The function of this class is to make adding ,
    removing,asking and editing subject simple."""
    def __init__(self, data_base: str) -> None:
        """ The database must be intialized first because it will be used later repetidly in the class. """
        # This try statment is used to privent injection attack
        try :
            self.data_base = data_base
            self.connection = sqlite3.connect(data_base)
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT 1")

        except sqlite3.Error as e:
            print(f"Database Connection error:{e}")
            self.connection = None

        

    # But first adding.
    def add_subject(self,subject_name: list[str],today: str = date.today().isoformat()) -> None:
        if not self.connection:
            print("Cannot add subject: database connection error")
            return
        try :
            formated_subject_input = [
                {"name" : subject.strip(), # Remove any white space.
                 
                 "rating" : 3,
                 "today" : today,
                 } for subject in subject_name
                ]
            self.cursor.executemany("INSERT INTO subjects(name, last_seen,rating) VALUES(:name,:today,:rating)",formated_subject_input)
            self.connection.commit() # Every change to the database must be comited .
            print("Subject added succesfully.")
        except sqlite3.IntegrityError:
            print(f"\"{subject_name}\" exists in the database.")
            self.connection.commit()# if not commited the data base will be locked for topic.

    def close_connection(self):# In case if needed.
        self.connections().close()

class Topic:
    """ The topic class has the same functionality as the subject class"""

    def __init__(self,data_base: str) -> None:
        """ Because topic is manuplated in a data base
        the database must be provided"""
        self.data_base = data_base
        self.connection = sqlite3.connect(data_base)
        self.cursor = self.connection.cursor()
    # Nothing will change from subject class.
    # but because i wanted to process subject id in the class there is additional code.
    def add_topic(self,subject_name : str,topic_name: str,remember_me : str = date.today().isoformat(), last_seen: str = date.today().isoformat(),
                  rating = 3):
        subject = (subject_name.strip(),)
        extract = self.cursor.execute("SELECT subject_id FROM subjects WHERE name = ?",subject) # i used brackets to put ? sign but when i tried to use add_topic the code raised "incorrect number of binding suplied error.
        result = extract.fetchone()
        # reporting to the user that the subject is not found is better than showing the trackrace
        if result:
            subject_id = result[0]
        else:
            print(f"Subject doesn't exist")
        formated_topic_list = [
                {"subject_id" : subject_id,
                 "name" : topic.strip(),
                 "remember_me" : remember_me,
                 "last_seen" : last_seen,
                 "rating" : rating

                 }for topic in topic_name
                ]
        self.cursor.executemany("""INSERT INTO topics(subject_id,name,remember_me,last_seen,rating) VALUES(:subject_id,:name,:remember_me,:last_seen,:rating)""",formated_topic_list)
        self.connection.commit()
        print("topic added successfully.")


# THE TEST PEOGRAM
if __name__ == "__main__":
    initalize_database(data_base,schema_file)
    subject_names = input("please enter the subject\n> ").split(",")
    sub = Subject(data_base)
    sub.add_subject(subject_names)

    for subject in subject_names:
        # this current program works for adding one topic to one subject .
        # incase there are different subjects this code allows to add topics topics for each.

        topic_name = input(f"add topics to {subject}\n> ").split(",")
        top = Topic(data_base)
        print(subject)
        top.add_topic(subject,topic_name) # the subject must be a tuple in order to eliminate "sqlite3.programming error".





