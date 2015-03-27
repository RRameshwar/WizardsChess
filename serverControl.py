import sys
from Model import Board
from View import Mover
from Control import Control
from Speech import Speech
import SoundTest

import SimpleHTTPServer
import SocketServer
import time
import cgi

import urlparse

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Respond to a POST request."""
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        print("======= POST VALUES =======")
       
        words = form['message'].value
	interpret = SoundTest.interpret(words)
        translated = Control.translate(words)

        print words        

        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write("Thanks" + "\n")



class Game():
	def __init__(self):
		self.gameState = True		#State of game: 1 if playing, 0 if game over
		self.player = 'white'		#Current player: white player always starts
		self.board = Board()		#The board representation
		self.control = Control()	#The control that handles user input
		self.sp = Speech()			#The verbal feedback given by the computer


		#Begin the game

		# self.sp.engine.say("Welcome to Wizard's Chess!")
		# self.sp.engine.runAndWait()	
		print ""
		print "*~*~*~*~*~*~*~*~*~*       Welcome to Wizard's Chess!       *~*~*~*~*~*~*~*~*~*"
		print "*~*~*~*~*~*~*~*~*~*  Input is of the form 'Knight 1 to H3'  *~*~*~*~*~*~*~*~*~*\n"
		self.board.updateBoard()
		self.board.printBoard()  #Print the board so the player can make their first move

		
	def play(self):

		self.handler = ServerHandler

		INTERFACE = "192.168.43.202"
		PORT = 8000
		httpd = SocketServer.TCPServer((INTERFACE,PORT), self.handler)
		httpd.allow_reuse_address = True

		print "Serving at: http://%(interface)s:%(port)s" % dict(interface=INTERFACE or "localhost", port=PORT)
		
		while self.gameState == True:
			httpd.serve_forever()

		httpd.server_close()



		


game = Game()
game.play()



