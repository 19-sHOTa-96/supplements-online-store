from random import randint

def generate_code(n):
	r = []
	for _ in range(n):
		r.append(str(randint(0, n)))
	return int(''.join(r))

r = generate_code(5)
print(r)
