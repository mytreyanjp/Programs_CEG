#include <stdio.h>
#include <stdlib.h>

#define MAX_PARTICIPANTS 3  // You can change this value to allow more participants

// Structure to hold participant details
struct Participant {
    char name[50];
    int age;
    char email[100];
    char contactNumber[15];
};

int main() {
    struct Participant participants[MAX_PARTICIPANTS];  // Array of participants
    int i;

    // Welcome message
    printf("Welcome to the I++ Event Registration!\n");
    printf("--------------------------------------\n");

    // Loop to get details of each participant
    for(i = 0; i < MAX_PARTICIPANTS; i++) {
        printf("Participant %d:\n", i + 1);

        printf("Name: ");
        fgets(participants[i].name, sizeof(participants[i].name), stdin);

        printf("Age: ");
        scanf("%d", &participants[i].age);
        getchar();  // To clear the newline character from input buffer

        printf("Email: ");
        fgets(participants[i].email, sizeof(participants[i].email), stdin);

        printf("Contact Number: ");
        fgets(participants[i].contactNumber, sizeof(participants[i].contactNumber), stdin);

        printf("--------------------------------------\n");
    }

    // Confirm registration and display details
    printf("\nRegistration Successful!\n");
    printf("Here are the details of the registered participants:\n");
    printf("--------------------------------------\n");

    for(i = 0; i < MAX_PARTICIPANTS; i++) {
        printf("Participant %d Details:\n", i + 1);
        printf("Name: %s", participants[i].name);
        printf("Age: %d\n", participants[i].age);
        printf("Email: %s", participants[i].email);
        printf("Contact Number: %s", participants[i].contactNumber);
        printf("--------------------------------------\n");
    }

    printf("Thank you for registering for I++!\n");

    return 0;
}
