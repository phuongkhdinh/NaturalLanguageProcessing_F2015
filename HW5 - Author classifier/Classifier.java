public class Classifier {

	public Classifier() { // constructor

	}

	public class LanguageModel {

		public HashMap<String, Integer> unigram;
		public HashMap<String, Integer> bigram;
		public HashMap<String, Integer> trigram;

		public String author;


		public LanguageModel(String auth, String[] text) {
			author = auth;
			unigram = createUnigram(String[] text);
			bigram = createBigram(String[] text);
			trigram = createTrigram(String[] text);
		}

		public HashMap<String, Integer> createUnigram(String[] text) {
			HashMap<String, Integer> unigram = new HashMap<String, Integer>();
			for (word : text) {
				if (unigram.containsKey(word)) {
					unigram.put(word, unigram.get(word) + 1); // add one to the current count
				}
				else {
					unigram.put(word, 1);
				}
			}
			return unigram;
		}

		public HashMap<String, Integer> createBigram(String[] text) {
			HashMap<String, Integer> bigram = new HashMap<String, Integer>();
			for (int i = 0; i < text.length - 1; i++) {
				String twoWords = text[i] + text[i + 1];
				if (bigram.containsKey(twoWords)) {
					bigram.put(twoWords, bigram.get(twoWords) + 1); // add one to the current count
				}
				else {
					bigram.put(twoWords, 1);
				}
			}
			return bigram;
		}

		public HashMap<String, Integer> createTrigram(String[] text) {
			HashMap<String, Integer> trigram = new HashMap<String, Integer>();
			for (int i = 0; i < text.length - 2; i++) {
				String threeWords = text[i] + text[i + 1] + text[i + 2];
				if (trigram.containsKey(threeWords)) {
					trigram.put(threeWords, trigram.get(threeWords) + 1); // add one to the current count
				}
				else {
					trigram.put(threeWords, 1);
				}
			}
			return trigram;
		}

	}

	public String getText(String url) {

	}

	public String[] extractDevSet(String text) {

	}

	public String[] tokenize(String text) {

	}

	public LanguageModel train(String author, String[] trainText) {

	}

	public String test(LanguageModel[] lms, String sentence) {
		//    tokenize
		//    compare this sentence against all language models
		//    find author/model with highest probability
	}

	public HashMap<String, Integer[]> devTest(LanguageModel[] lms, HashMap<String, String> testText) {
		// For each author:
		//   get text from hashmap
		//   split by dot
		//   For each sentence:
		//    test(lms, sentence)
		//    if we correctly identify the language model, add one to correct count
		//   Calculate the percentage of correctly identified sentences
		// Return results

	}

	public LanguageModel[] buildLanguageModels(String authorList) {

	}



	public static void main(String[] args) {
		if (args[0].equals("-dev") && args.length == 2) {
			// create lang models
			// test on dev set, print result

		}

		else if (args[0].equals("-test") && args.length == 3) {
			// create lang models
			// for each sentence in test set: 
			//     test(lms, sentence)
			//     print most probable author
		}

		else {
			System.out.println("Please provide [-dev authorlist] or [-test authorlist testset.txt]");
		}

	}
}