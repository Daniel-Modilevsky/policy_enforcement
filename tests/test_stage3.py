# # Creating instances of rules
# rule1 = Rule(id="1", name="Generic Rule", ip_proto=IPv4Network("192.168.0.0/24"), source_port=80)
# arupa_rule = ArupaRule(id="2", name="Arupa Rule", ip_proto=IPv4Network("10.0.0.0/24"), source_port=8080, source_subnet=IPv4Network("192.168.1.0/24"))
# frisco_rule = FriscoRule(id="3", name="Frisco Rule", ip_proto=IPv4Network("172.16.0.0/24"), source_port=443, source_ip=IPv4Network("192.168.2.0/24"), destination_ip=IPv4Network("192.168.3.0/24"))
#
# # Creating a policy and adding the rules
# policy = Policy(id="policy-1", name="Sample Policy", description="Example policy", type=PolicyType.ARUPA, rules={rule1, arupa_rule, frisco_rule})
#
# # Serializing the policy to a dictionary
# policy_dict = policy.to_dict()
#
# print(policy_dict)