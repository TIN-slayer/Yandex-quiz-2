sp = {}

while True:
    n = input()
    if n == '0':
        break
    n = n.split('*')
    sp[n[0].strip()] = n[1].strip()

print(sp)
