import lesk_algorithm as lesk

def main():
	#serve un parsificatore che riconosca ** e che vada poi a chiamare lesk_algo
	lesk.simplifiedLesk("Arms", "Arms bend at the elbow.")

if __name__== "__main__":
	main()