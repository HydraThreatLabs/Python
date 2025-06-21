import random
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


def guess_number(range_limit: int):
    """
    Number guessing game without attempt limits.
    User tries to guess a random number between 0 and range_limit.
    The game continues until the user guesses correctly.
    """
    number_to_guess = random.randint(0, range_limit)
    tries_counter = 0
    min_difference = range_limit

    while True:
        tries_counter += 1
        try:
            user_guess = int(input(Fore.CYAN + f"Guess a number between 0 and {range_limit}: " + Style.RESET_ALL))
            difference = abs(user_guess - number_to_guess)
            if difference < min_difference:
                min_difference = difference

            if user_guess == number_to_guess:
                print(
                    Fore.GREEN + f"\n🎉 Congratulations! You guessed the number {number_to_guess} in {tries_counter} tries." + Style.RESET_ALL)
                break
            else:
                print(Fore.YELLOW + "Wrong guess, try again!")
                if user_guess < number_to_guess:
                    print(Fore.BLUE + "Too low! 🔻" + Style.RESET_ALL)
                else:
                    print(Fore.MAGENTA + "Too high! 🔺" + Style.RESET_ALL)

        except ValueError as e:
            print(Fore.RED + f"Invalid input, please enter an integer. Error: {e}" + Style.RESET_ALL)


def main():
    print(Fore.GREEN + r"""
 _   _                 _                       
| | | | ___  _ __ ___ | |__   ___  _ __  ___  
| |_| |/ _ \| '_ ` _ \| '_ \ / _ \| '_ \/ __| 
|  _  | (_) | | | | | | |_) | (_) | | | \__ \ 
|_| |_|\___/|_| |_| |_|_.__/ \___/|_| |_|___/ 

    """ + Style.RESET_ALL)

    print(Fore.CYAN + "Welcome to the Hot and Cold Number Guessing Game!" + Style.RESET_ALL)
    print(Fore.CYAN + "Choose difficulty level:" + Style.RESET_ALL)
    print(Fore.YELLOW + "1. Easy (0-10)")
    print("2. Medium (0-100)")
    print("3. Hard (0-1000)")
    print("4. Exit" + Style.RESET_ALL)

    choice = input(Fore.CYAN + "Your choice: " + Style.RESET_ALL)
    if choice == "4":
        print(Fore.RED + "Exiting game. Goodbye!" + Style.RESET_ALL)
        exit()

    if choice == "1":
        guess_number(10)
    elif choice == "2":
        guess_number(100)
    elif choice == "3":
        guess_number(1000)
    else:
        print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)
        main()


if __name__ == "__main__":
    main()