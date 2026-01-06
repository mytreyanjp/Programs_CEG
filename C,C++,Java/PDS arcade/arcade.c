#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

// Structure to represent a stack
struct stack {
    int *array;
    int capacity;
    int top;
};

// Function to create a stack with a given capacity
struct stack* createstack(int capacity) {
    struct stack* stack = (struct stack*)malloc(sizeof(struct stack));
    stack->capacity = capacity;
    stack->top = -1;
    stack->array = (int*)malloc(stack->capacity * sizeof(int));
    return stack;
}

// Function to check if a stack is empty
int isempty(struct stack* stack) {
    return stack->top == -1;
}

// Function to push an item onto the stack
void push(struct stack* stack, int item) {
    stack->array[++stack->top] = item;
}

// Function to pop an item from the stack
int pop(struct stack* stack) {
    return stack->array[stack->top--];
}

// Function to move a disk from one peg to another
void movedisk(char from, char to, int disk) {
    printf("Move disk %d from %c to %c\n", disk, from, to);
}

// Function to display the contents of a peg
void displaypeg(char peg, struct stack* stack) {
    printf("Peg %c: ", peg);
    if (isempty(stack)) {
        printf("Empty\n");
        return;
    }

    for (int i = 0; i <= stack->top; ++i) {
        printf("%d ", stack->array[i]);
    }
    printf("\n");
}

int isstackarrayascending(struct stack* stack) {
    if (isempty(stack)) {
        return 2;
    }
    for (int i = 0; i < stack->top; ++i) {
        if (stack->array[i] > stack->array[i + 1]) {
            // If any element is greater than its next element, not in ascending
            return 0;
        }
    }
    return 1; // All elements are in ascending order
}

// Function to perform Tower of Hanoi using stacks
int towerofhanoi(int numdisks, struct stack* source, struct stack* auxiliary, struct stack* target) {
    int totalmoves = (1 << numdisks) - 1; // Total moves required

    // Initialize the source peg
    for (int i = numdisks; i > 0; --i) {
        push(source, i);
    }

    int temp = source->array[0];
    source->array[0] = source->array[numdisks - 1];
    source->array[numdisks - 1] = temp;

    // Display initial state
    printf("Initial state:\n");
    displaypeg('A', source);
    displaypeg('B', auxiliary);
    displaypeg('C', target);

    // Perform the Tower of Hanoi
    int moves = 0;
    while (1) {
        char sourcepeg, targetpeg;

        printf("Enter source peg (A, B, C) for the next move: ");
        scanf(" %c", &sourcepeg);
        printf("Enter target peg (A, B, C) for the next move: ");
        scanf(" %c", &targetpeg);

        struct stack* sourcestack;
        struct stack* targetstack;

        switch (sourcepeg) {
            case 'A':
                sourcestack = source;
                break;
            case 'B':
                sourcestack = auxiliary;
                break;
            case 'C':
                sourcestack = target;
                break;
            default:
                printf("Invalid source peg. Please enter A, B, or C.\n");
                continue;
        }

        if (isempty(sourcestack)) {
            printf("Selected Peg has no disks, Please select another Disk\n");
            continue;
        }

        switch (targetpeg) {
            case 'A':
                targetstack = source;
                break;
            case 'B':
                targetstack = auxiliary;
                break;
            case 'C':
                targetstack = target;
                break;
            default:
                printf("Invalid target peg. Please enter A, B, or C.\n");
                continue;
        }

        // Perform the move
        int disk = pop(sourcestack);
        push(targetstack, disk);

        // Display the updated state
        displaypeg('A', source);
        displaypeg('B', auxiliary);
        displaypeg('C', target);
        moves++;

        if (target->top == numdisks - 1)
            if (isstackarrayascending(target))
                break;
    }

    printf("Your Count of moves to finish: %d\n", moves);
    return moves;
}

//number guessing game - tree implementation of tournament kinda concept


struct player {
    char name[50];
    int guess;
    int attempts;
};

struct node {
    struct player player;
    struct node *left;
    struct node *right;
};

