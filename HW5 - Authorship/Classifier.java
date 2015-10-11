/*
Classifier.java
By Phuong Dinh and Julia Kroll
October 12, 2015
CS 322 - NLP
This program takes in a list of authors and urls of their text.
For the -dev command, it trains a language model on a development set of each author's text,
and then tests the language models on a test set, returning a list of how often the 
models correctly identified the author of each line in the test set.
For the -test command, it trains a language model on the development set for each author,
and then returns a prediction of the author of each line in the test set.
*/

import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.ArrayList;
import java.util.HashMap;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.*;
import java.io.*;

public class Classifier {

	public Classifier() { 

	}

	/* Stores the unigram, bigram, and trigram models for each author,
	   and performs Good-Turing smoothing.
	*/
	public class LanguageModel {

		public ArrayList<HashMap<String, Double>> ngrams;

		public HashMap<String, Double[]> smoothingCounts; // <"unigram", [#0,#1,#2...#6]>

		public HashMap<String, Double> unigram;
		public HashMap<String, Double> bigram;
		public HashMap<String, Double> trigram;

		public String author;

		public HashMap<String, Double[]> n0n1;


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

			n0n1 = new HashMap<String, Double[]>();


			for (String line:devSet) {

				ArrayList<String> text = tokenize(line);
				unigram = addToUnigram(text);
				bigram = addToBigram(text);
				trigram = addToTrigram(text);
			}

			// Smoothing
			String[] listname = new String[]{"unigram", "bigram", "trigram"};
			int j = 0;
			for (HashMap<String,Double> ngram : ngrams) {
				Double[] nc = new Double[]{0.0,0.0,0.0,0.0,0.0,0.0,0.0};
				nc[0] = Math.pow(1000000,j+1) - ngram.size();
				for (String key : ngram.keySet()) {

					for (int i = 1; i < 7; i++) {
						if (ngram.get(key) == i) {
							nc[i] = nc[i] + 1.0;
						}
					}
				}
				smoothingCounts.put(listname[j], nc);
				Double[] n0n1arr = new Double[]{nc[0], nc[1]};
				n0n1.put(listname[j], n0n1arr);
				j++;
			}

