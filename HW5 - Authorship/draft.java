			//Trigram first
			for (int i = 0; i < tokens.size()-2; i++){
				if (lm.bigram.get(tokens.get(i)+tokens.get(i+1)) != null) { 
					if (lm.trigram.get(tokens.get(i)+tokens.get(i+1)+tokens.get(i+2)) != null) { 
						logProb = logProb + Math.log(lm.trigram.get(tokens.get(i)+tokens.get(i+1)+tokens.get(i+2))) - Math.log(lm.bigram.get(tokens.get(i)+tokens.get(i+1)));
					} else { // first occurrence of this bigram, smooth N0
						logProb = logProb + Math.log(lm.getN1("trigram") / lm.getN0("trigram")) - Math.log(lm.bigram.get(tokens.get(i)+tokens.get(i+1)));
					}
				}
				else { // first word has never appeared
					//BACK OFF TO Bigram 
					if (lm.unigram.get(tokens.get(i+1)) != null) { 
						if (lm.bigram.get(tokens.get(i+1)+tokens.get(i+2)) != null) { 
								logProb = 0.8*(logProb + Math.log(lm.bigram.get(tokens.get(i+1)+tokens.get(i+2))) - Math.log(lm.unigram.get(tokens.get(i+1))));
						} else { // first occurrence of this bigram, smooth N0
							logProb = 0.8*(logProb + Math.log(lm.getN1("bigram") / lm.getN0("bigram")) - Math.log(lm.unigram.get(tokens.get(i+1))));
						}
					} else { // first word has never appeared
						// BACK OFF TO uni-gram
						for (int i = 0; i < tokens.size(); i++) {
							if (lm.unigram.get(tokens.get(i)) != null) {
								logProb = 0.6*(logProb + Math.log(lm.unigram.get(tokens.get(i))));
							}
							else {
								logProb = 0.6*(logProb + Math.log(lm.getN1("unigram") / lm.getN0("unigram")));
							}
						}
					}
				}
			}




						//Trigram first
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