struct node *create_node(struct player player) {
    struct node *node = (struct node *)malloc(sizeof(struct node));
    node->player = player;
    node->left = node->right = NULL;
    return node;
}

int generate() {
    // Generate a random number between 1 and 10
    return rand() % 10 + 1;
}

struct player play(struct player player1, struct player player2) {
    int target_number = generate();

    //printf("Target number: %d\n", target_number);

    // Players guess the same number until one of them gets it right
    while (1) {
        // Player 1 guesses
        printf("%s, enter your guess: ", player1.name);
        scanf("%d", &player1.guess);
        player1.attempts++;

        // Player 2 guesses
        printf("%s, enter your guess: ", player2.name);
        scanf("%d", &player2.guess);
        player2.attempts++;

        // Check if either player guessed correctly
        if (player1.guess == target_number || player2.guess == target_number) {
            break;
        }

        // Print hints if both players haven't guessed correctly
        printf("Too %s for %s. Too %s for %s.\n",
               (player1.guess < target_number) ? "low" : "high", player1.name,
               (player2.guess < target_number) ? "low" : "high", player2.name);
    }

    // Determine the winner by correct guess
    if (player1.guess == target_number && player2.guess != target_number) {
        printf("%s wins this round!\n", player1.name);
        printf("\n");
        printf("\n");
        printf("\n");
        return player1;
    } else if (player2.guess == target_number && player1.guess != target_number) {
        printf("%s wins this round!\n", player2.name);
        printf("\n");
        printf("\n");
        printf("\n");
        return player2;
    } else {
        // Both players guessed correctly; determine the winner by attempts
        printf("Both players guessed correctly. Determining the winner by attempts.\n");
        printf("\n");
        printf("\n");
        printf("\n");
        return (player1.attempts < player2.attempts) ? player1 : player2;
    }
}

struct node *tournament(struct player players[], int start, int end) {
    if (start == end) {
        return create_node(players[start]);
    }

    int mid = (start + end) / 2;

    struct node *left = tournament(players, start, mid);
    struct node *right = tournament(players, mid + 1, end);

    struct player winner = play(left->player, right->player);

    struct node *root = create_node(winner);
    root->left = left;
    root->right = right;

    return root;
}

