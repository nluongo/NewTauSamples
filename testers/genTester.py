#from helpScripts import isLocalMax, getSeedCell

test_var = 'here we are'

big_string = """The test_var is {}. Did it show up?""".format(test_var)
print big_string
exit()

cells = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0],
         [0, 0, 0],
         [0, 1, 0],
         [0, 1, 0],
         [1, 1, 1],
         [2, 2, 1],
         [1, 1, 1],
         [0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

print [entry[0] for entry in cells]
exit()
print cells[4][1]
print cells[3][-1]
print isLocalMax(cells, 4, 1)
print getSeedCell(cells)
