import src.lib.messenger as m
import src.dns.dnsserver as dnsserver
from src.config import config
m.send_latency_request("localhost", 8080, "54.94.156.232")
m.send_latency_request("localhost", 8080, "198.41.209.138")
m.send_latency_request("localhost", 8080, "129.10.116.51")
m.send_latency_request("localhost", 8080, "54.94.156.235")
m.send_latency_request("localhost", 8080, "54.94.156.23")
m.send_latency_request("localhost", 8080, "54.94.16.232")

print dnsserver.handle_response("54.94.156.232", config())
print dnsserver.handle_response("127.0.0.1", config())

