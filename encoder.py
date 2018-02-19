import sys
import os
import operator
import bisect
from bitstring import Bits
import json


class HuffmanEncoder:


	class TreeNode(object):

		def __init__(self, char=None, freq=0):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		def __lt__(self, other):
			return self.freq < other.freq


	def __init__(self, source, target):

		if not (os.path.exists( source ) and os.path.isfile( source )):
			error_mesg( 'Error: ' + source + ' does not exist.' )

		self.HuffmanTreeRoot = None
		self.source = source
		self.target = target
		self.char_freq_map = {}
		self.code_map = {}


	def frequency_counter(self):

		with open( self.source, 'rb' ) as plaintext:
			while True:
				byte = plaintext.read(1)
				if not byte:
					break
				if not (byte in self.char_freq_map):
					self.char_freq_map[ byte ] = 1 
				else:
					self.char_freq_map[ byte ] += 1


	def codeTree_builder(self):
	
		priority_node_queue = []
		for (char, freq) in sorted( self.char_freq_map.items(), key=operator.itemgetter(1) ):
			priority_node_queue.append( self.TreeNode(char=char, freq=freq) )

		while len(priority_node_queue) > 1:
			left_child 	= priority_node_queue.pop(0)
			right_child = priority_node_queue.pop(0)
			root = self.TreeNode( freq=left_child.freq+right_child.freq )
			root.left, root.right = left_child, right_child
			bisect.insort( priority_node_queue, root )

		self.HuffmanTreeRoot = priority_node_queue[0]

		
	def tree_traverser(self):

		def code_generator(current_node, current_code, code_map):

			if current_node is None:
				return

			if current_node.char is not None:
				code_map[ current_node.char ] = current_code
				return

			code_generator( current_node.left, current_code+'0', code_map )
			code_generator( current_node.right, current_code+'1', code_map )	

		code_generator( self.HuffmanTreeRoot, "", self.code_map )

	


	def output_target(self):

		encoded_text = ""
		with open( self.source, 'rb' ) as plaintext:
			while True:
				byte = plaintext.read(1)
				if not byte:
					break
				encoded_text += self.code_map[ byte ]
		
		padding_len = 0
		if len(encoded_text) % 8 != 0:
			padding_len = 8 - len(encoded_text) % 8 
			encoded_text += '0' * padding_len # padding with zeros
			
		encoded_file = ""
		for i in range( 0, len(encoded_text), 8 ):
			encoded_file += chr(Bits( bin='0'+encoded_text[i:i+8] ).int)

		serialize_map = dict( (char.decode('utf-8'), self.code_map[char]) for char in self.code_map )

		with open( self.target, 'w' ) as target:
			target.write( json.dumps( serialize_map ) )
			target.write( '\n#\n' )
			target.write( encoded_file )
			target.write( '\n#\n' )
			target.write( str(padding_len) )

		print( 'Huffman encode successfully.' )
		print( 'The plaintext size=', os.path.getsize( self.source ) )
		print( 'The encoded text size=', os.path.getsize( self.target ) )





#************************* Encoding algorithm *************************  
#1.	Scan text to be compressed and totally occurrence of all characters.
#2.	Sort or prioritize characters based on 	number of occurrences in text.
#3.	Build Huffman code tree based on prioritized list.
#4.	Perform a traversal of tree to determine all code words.
#5.	Scan text again and create new file using the Huffman codes.
#********************************************************************** 



def Encoder(source, target):

	encoder = HuffmanEncoder( source, target )
	encoder.frequency_counter() # step 1 
	encoder.codeTree_builder()  # step 2 & 3
	encoder.tree_traverser()    # step 4
	encoder.output_target()     # step 5




def error_mesg(mesg):

	print( mesg )
	sys.exit(0)



if __name__ == '__main__':

	if len( sys.argv ) != 3:
		error_mesg( 'Usage: python ' + sys.argv[0] + ' [plaintext path] [encoded text path]' )
		

	Encoder( source=sys.argv[1], target=sys.argv[2] )


