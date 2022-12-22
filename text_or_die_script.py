import pyscreenshot as ps
from pytesseract import pytesseract
import os
import keyboard
import pyautogui as auto
import time


answers_dict = {}  # dictionary that will hold all the questions and answers

# this will open the text file and add the questions and answers in the dictionary
with open(os.path.join(os.path.dirname(__file__), 'answers.txt'), mode='r') as answers:
    for line in answers:
        key, val = line.rstrip("\n").split(";")
        val = val.split(",")
        answers_dict[key] = val


# takes a screenshot of the region where the question pops up
screenshot = ps.grab(bbox=(560, 56-50, 1360, 130+50))
# path to the program that comverts image to text
pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


keys = answers_dict.keys()  # list of keys from the dictionary


previous_question = ""
while True:
    time.sleep(1/15)

    if keyboard.is_pressed('q'):  # if key 'q' is pressed then the program quits
        break

    # takes a screenshot of the region where the question pops up
    screenshot = ps.grab(bbox=(560, 56-50, 1360, 130+50))

    question = pytesseract.image_to_string(screenshot)

    if question != previous_question:
        # some questions are multiline, this line of code makes the string a one line string
        question_to_list = question.rstrip("\n").split(" ")

        # this will only pick the last 7/4 words of the question as some questions
        # are not exactly the same as the questions in the text file
        n = (len(question_to_list) / 7) * 4
        last_few_words_question = question_to_list[-round(n):]

        # this will iterate over each key (question), then check if the words are in the questions,
        # if all the wors are in the key then the word_inKey flag will be true
        word_in_key = False
        for key in keys:
            for word in last_few_words_question:
                if word.lower() in key.lower().split(" "):
                    word_in_key = True
                else:
                    word_in_key = False
                    break
            # if word_in_key is true then the key willbe used to find the list of answers,
            # then the longest word will be picked
            if word_in_key:
                answers = answers_dict[key]
                longest_answer = max(answers, key=len)
                print("=================================================")
                print("Question: ", key)
                print("Longest answer: ", longest_answer)
                # small delay before starting to type to wait for in game text box animations
                time.sleep(0.3)
                # autotype the answer with a small delay so that it doesn't raise suspicion
                auto.typewrite(longest_answer, interval=0.15)
                keyboard.press_and_release('enter')
                previous_question = question
                break
