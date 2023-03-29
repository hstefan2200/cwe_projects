/**
 * Sha-256 Implementation
 */
import java.util.*;
import java.io.*;
import java.math.BigInteger;
import java.security.NoSuchAlgorithmException;
import java.security.MessageDigest;


public class Sha256 {
	public static String getSha256Hash(String input) {
		try {
			MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
			byte[] messageDigest = sha256.digest(input.getBytes());
			BigInteger bigInt = new BigInteger(1, messageDigest);
			String digestStr = bigInt.toString(16);
			while (digestStr.length() < 64) {
				digestStr = "0" + digestStr;
			}
			return digestStr;
		}
		catch (NoSuchAlgorithmException e) {
			throw new RuntimeException(e);
		}
	}
	
	public static void main(String[] args) {
    	Scanner scan = new Scanner(System.in);
    	System.out.println("Enter string to be hashed:");
    	String plainText = scan.nextLine();
    	System.out.println("Your string in plaintext: " + plainText);
    	System.out.println("Your string hashed using Sha-256: " + getSha256Hash(plainText));
	}
}