import ds_messenger as DM


dm = DM.DirectMessage()
dm.recipient = "hellocookiedough"
dm.message = "This is a message"

dm2 = DM.DirectMessenger(dsuserver = "168.235.86.101", username = "hellocookiedough", password = "thisisapassword")
dm2.send(dm.message, dm.recipient)
print(dm2.retrieve_all())
print(dm2.retrieve_new())
