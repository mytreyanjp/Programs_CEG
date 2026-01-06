import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

public class CarNamesProcessor {

    // Method to check if a car name matches the required pattern
    private static boolean isValidCarName(String carName) {
        // Starts with B, M, or L, followed by any letter/digit(s), and ends with '3'
        String pattern = "^[BML][a-zA-Z0-9]*3$";
        return carName.matches(pattern);
    }

    // Method to change the last three characters to 'XXX'
    private static String maskLastThreeChars(String carName) {
        if (carName.length() < 3) {
            return carName; // Return as-is if less than 3 characters
        }
        return carName.substring(0, carName.length() - 3) + "XXX";
    }

    public static void main(String[] args) {
        String filename = "car_names.txt";
        Set<String> uniqueCarNames = new HashSet<>();   // Set to remove duplicates
        List<String> filteredCarNames = new ArrayList<>(); // List for valid, modified car names

        try {
            // Step 1: Read all lines from the file
            List<String> lines = Files.readAllLines(Paths.get(filename));
            
            // Step 2: Filter valid car names, remove duplicates
            for (String line : lines) {
                String carName = line.trim();
                
                // Check for duplicates and pattern matching
                if (!uniqueCarNames.contains(carName) && isValidCarName(carName)) {
                    uniqueCarNames.add(carName); // Add to set to ensure uniqueness
                    filteredCarNames.add(maskLastThreeChars(carName)); // Mask last 3 chars and add to list
                }
            }
            
            // Step 3: Sort the list
            Collections.sort(filteredCarNames);

            // Step 4: Write the sorted, modified names back to the file (overwrite)
            try (BufferedWriter writer = Files.newBufferedWriter(Paths.get(filename))) {
                for (String carName : filteredCarNames) {
                    writer.write(carName);
                    writer.newLine();
                }
            }
            
            System.out.println("File processed successfully!");

        } catch (IOException e) {
            System.out.println("An error occurred: " + e.getMessage());
        }
    }
}
