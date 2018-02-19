import os
import sys
import json

class HuffmanDecoder:

	class TreeNode(object):

		def __init__(self, char=None):

			self.char = char
			self.left = None
			self.right = None


	def __init__(self, source, target):

		if not (os.path.exists( source ) and os.path.isfile( source )):
			error_mesg( 'Error: ' + source + ' does not exist.' )

		self.HuffmanTreeRoot = self.TreeNode()
		self.source = source
		self.target = target
		self.code_map = {}
		self.encoded_text = ""
		self.padding_len = 0


	def parser(self):

		with open( self.source ) as encoded_file:
			(serailizedMap, self.encoded_text, self.padding_len) = encoded_file.read().split('\n#\n')
			self.code_map = json.loads( serailizedMap )



	def codeTree_builder(self):

		for (char, code) in self.code_map.items():
			current_node = self.HuffmanTreeRoot
			for bit in code:
				if bit == '0':
					if current_node.left is None:
						current_node.left = self.TreeNode()
					current_node = current_node.left
				else:
					if current_node.right is None:
						current_node.right = self.TreeNode()
					current_node = current_node.right
			current_node.char = char	


	def tree_traverser(self):

		byte_stream = ""
		for char in self.encoded_text:
			byte = bin(ord(char))[2:]
			if len(byte) < 8:
				byte = '0' * (8 - len(byte)) + byte
			byte_stream += byte
		byte_stream = byte_stream[:-int(self.padding_len)]

		decoded_text = ""
		current_node = self.HuffmanTreeRoot
		for bit in byte_stream:
			if bit == '0':
				current_node = current_node.left
			else:
				current_node = current_node.right
			if current_node.char is not None:
				decoded_text += current_node.char
				current_node = self.HuffmanTreeRoot
		
		with open( self.target, 'w' ) as decoded_file:
			decoded_file.write( decoded_text )

		print( 'Huffman decode successfully.' )



def Decoder(source, target):

	decoder = HuffmanDecoder( source, target )
	decoder.parser()
	decoder.codeTree_builder()  
	decoder.tree_traverser()    


def error_mesg(mesg):

	print( mesg )
	sys.exit(0)



if __name__ == '__main__':

	if len( sys.argv ) != 3:
		error_mesg( 'Usage: python ' + sys.argv[0] + ' [encoded text path] [decoded text path]' )
		

	Decoder( source=sys.argv[1], target=sys.argv[2] )