void free_tree(struct node *root) {
    if (root == NULL) {
        return;
    }

    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

//snake and ladder - array implementation of snakes and ladders


// Function to roll a six-sided die
int rolldie() {
    return rand() % 6 + 1;
}


void displayboard(char x, char o, int posx, int poso, int *snakeladder) {

    printf("Welcome to Snake and Ladder Game!\n");
    printf("Reach position 100 to win.\n\n");

    for (int row = 10; row >= 1; row--) {
        for (int col = 1; col <= 10; col++) {
            int square = row * 10;

            if (row % 2 == 0) {
                square = (row - 1) * 10 + 10 - col + 1; //reverse printing of rows like all snake and ladder
            } else {
                square = (row - 1) * 10 + col;
            }

            char symbol = ' ';

            if (square == posx) {
                printf("|%c%c", x, symbol); // Player X position
            } else if (square == poso) {
                printf("|%c%c", o, symbol); // Player O position
            } else {
                for (int i = 0; i < 2 * 6; i += 2) {
                    if (square == snakeladder[i]) {
                        symbol = 's'; // Snake
                    } else if (square == snakeladder[i + 1]) {
                        symbol = 'l'; // Ladder
                    }
                }

                printf("|%2d%c", square, symbol);
            }
        }

        printf("\n");
    }
}


int handlesnakeladder(int position, int *snakeladder) {
    for (int i = 0; i < 2 * 6; i += 2) {
        if (position == snakeladder[i]) {
            printf("Snake at position %d! Sliding down to %d.\n", position, snakeladder[i + 1]);
            return snakeladder[i + 1];
        } else if (position == snakeladder[i + 1]) {
            printf("Ladder at position %d! Climbing up to %d.\n", position, snakeladder[i]);
            return snakeladder[i];
        }
    }
    return position;
}


void playgame(char x, char o) {
    int posx = 1;
    int poso = 1;
    int dice;

    int snakeladder[] = {98, 28, 95, 24, 92, 51, 83, 19, 69, 33, 64, 36};

    while (1) {
        displayboard(x, o, posx, poso, snakeladder);

        printf("%c, enter '0' to roll the die or '-1' to exit: ", x);
        scanf("%d", &dice);

        if (dice == -1) {
            printf("Exiting the game. Thanks for playing!\n");
            break;
        } else if (dice != 0) {
            printf("Invalid input. Enter '0' to roll the die or '-1' to exit.\n");
            continue;
        }

        dice = rolldie();
        printf("%c rolled a %d.\n", x, dice);

        if (posx + dice > 100) {
            printf("Oops! %c needs %d to reach the end exactly. Try again.\n", x, 100 - posx);
        } else {
            posx += dice;
            posx = handlesnakeladder(posx, snakeladder); //[i] = snake and [i+1] is a ladder

            printf("%c moves to box %d.\n", x, posx);

            if (posx == 100) {
                printf("%c wins! Congratulations!\n", x);
                break;
            }
        }

        displayboard(x, o, posx, poso, snakeladder);

        printf("%c, enter '0' to roll the die or '-1' to exit: ", o);
        scanf("%d", &dice);

        if (dice == -1) {
            printf("Exiting the game. Thanks for playing!\n");
            break;
        } else if (dice != 0) {
            printf("Invalid input. Enter '0' to roll the die or '-1' to exit.\n");
            continue;
        }

        dice = rolldie();
        printf("%c rolled a %d.\n", o, dice);

        if (poso + dice > 100) {
            printf("Oops! %c needs %d to reach the end exactly. Try again.\n", o, 100 - poso);
        } else {
            poso += dice;
            poso = handlesnakeladder(poso, snakeladder);

            printf("%c moves to box %d.\n", o, poso);

            if (poso == 100) {
                printf("%c wins! Congratulations!\n", o);
                break;
            }
        }
    }
}


//tic -tac -toe

void display_board(char board[3][3]) {
    printf("\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            printf(" %c ", board[i][j]);
            if (j < 2) printf("|");
        }
        printf("\n");
        if (i < 2) printf("-----------\n");
    }
    printf("\n");
}

// Function to check if a player has won
int check_win(char board[3][3], char player) {
    for (int i = 0; i < 3; i++) {
        if ((board[i][0] == player && board[i][1] == player && board[i][2] == player) ||
            (board[0][i] == player && board[1][i] == player && board[2][i] == player)) {
            return 1; // Player wins
        }
    }

    if ((board[0][0] == player && board[1][1] == player && board[2][2] == player) ||
        (board[0][2] == player && board[1][1] == player && board[2][0] == player)) {
        return 1; // Player wins
    }

    return 0; // No winner yet
}

// Function to check if the board is full
int is_board_full(char board[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == ' ') {
                return 0; // Board is not full
            }
        }
    }
    return 1; // Board is full
}

// Function to play Tic Tac Toe
int play_tic_tac_toe(char player1[20], char player2[20]) {
    char board[3][3] = {{' ', ' ', ' '}, {' ', ' ', ' '}, {' ', ' ', ' '}};
    int row, col;
    char current_player = 'X';

    do {
        display_board(board);

        int valid_move = 0;

        // Get valid move from the current player
        while (!valid_move) {
            printf("%s, enter your move (row and column): ", (current_player == 'X') ? player1 : player2);
            scanf("%d %d", &row, &col);

            // Check if the chosen cell is empty
            if (row >= 0 && row < 3 && col >= 0 && col < 3 && board[row][col] == ' ') {
                board[row][col] = current_player;
                valid_move = 1;
            } else {
                printf("Invalid move. Try again.\n");
            }
        }

        // Check if the current player wins
        if (check_win(board, current_player)) {
            display_board(board);
            printf("%s wins!\n", (current_player == 'X') ? player1 : player2);
            return (current_player == 'X') ? 1 : 2;
        }

        // Check if the board is full (a tie)
        if (is_board_full(board)) {
            display_board(board);
            printf("It's a tie!\n");
            return 0;
        }

        // Switch to the other player
        current_player = (current_player == 'X') ? 'O' : 'X';

    } while (1);
}




