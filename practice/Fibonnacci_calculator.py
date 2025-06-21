def fibonacci(n):
    """
    Calculate the n-th Fibonacci number.

    Args:
        n (int): The position in the Fibonacci sequence (must be >= 1).

    Returns:
        int or str: The n-th Fibonacci number, or an error message if input is invalid.
    """
    if not isinstance(n, int):
        return 'Please provide an integer.'
    if n < 1:
        return 'Number must be greater than or equal to 1.'
    if n == 1:
        return 0
    if n == 2:
        return 1

    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
    return b


def main():
    print("🔢 Fibonacci Number Calculator 🔢")
    try:
        n = int(input("Enter which Fibonacci number you'd like to get (e.g. 10): "))
        result = fibonacci(n)
        if isinstance(result, int):
            print(f"\n✨ The {n}-th Fibonacci number is: {result} ✨")
        else:
            print(f"\n❗ {result} ❗")
    except ValueError:
        print("\n❌ Please enter a valid integer. ❌")


if __name__ == "__main__":
    main()