			j = 0;
			// Adjustment for all 3 n-gram
			for (HashMap<String,Double> ngram : ngrams) {
				for (String key : ngram.keySet()) {
					int c = ngram.get(key).intValue();
					if (c < 6) { // Only adjust smoothing for count less than 7
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
				String twoWords = text.get(i) + " " + text.get(i + 1);
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
				String threeWords = text.get(i) + " " + text.get(i + 1) + " "+ text.get(i + 2);
				if (trigram.containsKey(threeWords)) {
					trigram.put(threeWords, trigram.get(threeWords) + 1); // add one to the current count
				}
				else {
					trigram.put(threeWords, 1.0);
				}
			}
			return trigram;
		}

		public Double getN1(String ngram) {
			return n0n1.get(ngram)[1];
		}

		public Double getN0(String ngram) {
			return n0n1.get(ngram)[0];
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

    /* Extract 90% of text as the development set, and save 10% for test set */
	public String[] extractDevSet(String text) {
		String[] sentences = text.split("\n");
		//int sentenceCount = sentences.length;
		StringBuilder trainText = new StringBuilder();
		StringBuilder testText = new StringBuilder();

		int count = 0;
		for (String sentence:sentences){
			if (count%10 == 9) {
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

    /* Tokenizes raw text into an ArrayList of tokens, turning all end-of-sentence punctuation into one period. */
	public ArrayList<String> tokenize(String text) {

        // Remove $,;"|`#:%^*_+=~{}<>[]()
        String tokenizedLine = text.replaceAll("[\\$,\"\\(\\);\\|`#:%\\^\\*_\\+=~\\{\\}<>\\[\\]]", "");
           
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
                String punct = " . ";
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
		Double logProb;
		String bestMatchAuthor = "";
		for (LanguageModel lm : lms) {
			logProb = 0.0;

			//Bigram first
			for (int i = 0; i < tokens.size()-1; i++){
				if (lm.unigram.get(tokens.get(i)) != null) { 
					if (lm.bigram.get(tokens.get(i)+" "+tokens.get(i+1)) != null) { 
							logProb = logProb + Math.log(lm.bigram.get(tokens.get(i)+" "+tokens.get(i+1))) - Math.log(lm.unigram.get(tokens.get(i)));
					} else { // first occurrence of this bigram, smooth N0
						logProb = logProb + Math.log(lm.getN1("bigram") / lm.getN0("bigram")) - Math.log(lm.unigram.get(tokens.get(i)));
					}
				} else {
					logProb = logProb + Math.log(lm.getN1("bigram") / lm.getN0("bigram")) - Math.log(lm.getN1("unigram") / lm.getN0("unigram"));
				}
			}

		/* BACK OFF ALGORITHM
		   DID NOT GIVE GOOD RESULT -> We chose Bigram
			for (int i = 0; i < tokens.size()-2; i++){
				if (lm.trigram.get(tokens.get(i)+" "+tokens.get(i+1)+" "+tokens.get(i+2)) != null) { 
					logProb = logProb + Math.log(lm.trigram.get(tokens.get(i)+" "+tokens.get(i+1)+" "+tokens.get(i+2))) - Math.log(lm.bigram.get(tokens.get(i)+" "+tokens.get(i+1)));
				} else if (lm.bigram.get(tokens.get(i+1)+" "+tokens.get(i+2)) != null) {
					System.out.println(tokens.get(i+1)+" "+tokens.get(i+2));
					System.out.println(lm.bigram.get(tokens.get(i+1)+" "+tokens.get(i+2)));
					System.out.println(lm.unigram.get(tokens.get(i+1)));
					logProb = (logProb + Math.log(lm.bigram.get(tokens.get(i+1)+" "+tokens.get(i+2))) - Math.log(lm.unigram.get(tokens.get(i+1))));
				} else if (lm.unigram.get(tokens.get(i+2)) != null) {
					logProb = 0.7*(logProb + Math.log(lm.unigram.get(tokens.get(i+2))));
				} else {
					logProb = 0.5*(logProb + Math.log(lm.getN1("bigram") / lm.getN0("bigram")) - Math.log(lm.getN1("unigram") / lm.getN0("unigram")));
				}
			}
*/
			if (logProb > bestLogProb) {
				bestLogProb = logProb;
				bestMatchAuthor = lm.author;
			}
		}
        return bestMatchAuthor;
	}

	/* Tests on the 10% of original text set aside for testing.  */
	public HashMap<String, Integer[]> devTest(ArrayList<LanguageModel> lms, HashMap<String, String> testSets) {
		HashMap<String, Integer[]> results = new HashMap<String, Integer[]>();
		for (String author : testSets.keySet()) {
			String testText = testSets.get(author);
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
		}
        return results;
	}

	/* Gets dev set and test set for each author */
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
		ArrayList<LanguageModel> languageModels = new ArrayList<LanguageModel>();
		for (String author : devSets.keySet()) {
			LanguageModel lm = train(author, devSets.get(author));
			languageModels.add(lm);
		}
        return languageModels;
	}

	public String displayResults(HashMap<String, Integer[]> resultsMap) {
		StringBuilder resultsString = new StringBuilder();
		resultsString.append("Results on dev set:\n");
		for (String author : resultsMap.keySet()) {
			resultsString.append(author + "\t");
			Integer[] numCorrectAndTotal = resultsMap.get(author);
			resultsString.append(numCorrectAndTotal[0] + "/" + numCorrectAndTotal[1] + " correct\n");
		}
		return resultsString.toString();
	}

	public static void main(String[] args) {
		Classifier c = new Classifier();
        if (args.length > 0 && (args[0].equals("-dev") || args[0].equals("-test"))) {
            if (args[0].equals("-dev") && args.length == 2) {
            	System.out.println("Training... (this may take a while)");
            	// Create DevSet, testSet for each author
            	HashMap<String, String>[] authorsCompleteSets = c.getAuthorsCompleteSets(args[1]); // List of 2 dictionary, 1st element DevText, 
            														      //2nd element TestSet for each author

            	// create lang models
            	ArrayList<LanguageModel> languageModels = c.buildLanguageModels(authorsCompleteSets[0]); 
            	         						//authorsCompleteSets[0] is the hashmap of {author:devset}

                // test on test set, print result
                HashMap<String, Integer[]> devTestResults = c.devTest(languageModels, authorsCompleteSets[1]) ;
                								//authorsCompleteSets[1] is the hashmap of {author:testset}
                System.out.println(c.displayResults(devTestResults));

            }

            else if (args[0].equals("-test") && args.length == 3) {
            	System.out.println("Training... (this may take a while)");
            	// Create DevSet, testSet for each author
            	HashMap<String, String>[] authorsCompleteSets = c.getAuthorsCompleteSets(args[1]); // List of 2 dictionary, 1st element DevText, 
            														      //2nd element TestSet for each author

            	// create lang models
            	ArrayList<LanguageModel> languageModels = c.buildLanguageModels(authorsCompleteSets[0]); 
            	         						//authorsCompleteSets[0] is the hashmap of {author:devset}

                // test on test set, print result
	           try{
		            BufferedReader reader = new BufferedReader(new FileReader(args[2]));
			    	String line;
			    	while ((line = reader.readLine()) != null) {
		                
	                	String mostMatchAuthor = c.test(languageModels, line) ;
	                								//authorsCompleteSets[1] is the hashmap of {author:testset}
	                }
                }
	  			catch (Exception e) {
			    	System.err.println(e);
			    	System.err.println("Could not open file to test");
			  	}
            }
        }
		else {
			System.out.println("Please provide [-dev authorlist] or [-test authorlist testset.txt]");
		}

	}
}