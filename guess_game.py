import random
import math

LOWER = 0
UPPER = 10
LEVEL = LOWER
GUESS_QUANTITY = math.log(UPPER - LOWER + 1, 2)
# the lower and upper
X_NUM = random.randint(LOWER, UPPER)
print(f'Количество попыток: {round(GUESS_QUANTITY)}. Удачи!')

# Initializing the number of guesses.
COUNT = 0

# for calculation of minimum number of
# guesses depends upon range
while COUNT < GUESS_QUANTITY:
	COUNT += 1

	# taking guessing number as input
	guess = int(input("Guess a number:- "))

	# Condition testing
	if X_NUM == guess:
		print(f'Молодец! C {COUNT} попыток')
		# Once guessed, loop will break
		break
	elif X_NUM > guess:
		print('Не угадал! Моё число больше.')
	elif X_NUM < guess:
		print('Не угадал! Моё число меньше.')

# If Guessing is more than required guesses,
# shows this output.
if COUNT >= GUESS_QUANTITY:
	print(f'Я загадал {X_NUM}')
	print('Повезет в другой раз!')
