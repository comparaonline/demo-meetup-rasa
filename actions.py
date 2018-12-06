from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from requests import get

class ActionCoinValueSearch(Action):
   def name(self):
      # type: () -> Text
      return "action_coin_value_search"

   def run(self, dispatcher, tracker, domain):
      # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict[Text, Any]]

      coin = tracker.get_slot('coin')[0]
      coin_map = {
        "bitcoin": 1,
        "ether": 1027
      }
      response = get(f"https://api.coinmarketcap.com/v2/ticker/{coin_map[coin]}/")
      try:
        price = response.json()['data']['quotes']['USD']['price']
      except Exception as e:
        price = None
      if price:
        response = f"El valor de {coin} es actualmente USD{price:.2f}"
      else:
        response = f"No pude obtener el valor de {coin}"
      
      dispatcher.utter_message(response)
      return [SlotSet("coin", coin)]