from pymsfrpc import msfrpc
print(dir(msfrpc))
c = msfrpc.Client()
print(c.get_version)