//menu driven for all these three games.



int main() {
    srand(time(NULL)); //this is for random number generation

    int choice;
    do {
        printf("\n----------------- WELCOME ----------------------------\n");
        printf("\n--------------- JSM ARCADE ---------------------------\n");
        printf("\n Choose Our Games: \n");
        printf("1. Tower of Hanoi\n");
        printf("2. Snake and Ladder\n");
        printf("3. Number Guessing Tournament\n");
        printf("4. Tic Tac Toe\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: {
                // Tower of Hanoi
                int numdisks;
                int score[2];
                char player1[50];
                char player2[50];

                printf("\n");
                printf("\n");
                printf("\n");
                printf("----------- YOU CHOSE TOWER OF HANOI. GOOD LUCK ------------\n");

                printf("Welcome To Tower Of Hanoi\nEnter the number of disks for Tower of Hanoi: ");
                scanf("%d", &numdisks);

                printf("Enter Player 1 Name: ");
                scanf("%s", player1);

                printf("Enter Player 2 Name: ");
                scanf("%s", player2);

                for (int i = 0; i < 2; i++) {
                    printf("Turn of Player %d: %s\n", i + 1, (i == 0) ? player1 : player2);

                    printf("Order the elements in ascending order in Peg C\n");

                    // Create stacks for the three pegs
                    struct stack* source = createstack(numdisks);
                    struct stack* auxiliary = createstack(numdisks);
                    struct stack* target = createstack(numdisks);

                    score[i] = towerofhanoi(numdisks, source, auxiliary, target);

                    // Free allocated memory
                    free(source->array);
                    free(source);
                    free(auxiliary->array);
                    free(auxiliary);
                    free(target->array);
                    free(target);
                }

                printf("Player1 Score: %d\n Player2 Score: %d\n", score[0], score[1]);
                if (score[0] < score[1]) {
                    printf("Congats %s won\n", player1);
                } else if (score[0] > score[1]) {
                    printf("Congrats %s won\n", player2);
                } else {
                    printf("Draw the match\n");
                }
                break;
            }
            case 2: {
                // Snake and Ladder
                printf("\n");
                printf("\n");
                printf("\n");
                printf("----------- YOU CHOSE SNAKE AND LADDER. GOOD LUCK ------------\n");
                char x;
                char o;

                printf("Enter the first letters of Player X and Player O's names (e.g., 'A B'): ");
                scanf(" %c %c", &x, &o);

                playgame(x, o);
                break;
            }
            case 3: {
                // Number Guessing Tournament

                printf("\n");
                printf("\n");
                printf("\n");
                printf("----------- YOU CHOSE NUMBER GUESSING. GOOD LUCK ------------\n");
                int num_players;
                printf("Enter the number of players: ");
                scanf("%d", &num_players);

                struct player players[num_players];

                for (int i = 0; i < num_players; ++i) {
                    printf("Enter the name of Player %d: ", i + 1);
                    scanf("%s", players[i].name);
                }

                struct node *root = tournament(players, 0, num_players - 1);

                printf("The overall winner is %s\n", root->player.name);

                free_tree(root);
                break;
            }
            case 4: {
                // Tic Tac Toe
                char player1[20], player2[20];
                int winner;

                printf("\n");
                printf("\n");
                printf("\n");
                printf("----------- YOU CHOSE TIC TAC TOE. GOOD LUCK ------------\n");

                printf("Enter Player 1 name: ");
                scanf("%s", player1);
                printf("Enter Player 2 name: ");
                scanf("%s", player2);

                winner = play_tic_tac_toe(player1, player2);

                if (winner == 1) {
                    printf("%s wins the Tic Tac Toe game!\n", player1);
                } else if (winner == 2) {
                    printf("%s wins the Tic Tac Toe game!\n", player2);
                } else {
                    printf("It's a tie in the Tic Tac Toe game!\n");
                }
                break;
            }
            case 5:
                printf("Exiting the program. Thanks for playing!\n");
                break;
            default:
                printf("Invalid choice. Please enter a valid option.\n");
        }
    } while (choice != 5);

    return 0;
}