# Eliza.py
# By Phuong Dinh and Julia Kroll
# Sep 20th 2015
# An Eliza-style program that uses regular expressions to converse with the user
# To exit the program, type anything includes "goodbye"
# Multiple substitution is allowed.
# e.g.I feel happy when i see him. I am in love 
#  -> I see. Why do you feel happy when you see him. Do you enjoy being in love?? ( I feel -> why do you feel *;  I -> you, I am in love -> Do you enjoy *)

import re, sys

def main():
	userInput = input("Eliza: Hello. Please tell me about your problems.\nYou: ")

	while not re.search(r'goodbye', userInput.lower(), flags=re.IGNORECASE):
		# Substitution series

		'''----------------
		 Assignment given sub
		 ---------------------
		 '''
		# Yes, No, *you will substitute the whole sentence
		userInputAltered = re.sub(r'.*(^|\s)yes(\s|$|\.|\?|,).*','IEliza see.', userInput, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'.*(^|\s)no(\s|$|\.|\?|!).*','Why not?', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'.* you(\s|$).*',"Let's not talk about meEliza.", userInputAltered, flags=re.IGNORECASE)
		# What is *, i am*, why is* will substitute part of the sentence
		userInputAltered = re.sub(r'(^|[!\.\?] )what is (.*)\?',r'\1Why do youEliza ask about \2?', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|[!\.\?] )i am (.*)',r'\1Do youEliza enjoy being \2?', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|[!\.\?] )why is (.*)\?',r'\1Why do youEliza think \2?', userInputAltered, flags=re.IGNORECASE)

		''' ---------------
		Our own rules
		--------------------
		'''
		# Eliza introduction
		userInputAltered = re.sub(r'.*who are you\?.*',r"Hi, I'm Eliza, a computer program created by Phuong and Julia to talk to youEliza! Tell meEliza anything!", userInputAltered, flags=re.IGNORECASE)
		# I feel * when I * -> I see. Why do you feel * when you *?
		userInputAltered = re.sub(r'^i feel (.*) when I (.*)$',r'IEliza see. Why do youEliza feel \1 when youEliza \2?', userInputAltered, flags=re.IGNORECASE)
		# I remember * -> What makes you think of *?
		userInputAltered = re.sub(r'^i remember (.*)$',r'What makes youEliza think of \1?', userInputAltered, flags=re.IGNORECASE)
		# everyone * -> surely not everyone * 
		userInputAltered = re.sub(r'everyone ',r'surely not everyone ', userInputAltered, flags=re.IGNORECASE)
		# * sorry * -> Apologies are not necessary
		userInputAltered = re.sub(r'.*sorry.*', r'Apologies are not necessary.', userInputAltered, flags=re.IGNORECASE)
		# Capture variations on family member titles, e.g. grandfather, stepsister, mother
		# If input has words such as grandfather/mother, stepsister/brother, brother/sister-in-law..., Eliza will ask more about the person mentioned
		userInputAltered = re.sub(r'.*(^|\s)(grand|step)?(father|mother|sister|brother|family)([a-zA-Z\-]*)(\s|$).*', r'Tell meEliza more about yourEliza \2\3\4.', userInputAltered, flags=re.IGNORECASE)
		
		# Assignment given sub (moved down here for logic reason)
		userInputAltered = re.sub(r'^my (.*)$',r'YourEliza \1.', userInputAltered, flags=re.IGNORECASE)

		# Reverse first-person and second-person pronouns to respond grammatically. 
		userInputAltered = re.sub(r'(^|\s)i(\s|$|\.|\?|!)',r'\1youEliza\2', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|\s)me(\s|$|\.|\?|!)',r'\1youEliza\2', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|\s)mine(\s|$|\.|\?|!)',r'\1yoursEliza\2', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|\s)my(\s|$|\.|\?|!)',r'\1yourEliza\2', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|\s)am(\s|$|\.|\?|!)',r'\1are\2', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|\s)you are(\s|$|\.|\?|!)',r'\1I am\2', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|\s)you(\s|$|\.|\?|!)',r'\1I\2', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|\s)your(\s|$|\.|\?|!)',r'\1my\2', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'(^|\s)yours(\s|$|\.|\?|!)',r'\1mine\2', userInputAltered, flags=re.IGNORECASE)

		#The Eliza rules -- sub in the target word now that all other substitutions have been completed.
		userInputAltered = re.sub(r'IEliza',r'I', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'youEliza',r'you', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'yourEliza',r'your', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'yoursEliza',r'yours', userInputAltered, flags=re.IGNORECASE)
		userInputAltered = re.sub(r'meEliza',r'me', userInputAltered, flags=re.IGNORECASE)

		# Receive new input from the user.
		if re.match(userInputAltered, userInput, flags=re.IGNORECASE) and re.match(userInput, userInputAltered, flags=re.IGNORECASE):
			userInput = input("Eliza: Please go on.\nYou: ")
		else:
			userInput = input("Eliza: " + userInputAltered + "\nYou: ") 

	print("Eliza: Goodbye!")
	exit(0)

if __name__ == "__main__":
	main()

