from fastapi import FastAPI, HTTPException
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from decouple import config

app = FastAPI()

api_key = config('API_KEY')
list_id = config('LIST_ID')


@app.get("/")
def root():
    return {"Message": "Greetings!!"}


@app.post("/api/v1/subscribe")
# function to manage subscriber
async def subscribeToNewsLetter(email: str):
    if email is not '':

        # initializing the mailchimp client with api key
        mailchimpClient = Client()
        mailchimpClient.set_config({
            "api_key": api_key,
        })

        userInfo = {
            "email_address": email,
            "status": "subscribed",
        }

        try:
            # adding member to mailchimp audience list
            mailchimpClient.lists.add_list_member(list_id, userInfo)
            return {"message": "Success"}
        except ApiClientError as error:
            print(error.text)
            raise HTTPException(
                status_code=500, detail='Something went wrong somewhere')

    return {"message": "Welcome"}
