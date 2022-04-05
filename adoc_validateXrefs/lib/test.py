import getOutputFile as OfClass

x = OfClass.utils.getOutputFile('fred')
if x:
    of = open(x, 'w')
    of.write('fred')
    with of:
        of.write('fred2 ')
    of.close()

