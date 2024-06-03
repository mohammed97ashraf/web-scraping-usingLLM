import os
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info
import json

load_dotenv()

openai_key = os.getenv("OPENAI_APIKEY")

graph_config = {
   "llm": {
      "api_key": openai_key,
      "model": "gpt-3.5-turbo",
   },
}

# ************************************************
# Create the SmartScraperGraph instance and run it
# ************************************************

smart_scraper_graph = SmartScraperGraph(
   prompt="List me all the products name with their price.",
   # also accepts a string with the already downloaded HTML code
   source="https://www.amazon.in/iphone/s?k=iphone",
   config=graph_config
)

result = smart_scraper_graph.run()
with open("results.json", 'w', encoding='utf-8') as f:
      json.dump(result,f, indent=4)
      