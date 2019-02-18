from twilio.rest import Client 
 
account_sid = 'ACd0767ea59a8b91740f8c3cc02e18e627' 
auth_token = 'edc7fa535e6bf70fdb5e5ccb6aea9e59' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Please have your medicine',      
                              to='whatsapp:+919999795087' 
                          )
