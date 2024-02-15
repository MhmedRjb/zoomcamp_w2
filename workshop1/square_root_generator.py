def square_root_generator(limit):
    n = 1
    while n <= limit:
        yield n ** 0.5
        n += 1

# Example usage:

#if main 
if __name__ == "__main__":
    limit = 5
    generator = square_root_generator(limit)
    temp=0
    for sqrt_value in generator:
        temp=temp+sqrt_value
    print (f"the sum of the outputs of the generator for limit = 5 is {temp}")
