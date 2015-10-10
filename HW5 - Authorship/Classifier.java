import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.ArrayList;
import java.util.HashMap;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.*;
import java.io.*;

public class Classifier {

	public Classifier() { // constructor

	}

	public class LanguageModel {

		public ArrayList<HashMap<String, Double>> ngrams;

		public HashMap<String, Double[]> smoothingCounts; // <"unigram", [#0,#1,#2...#6]>

		public HashMap<String, Double> unigram;
		public HashMap<String, Double> bigram;
		public HashMap<String, Double> trigram;

		public String author;


		public LanguageModel(String auth, String[] devSet) {
			author = auth;
			unigram = new HashMap<String, Double>();
			bigram = new HashMap<String, Double>();
			trigram = new HashMap<String, Double>();

			ngrams = new ArrayList<HashMap<String, Double>>();
			ngrams.add(unigram);
			ngrams.add(bigram);
			ngrams.add(trigram);

			smoothingCounts = new HashMap<String, Double[]>();


			for (String line:devSet) {

				ArrayList<String> text = tokenize(line);
				unigram = addToUnigram(text);
				bigram = addToBigram(text);
				trigram = addToTrigram(text);
			}

			// Soothing
			String[] listname = new String[]{"unigram", "bigram", "trigram"};
			int j = 0;
			for (HashMap<String,Double> ngram : ngrams) {
				Double[] nc = new Double[]{0.0,0.0,0.0,0.0,0.0,0.0,0.0,};
				nc[0] = Math.pow(1000000,j+1) - ngram.size();
				for (String key : ngram.keySet()) {
					System.out.println(key);

					for (int i = 1; i < 7; i++) {
						if (ngram.get(key) == i) {
							System.out.println(nc[i]);

							nc[i] = nc[i] + 1.0;
						}
					}
				}
				smoothingCounts.put(listname[j], nc);
				j++;
			}

			j = 0;
			// Adjustment for all 3 n-gram
			for (HashMap<String,Double> ngram : ngrams) {
				for (String key : ngram.keySet()) {
					int c = ngram.get(key).intValue();
					if (c < 7) { // Only adjust smoothing for count less than 7
						Double adjValue = (c+1) * smoothingCounts.get(listname[j])[c+1] / smoothingCounts.get(listname[j])[c];
						// Smoothing formula: C* = (C+1)* Nc+1 /Nc
						ngram.put(key, adjValue);
					}
				}
				j++;
			}
				//for each n-gram
				// Count number of patterns that count <6
				// Calculate new probability for each int again
		}

		public HashMap<String, Double> addToUnigram(ArrayList<String> text) {
			//HashMap<String, Integer> unigram = new HashMap<String, Integer>();
			for (int i = 0; i < text.size(); i++) {
                String word = text.get(i);
				if (unigram.containsKey(word)) {
					unigram.put(word, unigram.get(word) + 1); // add one to the current count
				}
				else {
					unigram.put(word, 1.0);
				}
			}
			return unigram;
		}

		public HashMap<String, Double> addToBigram(ArrayList<String> text) {
			//HashMap<String, Integer> bigram = new HashMap<String, Integer>();
			for (int i = 0; i < text.size() - 1; i++) {
				String twoWords = text.get(i) + text.get(i + 1);
				if (bigram.containsKey(twoWords)) {
					bigram.put(twoWords, bigram.get(twoWords) + 1); // add one to the current count
				}
				else {
					bigram.put(twoWords, 1.0);
				}
			}
			return bigram;
		}

		public HashMap<String, Double> addToTrigram(ArrayList<String> text) {
			//HashMap<String, Integer> trigram = new HashMap<String, Integer>();
			for (int i = 0; i < text.size() - 2; i++) {
				String threeWords = text.get(i) + text.get(i + 1) + text.get(i + 2);
				if (trigram.containsKey(threeWords)) {
					trigram.put(threeWords, trigram.get(threeWords) + 1); // add one to the current count
				}
				else {
					trigram.put(threeWords, 1.0);
				}
			}
			return trigram;
		}

	}

