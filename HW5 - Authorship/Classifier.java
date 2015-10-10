import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.ArrayList;

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

    /* Tokenizes raw text into an ArrayList of tokens. */
	public ArrayList<String> tokenize(String text) {

        // Remove $,;"|`#:%^*_+=~{}<>[]()
        String tokenizedLine = text.replaceAll("[$,\"\\(\\);\\|`#:%\\^\\*_\\+=~\\{\\}<>\\[\\]]", "");
           
        // Remove single quotes from around words
        tokenizedLine = tokenizedLine.replaceAll("' ", " ");
        tokenizedLine = tokenizedLine.replaceAll(" '", " ");
        tokenizedLine = tokenizedLine.replaceAll("'$", " ");
        tokenizedLine = tokenizedLine.replaceAll("^'", " ");           
        
        String[] rawTokens = tokenizedLine.split("\\s+"); // split by any whitespace
        ArrayList<String> tokensList = new ArrayList<String>(); // to hold sanitized tokens
        
        // TODO!!! Remove punctuation .!? from everywhere except end of token
        // TODO test tokenization of multiple tokens ending with punct, ex "test! this."
        
        // Treats each punctuation character in .?! as its own token 
        String endsWithPunct = "([^\\.\\?!]*)([\\.\\?!]+)([^\\.\\?!\\s$]*)"; // 0+ non-punctuations followed by 1+ punctuation
        Pattern punctPattern = Pattern.compile(endsWithPunct);
        for (int i = 0; i < rawTokens.length; i++) {
            Matcher m = punctPattern.matcher(rawTokens[i]);
            if (m.find()) { // if token ends with at least one punctuation, split into separate tokens
                String nonPunct = m.group(1);
                String punct = m.group(2);
                String postPunct = m.group(3);
                tokensList.add(nonPunct);
                for (int j = 0; j < punct.length(); j++) {
                    tokensList.add(punct.substring(j, j+1));
                } 
                if (!postPunct.equals("")) {
                    tokensList.add(postPunct);
                }
            }
            else { // no punctuation in token
                tokensList.add(rawTokens[i]);
            }
        }
        return tokensList;
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