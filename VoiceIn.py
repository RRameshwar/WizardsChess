	

def getVoiceInput(self,player):

	self.sp.engine.say(player + " player, your move.")
	self.sp.engine.runAndWait()
	print player + " player, your move.\n\n"

	return self.translate()