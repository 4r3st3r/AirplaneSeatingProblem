import random


def getSeats(num_rows, num_aisles):
    """
    A function to create the plane seats (in standard plane seat formatting) given the number of rows and aisles
    :param num_rows: Number of rows this plane has
    :param num_aisles: Number of Aisles this plane has
    :return: a list of seats on the plane
    """

    aisleLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    aisleChars = ''.join(aisleLetters[i % len(aisleLetters)] for i in range(num_aisles))

    seats = []

    for row in range(num_rows):
        for char in aisleChars:
            seats.append(f'{row + 1}{char}')

    return seats


class Passenger:
    def __init__(self, seat):
        self.seat = seat
        self.isLost = False


def simulateBoarding(num_rows, num_aisles, nthpassenger=-1):
    """
    A function to simulate the boarding of a plane, where the first passenger forgets their allocated seat and so
    picks another seat, and so on.
    :param num_rows: Specify the number of rows this plane has
    :param num_aisles:
    Specify the number of aisles this plane has
    :param nthpassenger: OPTIONAL to specify which passenger we are interested in, DEFAULTS to the last passenger
    :return: True/False depending on if the nth passenger got their seat
    """

    # If the nth passenger is specified as the last, do so mathematically
    if nthpassenger == -1:
        nthpassenger = (num_rows * num_aisles) - 1

    seats = getSeats(num_rows, num_aisles)

    # Create the passengers, assigning each a seat
    passengers = []

    for ticket in seats:
        passengers.append(Passenger(ticket))

    # Pick a passenger at random, and make him forget which seat he is in
    randomPassenger = random.choice(passengers)
    randomPassenger.isLost = True

    # Sort the list of passengers so that the lost on is first
    sorted_list = sorted(passengers, key=lambda p: not p.isLost)

    # Find the index where isLost becomes False (i.e., first passenger with isLost=False)
    first_non_lost = next((i for i, p in enumerate(sorted_list) if not p.isLost), len(sorted_list))

    # Shuffle the non-lost passengers (isLost=False)
    non_lost_part = sorted_list[first_non_lost:]
    random.shuffle(non_lost_part)

    # Combine the lost (isLost=True) part with the shuffled non-lost part
    passengers = sorted_list[:first_non_lost] + non_lost_part

    # board the passengers one by one, counting the number of times lost passengers must find a new seat
    for i, passenger in enumerate(passengers):

        # Check to see if it is the nth passenger:
        if i == nthpassenger:
            # Check to see if the nth passenger can sit in their seat
            if passenger.seat in seats:
                return True
            else:
                return False

        # Check to see if the passengers seat is taken, if so make them lost
        if passenger.seat not in seats:
            passenger.isLost = True

        # If the passenger is lost, give them a new seat
        if passenger.isLost:
            passenger.seat = random.choice(seats)
            passenger.isLost = False

        # Seat the passenger
        seats.remove(passenger.seat)


# Set the parameters for the test
aisles = 9
rows = 40
num_simulations = 100

successes = 0
for i in range(num_simulations):
    print(f'{i / num_simulations * 100:.2f}% Done')
    if simulateBoarding(rows, aisles):
        successes += 1

probability = successes / num_simulations

print(f'Chance that the nth passenger gets their assigned seat: {probability * 100:.0f}%')
