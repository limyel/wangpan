f = open('a.mp4', 'wb')
for i in range(1):
    f.write(b' ' * 549696400)
f.close()