    /* Connects to URL and returns text as String from the webpage 
       Adapted from http://docs.oracle.com/javase/tutorial/networking/urls/readingURL.html */
	public String getText(String urlAddress) {
        URL url;
        StringBuilder pageText = new StringBuilder();
        try {
            url = new URL(urlAddress);
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                pageText.append(inputLine);
                pageText.append("\n"); //NOt sure why you put new lines. are we still considering dot as a character?
            }
            in.close();
        }
        catch (Exception e) {
            System.err.println(e);
            System.err.println("Error: Could not read from URL " + urlAddress);
        }
        return pageText.toString();
    }

	public String[] extractDevSet(String text) {
		String[] sentences = text.split("\n");
		//int sentenceCount = sentences.length;
		StringBuilder trainText = new StringBuilder();
		StringBuilder testText = new StringBuilder();

		int count = 0;
		for (String sentence:sentences){
			if (count%10 == 0) {
				//Move in the test set
				testText.append(sentence);
				testText.append("\n");
			} else {
				// Move in the train set
				trainText.append(sentence);
				trainText.append("\n");
			}
			count = count + 1;
		}
		String[] sets = new String[] {trainText.toString(), testText.toString()};
        return sets;
	}

    /* Tokenizes raw text into an ArrayList of tokens. */
	public ArrayList<String> tokenize(String text) {

		//String[] abbrList = ['co.', 'dr.', 'jan.', 'feb.', 'mar.', 'apr.', 'jun.', 'jul.', 'aug.', 'sep.', 'sept.', 'oct.', \
    //'nov.', 'dec.', 'mrs.', 'ms.', 'mr.' 'jr.', 'sr.', 'inc.'];

        // Remove $,;"|`#:%^*_+=~{}<>[]()
        String tokenizedLine = text.replaceAll("[$,\"\\(\\);\\|`#:%\\^\\*_\\+=~\\{\\}<>\\[\\]]", "");
           
        // Remove single quotes from around words
        tokenizedLine = tokenizedLine.replaceAll("' ", " ");
        tokenizedLine = tokenizedLine.replaceAll(" '", " ");
        tokenizedLine = tokenizedLine.replaceAll("'$", " ");
        tokenizedLine = tokenizedLine.replaceAll("^'", " ");           
        
        String[] rawTokens = tokenizedLine.split("\\s+"); // split by any whitespace
        ArrayList<String> tokensList = new ArrayList<String>(); // to hold sanitized tokens
        
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

	public LanguageModel train(String author, String devSet) {
		String[] lines = devSet.split("\n");
		LanguageModel lm = new LanguageModel(author, lines);
		return lm;
	}

	public String test(ArrayList<LanguageModel> lms, String line) {
		ArrayList<String> tokens = tokenize(line);
		Double bestLogProb = Double.NEGATIVE_INFINITY;
		Double logProb = 0.0;
		String bestMatchAuthor = "";
		for (LanguageModel lm : lms) {
			//Bigram first
			for (int i = 0; i < tokens.size(); i++){
				logProb = logProb + Math.log(lm.bigram.get(tokens.get(i)+tokens.get(i+1))) - Math.log(lm.unigram.get(tokens.get(i)));
			}
			if (logProb > bestLogProb) {
				bestLogProb = logProb;
				bestMatchAuthor = lm.author;
			}
		}
		//    tokenize
		//    compare this line against all language models
		//    find author/model with highest probability
		System.out.println(bestMatchAuthor);
        return bestMatchAuthor;
	}

	public HashMap<String, Integer[]> devTest(ArrayList<LanguageModel> lms, HashMap<String, String> testSets) {
		HashMap<String, Integer[]> results = new HashMap<String, Integer[]>();
		for (String author : testSets.keySet()) {
		// For each author:
			String testText = testSets.get(author);
		//   get text from hashmap
			String[] lines = testText.split("\n");
			int totalLines = lines.length;
			int correctMatch = 0;
			for (String line : lines) {
				String matchedAuthor = test(lms, line);
				if (matchedAuthor.equals(author)) {
					correctMatch ++;
				}
			}
			results.put(author, new Integer[] {correctMatch, totalLines});


		//   split by line
		//   For each line:
		//    test(lms, line)
		//    if we correctly identify the language model, add one to correct count
		//   Calculate the percentage of correctly identified sentences

		}
		
		// Return results
        return results;

	}

	public HashMap<String, String>[] getAuthorsCompleteSets(String authorlist){
		HashMap<String, String> devSets = new HashMap<String, String>();
		HashMap<String, String> testSets = new HashMap<String, String>();
	  	try {
	    	BufferedReader reader = new BufferedReader(new FileReader(authorlist));
	    	String line;
	    	while ((line = reader.readLine()) != null) {
	      		String[] authorAndUrl = line.split(",");
	      		String prose = getText(authorAndUrl[1]);
	      		String[] authorSets = extractDevSet(prose);
	      		devSets.put(authorAndUrl[0], authorSets[0]); // author, devSet
	      		testSets.put(authorAndUrl[0], authorSets[1]); // author, testSet
	    	}
		    reader.close();
		    return new HashMap[] {devSets, testSets};
	  	}
	  	catch (Exception e) {
	    	System.err.println(e);
	    	System.err.println("Could not open authorlist");
	    	return null;
	  	}
	}

	public ArrayList<LanguageModel> buildLanguageModels(HashMap<String, String> devSets) {

		// Build model
		ArrayList<LanguageModel> languageModels = new ArrayList<LanguageModel>();
		//Set keyset = devSets.keySet();
		for (String author : devSets.keySet()) {
			LanguageModel lm = train(author, devSets.get(author));
			languageModels.add(lm);
		}
        return languageModels;
	}



	public static void main(String[] args) {
		Classifier c = new Classifier();
        if (args.length > 0 && (args[0].equals("-dev") || args[0].equals("-test"))) {
            if (args[0].equals("-dev") && args.length == 2) {

            	// Create DevSet, testSet for each author
            	HashMap<String, String>[] authorsCompleteSets = c.getAuthorsCompleteSets(args[1]); // List of 2 dictionary, 1st element DevText, 
            														      //2nd element TestSet for each author

            	// create lang models
            	ArrayList<LanguageModel> languageModels = c.buildLanguageModels(authorsCompleteSets[0]); 
            	         						//authorsCompleteSets[0] is the hashmap of {author:devset}

                // test on test set, print result
                HashMap<String, Integer[]> devTestResults = c.devTest(languageModels, authorsCompleteSets[1]) ;
                								//authorsCompleteSets[1] is the hashmap of {author:testset}

            }

            else if (args[0].equals("-test") && args.length == 3) {
                // create lang models
                // for each sentence in test set: 
                //     test(lms, sentence)
                //     print most probable author
            }
        }
		else {
			System.out.println("Please provide [-dev authorlist] or [-test authorlist testset.txt]");
		}
        
        /* Code snippet to test getting text from URL */
        //Classifier c = new Classifier();
        //String text = c.getText("http://www.cs.carleton.edu/faculty/aexley/authors/whitman.txt");
        //System.out.println(text);

	}
}