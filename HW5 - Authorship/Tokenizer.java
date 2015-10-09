import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.ArrayList;
import java.util.Scanner;

public class Tokenizer {
    
	public ArrayList<String> tokenize(String text) {

        // Remove ;"|`#:%^*_+=~{}<>[]()
        String tokenizedLine = text.replaceAll("[\"\\(\\);\\|`#:%\\^\\*_\\+=~\\{\\}<>\\[\\]]", "");
         
        // Remove commas except within numbers
        tokenizedLine = tokenizedLine.replaceAll("([^0-9]),", "\1");
        tokenizedLine = tokenizedLine.replaceAll(",([^0-9])", "\1");
           
        // Remove single quotes from around words
        tokenizedLine = tokenizedLine.replaceAll("^'", "");
        tokenizedLine = tokenizedLine.replaceAll("([^A-Za-z0-9])'", "\1");
           
        // Treats each punctuation character in .?! as its own token   
        tokenizedLine = tokenizedLine.replaceAll("('|:|-)$", "");
        tokenizedLine = tokenizedLine.replaceAll("('|:|-)([^A-Za-z0-9])", " \2");
           
        
        String[] rawTokens = tokenizedLine.split("\\s+"); // split by any whitespace
        ArrayList<String> tokensList = new ArrayList<String>(); 
        
        // TODO!!! Remove punctuation .!? from everywhere except end of token
        // TODO test tokenization of multiple tokens ending with punct, ex "test! this."
        
        String endsWithPunct = "([^\\.\\?!]*)([\\.\\?!]+)$"; // 0+ non-punctuations followed by 1+ punctuation
        Pattern punctPattern = Pattern.compile(endsWithPunct);
        for (int i = 0; i < rawTokens.length; i++) {
            Matcher m = punctPattern.matcher(rawTokens[i]);
            if (m.find()) { // if token ends with at least one punctuation, split into separate tokens
                String nonPunct = m.group(1);
                String punct = m.group(2);
                tokensList.add(nonPunct);
                for (i = 0; i < punct.length(); i++) {
                    tokensList.add(punct.substring(i, i+1));
                }
            }
            else {
                tokensList.add(rawTokens[i]);
            }
        }
        return tokensList;
	}
    
    public static void main(String[] args) {
        Tokenizer t = new Tokenizer();
        Scanner scanner = new Scanner(System.in);
        String str = "";
        System.out.println("Enter input: ");
        do {
            str = scanner.nextLine();
            ArrayList<String> tokenized = t.tokenize(str);
            System.out.println("Tokenized: ");
            for (int i = 0; i < tokenized.size(); i++) {
                System.out.println(tokenized.get(i));
            }
            System.out.println();
        } while (!str.equals("quit()"));
        System.out.println("Done testing");
    }
}