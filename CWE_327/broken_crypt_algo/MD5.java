/**
 * MD5 Implementation
 */
import java.util.*;
import java.io.*;
import java.math.BigInteger;
import java.security.NoSuchAlgorithmException;
import java.security.MessageDigest;


public class MD5 {
	public static String getMd5Hash(String input) {
		try {
			MessageDigest md5 = MessageDigest.getInstance("MD5");
			byte[] messageDigest = md5.digest(input.getBytes());
			BigInteger bigInt = new BigInteger(1, messageDigest);
			String digestStr = bigInt.toString(16);
			while (digestStr.length() < 32) {
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
    	System.out.println("Your string hashed using MD5: " + getMd5Hash(plainText));
	}
}