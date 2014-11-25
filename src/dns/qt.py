from dnsserver import Query
q = Query("ASDFASDF")
out = q.question("google.com")
print out
